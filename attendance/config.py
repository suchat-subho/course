import os

IMAGE_NAME = "30_07_2026_2C7"


# ==========================================
# 🌐 GLOBAL CONFIGURATION & PATHS
# ==========================================

# Directory Paths
IMAGE_PATH = "Dataset/RawPicture/"
ANNOTATION_PATH = "Dataset/Annotated/"
AUGMENTED_IMAGE_PATH = "Dataset/Augmented/Images/"
AUGMENTED_ANNOTATION_PATH = "Dataset/Augmented/"
PREVIEW_PATH="Dataset/Preview/"

# Default Target File
IMAGE_EXTN = ".jpg"

# Processing & Cleanup Parameters
IOU_THRESHOLD = 0.45
ROW_TOLERANCE = 0.08


# ==========================================
# 🛠️ DYNAMIC PATH HELPER FUNCTIONS
# ==========================================

def get_image_path(img_name=None):
    """Returns full path for the raw image."""
    name = img_name if img_name else IMAGE_NAME
    return os.path.join(IMAGE_PATH, f"{name}{IMAGE_EXTN}")


def get_annotation_path(img_name=None):
    """Returns full path for the JSON annotation file."""
    name = img_name if img_name else IMAGE_NAME
    return os.path.join(ANNOTATION_PATH, f"{name}.json")


def get_annotated_output_path(img_name=None):
    """Returns full path for saving the rendered image with drawn boxes."""
    name = img_name if img_name else IMAGE_NAME
    return os.path.join(ANNOTATION_PATH, f"{name}{IMAGE_EXTN}")
