import argparse
import json
from pathlib import Path
from ultralytics import YOLO

def annotate_image_to_json(model_path, image_path, output_json_path, conf_threshold=0.25):
    # Load trained YOLO model
    model = YOLO(model_path)

    # Run inference
    results = model.predict(source=str(image_path), conf=conf_threshold, verbose=False)

    annotation_lines = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0].item())
            x_center, y_center, w, h = box.xywhn[0].tolist()
            
            # Format to 4 decimal places
            line = f"{cls_id} {x_center:.4f} {y_center:.4f} {w:.4f} {h:.4f}"
            annotation_lines.append(line)

    # Ensure output directory exists
    output_json_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to JSON
    with open(output_json_path, 'w') as f:
        json.dump(annotation_lines, f, indent=2)

    print(f"Successfully generated: {output_json_path}")
    print(f"Total faces detected: {len(annotation_lines)}")

def main():
    parser = argparse.ArgumentParser(
        description="Annotate an image using a trained YOLO model and export predictions to JSON format."
    )
    
    # Command-line arguments
    parser.add_argument(
        "-i", "--input", 
        type=Path, 
        required=True, 
        help="Path to the input image file."
    )
    parser.add_argument(
        "-o", "--output", 
        type=Path, 
        default=None, 
        help="Path for output JSON file (default: saved to ../../Dataset/Annotated/<image_name>.json)."
    )
    parser.add_argument(
        "-m", "--model", 
        type=str, 
        default="student_face_detection/experiment_1/weights/best.pt", 
        help="Path to trained YOLO model weights."
    )
    parser.add_argument(
        "-c", "--conf", 
        type=float, 
        default=0.30, 
        help="Confidence threshold for detection (0.0 to 1.0)."
    )

    args = parser.parse_args()

    # Determine default output JSON path if not provided
    if args.output is None:
        args.output = Path(f"../../Dataset/Annotated/{args.input.stem}.json")

    annotate_image_to_json(
        model_path=args.model,
        image_path=args.input,
        output_json_path=args.output,
        conf_threshold=args.conf
    )

if __name__ == "__main__":
    main()