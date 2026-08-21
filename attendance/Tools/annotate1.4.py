import json
import os
import cv2
import config
import tkinter as tk

# ==========================================
# 🌐 CONFIGURATION & PATH SETUP
# ==========================================
IMAGE_PATH = getattr(config, "IMAGE_PATH", "Dataset/RawPicture/")
ANNOTATION_PATH = getattr(config, "ANNOTATION_PATH", "Dataset/Annotated/")
IMAGE_EXTN = getattr(config, "IMAGE_EXTN", ".jpg")
ImageName = getattr(config, "IMAGE_NAME", "")

if hasattr(config, "get_image_path"):
    FULL_IMAGE_PATH = config.get_image_path(ImageName)
else:
    FULL_IMAGE_PATH = os.path.join(IMAGE_PATH, ImageName + IMAGE_EXTN)

if hasattr(config, "get_annotation_path"):
    FULL_ANNOTATION_PATH = config.get_annotation_path(ImageName)
else:
    FULL_ANNOTATION_PATH = os.path.join(ANNOTATION_PATH, ImageName + ".json")

# Global tracking state
drawing = False
ix, iy = -1, -1
temp_image = None
current_image = None
raw_image = None

# Zoom & Pan State
zoom_scale = 1.0
pan_x = 0
pan_y = 0

# UI Scrollbar dragging flags
dragging_h_bar = False
dragging_v_bar = False

BAR_THICKNESS = 18  # Thickness of embedded scrollbars in pixels

existing_boxes = []  # Drawn in GREEN
new_yolo_boxes = []  # Drawn in RED


