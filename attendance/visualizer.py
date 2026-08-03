import cv2
import numpy as np

# Define class label name
CLASS_NAME = "Student"
DATASET_PATH=""
ImageName="31_07_2026_2C7.jpg"

# YOLO annotations provided previously

annotations_data = {
    "1000060381.jpg": [
        "0 0.237 0.693 0.106 0.380", "0 0.056 0.428 0.111 0.211", "0 0.099 0.392 0.052 0.134",
        "0 0.153 0.413 0.052 0.129", "0 0.207 0.431 0.059 0.150", "0 0.274 0.548 0.047 0.153",
        "0 0.485 0.589 0.068 0.211", "0 0.561 0.528 0.068 0.183", "0 0.630 0.627 0.076 0.228",
        "0 0.697 0.612 0.082 0.163", "0 0.736 0.575 0.058 0.136", "0 0.763 0.545 0.052 0.120",
        "0 0.803 0.529 0.050 0.108", "0 0.461 0.518 0.052 0.136", "0 0.508 0.482 0.043 0.102",
        "0 0.536 0.470 0.038 0.088", "0 0.603 0.482 0.038 0.099", "0 0.666 0.512 0.044 0.117",
        "0 0.697 0.500 0.035 0.079", "0 0.455 0.412 0.048 0.124", "0 0.428 0.443 0.047 0.112",
        "0 0.425 0.354 0.039 0.111", "0 0.403 0.358 0.035 0.091", "0 0.380 0.334 0.035 0.088",
        "0 0.129 0.324 0.030 0.082", "0 0.171 0.258 0.026 0.058", "0 0.203 0.271 0.028 0.062",
        "0 0.229 0.315 0.030 0.068", "0 0.267 0.327 0.035 0.071", "0 0.215 0.239 0.023 0.056",
        "0 0.245 0.246 0.024 0.058", "0 0.267 0.255 0.026 0.058", "0 0.278 0.268 0.023 0.056",
        "0 0.386 0.265 0.024 0.053", "0 0.420 0.273 0.023 0.055", "0 0.439 0.266 0.023 0.052",
        "0 0.450 0.316 0.026 0.068", "0 0.482 0.329 0.026 0.062", "0 0.505 0.373 0.025 0.065",
        "0 0.536 0.384 0.028 0.068", "0 0.568 0.398 0.028 0.068", "0 0.598 0.417 0.028 0.069",
        "0 0.627 0.425 0.028 0.068", "0 0.647 0.428 0.026 0.062", "0 0.666 0.422 0.024 0.058",
        "0 0.686 0.429 0.022 0.055", "0 0.700 0.429 0.020 0.050", "0 0.720 0.426 0.019 0.048",
        "0 0.736 0.425 0.018 0.045", "0 0.817 0.502 0.040 0.088", "0 0.835 0.493 0.032 0.075",
        "0 0.880 0.455 0.032 0.062"
    ],
    "1000060224.jpg": [
        "0 0.324 0.638 0.123 0.270", "0 0.434 0.638 0.117 0.203", "0 0.092 0.506 0.113 0.207",
        "0 0.670 0.589 0.110 0.224", "0 0.748 0.537 0.075 0.126", "0 0.816 0.511 0.050 0.096",
        "0 0.602 0.491 0.058 0.136", "0 0.642 0.485 0.048 0.108", "0 0.688 0.468 0.042 0.098",
        "0 0.499 0.491 0.066 0.158", "0 0.534 0.408 0.044 0.084", "0 0.575 0.461 0.042 0.082",
        "0 0.598 0.488 0.051 0.110", "0 0.301 0.466 0.068 0.110", "0 0.228 0.401 0.049 0.068",
        "0 0.283 0.401 0.046 0.071", "0 0.163 0.339 0.051 0.080", "0 0.212 0.344 0.048 0.071",
        "0 0.398 0.362 0.043 0.062", "0 0.439 0.365 0.038 0.058", "0 0.532 0.398 0.044 0.075",
        "0 0.402 0.329 0.035 0.068", "0 0.442 0.328 0.031 0.058", "0 0.466 0.341 0.030 0.058",
        "0 0.377 0.345 0.038 0.075", "0 0.380 0.305 0.030 0.055", "0 0.420 0.324 0.028 0.050",
        "0 0.485 0.408 0.046 0.065", "0 0.123 0.308 0.038 0.058", "0 0.153 0.308 0.032 0.055",
        "0 0.198 0.292 0.030 0.052", "0 0.247 0.318 0.032 0.058", "0 0.226 0.260 0.023 0.045",
        "0 0.195 0.261 0.021 0.045", "0 0.160 0.260 0.023 0.045", "0 0.128 0.260 0.021 0.045",
        "0 0.485 0.362 0.028 0.050", "0 0.505 0.354 0.026 0.048", "0 0.560 0.373 0.026 0.048",
        "0 0.627 0.381 0.025 0.048", "0 0.665 0.395 0.025 0.048", "0 0.725 0.410 0.025 0.048",
        "0 0.750 0.413 0.024 0.045", "0 0.771 0.420 0.022 0.042", "0 0.816 0.435 0.020 0.038",
        "0 0.838 0.440 0.020 0.038", "0 0.865 0.448 0.020 0.038"
    ]
}

def draw_yolo_boxes(img_path, annotations):
    # Load image
    image = cv2.imread(img_path)
    if image is None:
        print(f"Error: Could not load image {img_path}. Make sure it's in the current folder.")
        return
        
    img_h, img_w, _ = image.shape
    
    # Draw each box and label
    for idx, line in enumerate(annotations, start=1):
        parts = line.strip().split()
        _, x_center, y_center, width, height = map(float, parts)
        
        # Convert normalized YOLO format back to pixel coordinates
        x1 = int((x_center - width / 2) * img_w)
        y1 = int((y_center - height / 2) * img_h)
        x2 = int((x_center + width / 2) * img_w)
        y2 = int((y_center + height / 2) * img_h)
        
        # Bounding Box Styling (Bright Green, thickness 2)
        color = (0, 255, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # Serial Number / Headcount Label Styling
        label = f"#{idx}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        font_thickness = 1
        
        # Get label size for background box
        (label_w, label_h), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
        
        # Draw small background box for label readability
        cv2.rectangle(image, (x1, y1 - label_h - 4), (x1 + label_w, y1), color, -1)
        # Draw Serial Number Text in Black
        cv2.putText(image, label, (x1, y1 - 2), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

    # Add Total Count Overlay Banner at the Top-Left Corner
    total_count = len(annotations)
    banner_text = f"Total Headcount: {total_count}"
    cv2.rectangle(image, (10, 10), (320, 50), (0, 0, 0), -1)
    cv2.putText(image, banner_text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save output image
    output_path = f"annotated_{img_path}"
    cv2.imwrite(output_path, image)
    print(f"✅ Processed '{img_path}': Total Students = {total_count} | Saved output to '{output_path}'")

# Run through both images
if __name__ == "__main__":
    for img_file, lines in annotations_data.items():
        draw_yolo_boxes(img_file, lines)