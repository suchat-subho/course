import json
import os
import cv2
import config

# ==========================================
# 🌐 CONFIGURATION & PATH SETUP
# ==========================================
IMAGE_PATH = getattr(config, "IMAGE_PATH", "Dataset/RawPicture/")
ANNOTATION_PATH = getattr(config, "ANNOTATION_PATH", "Dataset/Annotated/")
IMAGE_EXTN = getattr(config, "IMAGE_EXTN", ".jpg")
ImageName = getattr(config, "IMAGE_NAME", "")

# Safely construct Full Paths
if hasattr(config, "get_image_path"):
    FULL_IMAGE_PATH = config.get_image_path(ImageName)
else:
    FULL_IMAGE_PATH = os.path.join(IMAGE_PATH, ImageName + IMAGE_EXTN)

if hasattr(config, "get_annotation_path"):
    FULL_ANNOTATION_PATH = config.get_annotation_path(ImageName)
else:
    FULL_ANNOTATION_PATH = os.path.join(ANNOTATION_PATH, ImageName + ".json")

# Global tracking variables
drawing = False
ix, iy = -1, -1
temp_image = None
current_image = None
base_annotated_image = None  # Preserves base layer with green existing boxes
new_yolo_boxes = []  # Holds new annotations to write to JSON


def load_existing_annotations(json_path):
    """Loads existing annotations from JSON file."""
    if not os.path.exists(json_path):
        print(f"⚠️ Notice: '{json_path}' not found. A new file will be created on save.")
        return []

    with open(json_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = data.get("annotations", data.get("labels", []))

    return data


def redraw_canvas():
    """Redraws all newly queued boxes on top of the base image."""
    global current_image, temp_image, base_annotated_image, new_yolo_boxes

    current_image = base_annotated_image.copy()
    img_h, img_w, _ = current_image.shape

    for idx, box_str in enumerate(new_yolo_boxes, start=1):
        parts = box_str.strip().split()
        _, x_center, y_center, width, height = map(float, parts[:5])

        x1 = int((x_center - width / 2) * img_w)
        y1 = int((y_center - height / 2) * img_h)
        x2 = int((x_center + width / 2) * img_w)
        y2 = int((y_center + height / 2) * img_h)

        cv2.rectangle(current_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            current_image,
            f"NEW #{idx}",
            (x1, max(y1 - 5, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    temp_image = current_image.copy()


def draw_mouse_bbox(event, x, y, flags, param):
    """Mouse callback to handle click-and-drag drawing."""
    global ix, iy, drawing, temp_image, current_image, new_yolo_boxes

    img_h, img_w, _ = current_image.shape

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_image = current_image.copy()
            cv2.rectangle(temp_image, (ix, iy), (x, y), (0, 0, 255), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            x1, y1 = min(ix, x), min(iy, y)
            x2, y2 = max(ix, x), max(iy, y)

            # Ignore tiny accidental clicks (less than 5 pixels)
            if (x2 - x1) > 5 and (y2 - y1) > 5:
                # Convert pixel coordinates to normalized YOLO format
                width = (x2 - x1) / img_w
                height = (y2 - y1) / img_h
                x_center = (x1 + (x2 - x1) / 2) / img_w
                y_center = (y1 + (y2 - y1) / 2) / img_h

                # Format YOLO string: "class_id x_center y_center width height"
                yolo_str = f"0 {x_center:.4f} {y_center:.4f} {width:.4f} {height:.4f}"

                # Store in list to be written into JSON upon saving
                new_yolo_boxes.append(yolo_str)
                print(f"➕ Queued New Box #{len(new_yolo_boxes)}: {yolo_str}")

                redraw_canvas()


def run_interactive_annotator():
    global current_image, temp_image, base_annotated_image, new_yolo_boxes

    # 1. Load Raw Image
    image = cv2.imread(FULL_IMAGE_PATH)
    if image is None:
        print(f"❌ Error: Could not open image at '{FULL_IMAGE_PATH}'")
        return

    img_h, img_w, _ = image.shape
    base_annotated_image = image.copy()

    # 2. Load existing JSON annotations & render them in GREEN
    existing_annotations = load_existing_annotations(FULL_ANNOTATION_PATH)
    for idx, item in enumerate(existing_annotations, start=1):
        if isinstance(item, str):
            parts = item.strip().split()
            if len(parts) < 5:
                continue
            _, x_center, y_center, width, height = map(float, parts[:5])
        elif isinstance(item, dict):
            bbox = item.get("bbox", [])
            if len(bbox) == 4:
                x_center, y_center, width, height = map(float, bbox)
            else:
                continue
        else:
            continue

        x1 = int((x_center - width / 2) * img_w)
        y1 = int((y_center - height / 2) * img_h)
        x2 = int((x_center + width / 2) * img_w)
        y2 = int((y_center + height / 2) * img_h)

        cv2.rectangle(base_annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            base_annotated_image,
            f"#{idx}",
            (x1, max(y1 - 5, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

    current_image = base_annotated_image.copy()
    temp_image = current_image.copy()

    # 3. Setup OpenCV Window & Controls
    window_name = "Interactive Annotator | 'S': Save | 'Z': Undo | 'R': Reset | 'Q': Quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, draw_mouse_bbox)

    print("\n--- 🖱️ INSTRUCTIONS ---")
    print("1. Click & drag mouse over missing student faces.")
    print("2. Press 'Z' to Undo last drawn box.")
    print("3. Press 'R' to Reset all newly added boxes.")
    print("4. Press 'S' to Save & Append to JSON file.")
    print("5. Press 'Q' or 'ESC' to Exit without saving.\n")

    while True:
        cv2.imshow(window_name, temp_image)
        key = cv2.waitKey(20) & 0xFF

        # Press 'S' to Save
        if key == ord("s") or key == ord("S"):
            if new_yolo_boxes:
                updated_annotations = existing_annotations + new_yolo_boxes

                os.makedirs(os.path.dirname(FULL_ANNOTATION_PATH), exist_ok=True)

                with open(FULL_ANNOTATION_PATH, "w") as f:
                    json.dump(updated_annotations, f, indent=2)

                print(f"\n✅ SUCCESS! Updated '{FULL_ANNOTATION_PATH}'")
                print(f"   ├─ Added {len(new_yolo_boxes)} new box(es)")
                print(f"   └─ Total annotations in JSON: {len(updated_annotations)}")
            else:
                print("\n⚠️ No new boxes added. JSON file remains unchanged.")
            break

        # Press 'Z' to Undo last drawn box
        elif key == ord("z") or key == ord("Z"):
            if new_yolo_boxes:
                removed = new_yolo_boxes.pop()
                print(f"↩️ Undid box: {removed}")
                redraw_canvas()
            else:
                print("⚠️ Nothing to undo.")

        # Press 'R' to Reset all unsaved boxes
        elif key == ord("r") or key == ord("R"):
            if new_yolo_boxes:
                new_yolo_boxes.clear()
                print("🔄 Reset all unsaved boxes.")
                redraw_canvas()

        # Press 'Q' or ESC to Quit without saving
        elif key == ord("q") or key == ord("Q") or key == 27:
            print("\n❌ Exited without saving changes.")
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    run_interactive_annotator()