def load_existing_annotations(json_path):
    if not os.path.exists(json_path):
        print(f"⚠️ Notice: '{json_path}' not found. A new file will be created on save.")
        return []

    with open(json_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = data.get("annotations", data.get("labels", []))

    normalized = []
    for item in data:
        if isinstance(item, str):
            parts = item.strip().split()
            if len(parts) >= 5:
                normalized.append(" ".join(parts[:5]))
        elif isinstance(item, dict):
            bbox = item.get("bbox", item.get("box", []))
            if len(bbox) == 4:
                cls_id = item.get("class", 0)
                normalized.append(
                    f"{cls_id} {bbox[0]:.4f} {bbox[1]:.4f} {bbox[2]:.4f} {bbox[3]:.4f}"
                )

    return normalized


def yolo_to_pixels(box_str, img_w, img_h):
    parts = box_str.strip().split()
    _, x_c, y_c, w, h = map(float, parts[:5])

    x1 = int((x_c - w / 2.0) * img_w)
    y1 = int((y_c - h / 2.0) * img_h)
    x2 = int((x_c + w / 2.0) * img_w)
    y2 = int((y_c + h / 2.0) * img_h)

    return x1, y1, x2, y2


def display_to_image_coords(disp_x, disp_y):
    """Converts display window coordinates back to original unzoomed image coordinates."""
    img_x = int((disp_x / zoom_scale) + pan_x)
    img_y = int((disp_y / zoom_scale) + pan_y)

    img_h, img_w, _ = raw_image.shape
    img_x = max(0, min(img_x, img_w - 1))
    img_y = max(0, min(img_y, img_h - 1))
    return img_x, img_y


def clamp_pan():
    """Keeps pan values bounded within valid ranges based on current zoom."""
    global pan_x, pan_y
    img_h, img_w, _ = raw_image.shape

    max_pan_x = max(0, img_w - int(img_w / zoom_scale))
    max_pan_y = max(0, img_h - int(img_h / zoom_scale))

    pan_x = max(0, min(pan_x, max_pan_x))
    pan_y = max(0, min(pan_y, max_pan_y))


def redraw_canvas():
    global current_image, temp_image, raw_image, existing_boxes, new_yolo_boxes

    current_image = raw_image.copy()
    img_h, img_w, _ = current_image.shape

    # 1. Render Existing Annotations (GREEN)
    for idx, box_str in enumerate(existing_boxes, start=1):
        x1, y1, x2, y2 = yolo_to_pixels(box_str, img_w, img_h)
        cv2.rectangle(current_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            current_image,
            f"#{idx}",
            (x1, max(y1 - 5, 12)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

    # 2. Render Newly Added Annotations (RED)
    for idx, box_str in enumerate(new_yolo_boxes, start=1):
        x1, y1, x2, y2 = yolo_to_pixels(box_str, img_w, img_h)
        cv2.rectangle(current_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            current_image,
            f"NEW #{idx}",
            (x1, max(y1 - 5, 12)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    temp_image = current_image.copy()


def get_view_crop_with_scrollbars(img):
    """Crops the zoomed view and draws custom scrollbars along the bottom and right edges."""
    img_h, img_w, _ = img.shape
    view_w = max(1, int(img_w / zoom_scale))
    view_h = max(1, int(img_h / zoom_scale))

    crop = img[pan_y : pan_y + view_h, pan_x : pan_x + view_w]
    canvas = cv2.resize(crop, (img_w, img_h), interpolation=cv2.INTER_LINEAR)

    max_pan_x = max(1, img_w - view_w)
    max_pan_y = max(1, img_h - view_h)

    # -------------------------------------------------------------
    # 1. Draw Bottom Horizontal Scrollbar
    # -------------------------------------------------------------
    bar_h_y1 = img_h - BAR_THICKNESS
    bar_h_y2 = img_h
    bar_h_w = img_w - BAR_THICKNESS

    cv2.rectangle(canvas, (0, bar_h_y1), (bar_h_w, bar_h_y2), (50, 50, 50), -1)

    thumb_w = max(20, int(bar_h_w / zoom_scale))
    thumb_x1 = int((pan_x / max_pan_x) * (bar_h_w - thumb_w))
    thumb_x2 = thumb_x1 + thumb_w
    cv2.rectangle(
        canvas, (thumb_x1, bar_h_y1 + 2), (thumb_x2, bar_h_y2 - 2), (180, 180, 180), -1
    )

    # -------------------------------------------------------------
    # 2. Draw Side Vertical Scrollbar
    # -------------------------------------------------------------
    bar_v_x1 = img_w - BAR_THICKNESS
    bar_v_x2 = img_w
    bar_v_h = img_h - BAR_THICKNESS

    cv2.rectangle(canvas, (bar_v_x1, 0), (bar_v_x2, bar_v_h), (50, 50, 50), -1)

    thumb_h = max(20, int(bar_v_h / zoom_scale))
    thumb_y1 = int((pan_y / max_pan_y) * (bar_v_h - thumb_h))
    thumb_y2 = thumb_y1 + thumb_h
    cv2.rectangle(
        canvas, (bar_v_x1 + 2, thumb_y1), (bar_v_x2 - 2, thumb_y2), (180, 180, 180), -1
    )

    # Corner Box
    cv2.rectangle(canvas, (bar_v_x1, bar_h_y1), (img_w, img_h), (30, 30, 30), -1)

    return canvas


def handle_right_click_delete(click_x, click_y):
    global existing_boxes, new_yolo_boxes, current_image

    img_h, img_w, _ = current_image.shape

    for idx in range(len(new_yolo_boxes) - 1, -1, -1):
        x1, y1, x2, y2 = yolo_to_pixels(new_yolo_boxes[idx], img_w, img_h)
        if x1 <= click_x <= x2 and y1 <= click_y <= y2:
            removed = new_yolo_boxes.pop(idx)
            print(f"🗑️ Deleted New Box #{idx + 1}: {removed}")
            redraw_canvas()
            return

    for idx in range(len(existing_boxes) - 1, -1, -1):
        x1, y1, x2, y2 = yolo_to_pixels(existing_boxes[idx], img_w, img_h)
        if x1 <= click_x <= x2 and y1 <= click_y <= y2:
            removed = existing_boxes.pop(idx)
            print(f"🗑️ Deleted Existing Box #{idx + 1}: {removed}")
            redraw_canvas()
            return


def update_pan_from_h_bar(x):
    global pan_x
    img_h, img_w, _ = raw_image.shape
    view_w = max(1, int(img_w / zoom_scale))
    max_pan_x = max(1, img_w - view_w)
    bar_h_w = img_w - BAR_THICKNESS
    thumb_w = max(20, int(bar_h_w / zoom_scale))

    pct = max(0.0, min(1.0, x / max(1, (bar_h_w - thumb_w))))
    pan_x = int(pct * max_pan_x)
    clamp_pan()


def update_pan_from_v_bar(y):
    global pan_y
    img_h, img_w, _ = raw_image.shape
    view_h = max(1, int(img_h / zoom_scale))
    max_pan_y = max(1, img_h - view_h)
    bar_v_h = img_h - BAR_THICKNESS
    thumb_h = max(20, int(bar_v_h / zoom_scale))

    pct = max(0.0, min(1.0, y / max(1, (bar_v_h - thumb_h))))
    pan_y = int(pct * max_pan_y)
    clamp_pan()


def draw_mouse_bbox(event, x, y, flags, param):
    global ix, iy, drawing, temp_image, current_image, new_yolo_boxes
    global dragging_h_bar, dragging_v_bar

    img_h, img_w, _ = current_image.shape

    is_over_h_bar = (y >= img_h - BAR_THICKNESS) and (x < img_w - BAR_THICKNESS)
    is_over_v_bar = (x >= img_w - BAR_THICKNESS) and (y < img_h - BAR_THICKNESS)

    if event == cv2.EVENT_LBUTTONDOWN:
        if is_over_h_bar:
            dragging_h_bar = True
            update_pan_from_h_bar(x)
        elif is_over_v_bar:
            dragging_v_bar = True
            update_pan_from_v_bar(y)
        else:
            drawing = True
            real_x, real_y = display_to_image_coords(x, y)
            ix, iy = real_x, real_y

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging_h_bar:
            update_pan_from_h_bar(x)
        elif dragging_v_bar:
            update_pan_from_v_bar(y)
        elif drawing:
            real_x, real_y = display_to_image_coords(x, y)
            temp_image = current_image.copy()
            cv2.rectangle(temp_image, (ix, iy), (real_x, real_y), (0, 0, 255), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging_h_bar = False
        dragging_v_bar = False

        if drawing:
            drawing = False
            real_x, real_y = display_to_image_coords(x, y)
            x1, y1 = min(ix, real_x), min(iy, real_y)
            x2, y2 = max(ix, real_x), max(iy, real_y)

            if (x2 - x1) > 5 and (y2 - y1) > 5:
                width = (x2 - x1) / img_w
                height = (y2 - y1) / img_h
                x_center = (x1 + (x2 - x1) / 2) / img_w
                y_center = (y1 + (y2 - y1) / 2) / img_h

                yolo_str = f"0 {x_center:.4f} {y_center:.4f} {width:.4f} {height:.4f}"
                new_yolo_boxes.append(yolo_str)
                print(f"➕ Added Box #{len(new_yolo_boxes)}: {yolo_str}")

                redraw_canvas()

    elif event == cv2.EVENT_RBUTTONDOWN:
        if not is_over_h_bar and not is_over_v_bar:
            real_x, real_y = display_to_image_coords(x, y)
            handle_right_click_delete(real_x, real_y)


def run_interactive_annotator():
    global current_image, temp_image, raw_image, existing_boxes, new_yolo_boxes
    global zoom_scale, pan_x, pan_y

    raw_image = cv2.imread(FULL_IMAGE_PATH)
    if raw_image is None:
        print(f"❌ Error: Could not open image at '{FULL_IMAGE_PATH}'")
        return

    existing_boxes = load_existing_annotations(FULL_ANNOTATION_PATH)
    new_yolo_boxes = []

    redraw_canvas()

    window_name = f"Annotator | 'S': Save | Right-Click: Delete | 'Z': Undo | 'Q': Quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    window_width = screen_width
    window_height = screen_height - 70

    cv2.resizeWindow(window_name, window_width, window_height)
    cv2.moveWindow(window_name, 0, 0)
    cv2.setMouseCallback(window_name, draw_mouse_bbox)

    print("\n" + "=" * 50)
    print(" 🖱️ INTERACTIVE ANNOTATOR CONTROLS")
    print("=" * 50)
    print("• Left/Right Arrows : Slide BOTTOM scroll bar (Horizontally)")
    print("• Up/Down Arrows    : Slide SIDE scroll bar (Vertically)")
    print("• Press '+' / '-'   : Zoom In / Zoom Out")
    print("• Left-Click & Drag : Draw a new box (RED)")
    print("• Right-Click Box   : Delete box under cursor")
    print("• Press 'Z'         : Undo last drawn box")
    print("• Press 'R'         : Reset newly added boxes")
    print("• Press 'S'         : Save changes to JSON file")
    print("• Press 'Q' or ESC  : Exit without saving\n")

    pan_step = 40  # Step speed for scroll bars when using arrow keys

    # OS Cross-Platform Extended Key Codes for Arrow Keys
    LEFT_KEYS = {2424832, 81, 65361, 0x250000}
    UP_KEYS = {2490368, 82, 65362, 0x260000}
    RIGHT_KEYS = {2555904, 83, 65363, 0x270000}
    DOWN_KEYS = {2621440, 84, 65364, 0x280000}

    while True:
        display_img = get_view_crop_with_scrollbars(temp_image)
        cv2.imshow(window_name, display_img)

        full_key = cv2.waitKeyEx(20)

        if full_key == -1:
            continue

        # 1. Handle Non-ASCII Arrow Keys FIRST to prevent collision with 'S' / 'A' / 'W' / 'D'
        if full_key in LEFT_KEYS:
            pan_x -= pan_step
            clamp_pan()
            continue
        elif full_key in RIGHT_KEYS:
            pan_x += pan_step
            clamp_pan()
            continue
        elif full_key in UP_KEYS:
            pan_y -= pan_step
            clamp_pan()
            continue
        elif full_key in DOWN_KEYS:
            pan_y += pan_step
            clamp_pan()
            continue

        # 2. Extract standard ASCII character key
        char_key = full_key & 0xFF

        # Exit ('Q' or ESC)
        if char_key in (ord("q"), ord("Q"), 27):
            print("\n❌ Exited without saving changes.")
            break

        # Save Changes ('S')
        elif char_key in (ord("s"), ord("S")):
            all_annotations = existing_boxes + new_yolo_boxes

            os.makedirs(os.path.dirname(FULL_ANNOTATION_PATH), exist_ok=True)
            with open(FULL_ANNOTATION_PATH, "w") as f:
                json.dump(all_annotations, f, indent=2)

            print(f"\n✅ SUCCESS! Updated file: '{FULL_ANNOTATION_PATH}'")
            print(f"   └─ Total Saved Annotations: {len(all_annotations)}")
            break

        # Undo Last Addition ('Z')
        elif char_key in (ord("z"), ord("Z")):
            if new_yolo_boxes:
                removed = new_yolo_boxes.pop()
                print(f"↩️ Undid box: {removed}")
                redraw_canvas()
            else:
                print("⚠️ No new boxes to undo.")

        # Reset Unsaved New Boxes ('R')
        elif char_key in (ord("r"), ord("R")):
            if new_yolo_boxes:
                new_yolo_boxes.clear()
                print("🔄 Reset all unsaved new boxes.")
                redraw_canvas()

        # Zoom Controls (+ / -)
        elif char_key in (ord("+"), ord("=")):
            zoom_scale = min(zoom_scale + 0.25, 5.0)
            clamp_pan()
        elif char_key in (ord("-"), ord("_")):
            zoom_scale = max(zoom_scale - 0.25, 1.0)
            clamp_pan()

        # WASD Panning
        elif char_key in (ord("a"), ord("A")):
            pan_x -= pan_step
            clamp_pan()
        elif char_key in (ord("d"), ord("D")):
            pan_x += pan_step
            clamp_pan()
        elif char_key in (ord("w"), ord("W")):
            pan_y -= pan_step
            clamp_pan()

    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    run_interactive_annotator()