import os
import json
import shutil
import random
from pathlib import Path
from ultralytics import YOLO

def prepare_yolo_dataset(raw_images_dir, annotations_dir, dataset_root, val_split=0.15):
    """
    Parses JSON files containing YOLO string annotations and organizes
    images and labels into train/val folders required by Ultralytics YOLO.
    """
    raw_images_dir = Path(raw_images_dir)
    annotations_dir = Path(annotations_dir)
    dataset_root = Path(dataset_root)

    # Define YOLO structure paths
    train_img_dir = dataset_root / "train" / "images"
    train_lbl_dir = dataset_root / "train" / "labels"
    val_img_dir = dataset_root / "val" / "images"
    val_lbl_dir = dataset_root / "val" / "labels"

    # Create directories
    for d in [train_img_dir, train_lbl_dir, val_img_dir, val_lbl_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Gather matching image and JSON pairs
    image_files = list(raw_images_dir.glob("*.jpg")) + list(raw_images_dir.glob("*.jpeg"))
    valid_pairs = []

    for img_path in image_files:
        json_path = annotations_dir / f"{img_path.stem}.json"
        if json_path.exists():
            valid_pairs.append((img_path, json_path))
        else:
            print(f"Warning: Annotation missing for {img_path.name}")

    if not valid_pairs:
        raise FileNotFoundError("No matching image and JSON pairs were found.")

    # Shuffle and split into train / val
    random.shuffle(valid_pairs)
    val_count = int(len(valid_pairs) * val_split)
    val_pairs = valid_pairs[:val_count]
    train_pairs = valid_pairs[val_count:]

    def copy_and_process(pairs, target_img_dir, target_lbl_dir):
        for img_path, json_path in pairs:
            # 1. Copy image file
            shutil.copy(img_path, target_img_dir / img_path.name)

            # 2. Read JSON array and write plain YOLO text file (.txt)
            with open(json_path, 'r') as f:
                yolo_lines = json.load(f)

            txt_path = target_lbl_dir / f"{img_path.stem}.txt"
            with open(txt_path, 'w') as f:
                f.write("\n".join(yolo_lines))

    print(f"Processing {len(train_pairs)} training samples and {len(val_pairs)} validation samples...")
    copy_and_process(train_pairs, train_img_dir, train_lbl_dir)
    copy_and_process(val_pairs, val_img_dir, val_lbl_dir)

    # Create data.yaml
    yaml_content = f"""path: {dataset_root.resolve()}
train: train/images
val: val/images

names:
  0: student_face
"""
    yaml_path = dataset_root / "data.yaml"
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)

    print(f"Dataset successfully prepared at: {dataset_root.resolve()}")
    return yaml_path.resolve()

def train_yolo():
    # Relative paths specified in your query
    RAW_IMAGES = "../../Dataset/RawPicture"
    ANNOTATIONS = "../../Dataset/Annotated"
    PROCESSED_DATASET = "../../Dataset/YOLO_Formatted"

    # Step 1: Format dataset and generate data.yaml
    data_yaml_path = prepare_yolo_dataset(
        raw_images_dir=RAW_IMAGES,
        annotations_dir=ANNOTATIONS,
        dataset_root=PROCESSED_DATASET,
        val_split=0.15  # 15% used for validation during training
    )

    # Step 2: Load pretrained YOLO model and start training
    model = YOLO("yolo11n.pt")  # Lightweight baseline model

    print("\nStarting YOLO Training...")
    results = model.train(
        data=str(data_yaml_path),
        epochs=100,
        imgsz=640,
        batch=16,
        project="student_face_detection",
        name="experiment_1",
        exist_ok=True,
        pretrained=True
    )

    print("\nTraining Complete!")
    print(f"Trained model saved to: {results.save_dir}/weights/best.pt")

if __name__ == "__main__":
    train_yolo()