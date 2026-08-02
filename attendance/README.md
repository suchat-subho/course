# Collect Student Attandance Using Image Map

## Folder Structure
```
attendance/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── frontend/                     # GitHub Pages website
│   │
│   ├── index.html                # Landing page
│   ├── annotate.html             # Annotation page
│   ├── dashboard.html            # Statistics & progress
│   ├── review.html               # Review completed annotations
│   │
│   ├── css/
│   │   ├── style.css
│   │   ├── toolbar.css
│   │   └── dashboard.css
│   │
│   ├── dataset/
│   │   │
│   │   ├── RawPicture/               # Original images (Never modify)
|   │   ├── 31_07_2026_2C7.jpg
|   │   │   ├── 31_07_2026_2C8.jpg
|   │   │   ├── 01_08_2026_2C7.jpg
|   │   │   └── manifest.json
|   │   │
|   │   ├── Annotated/                # Annotated preview images
|   │   │   ├── 31_07_2026_2C7_annotated.jpg
|   │   │   └── ...
|   │   │
|   │   ├── Labels/                   # Annotation JSON files
|   │   │   ├── 31_07_2026_2C7.json
|   │   │   ├── 31_07_2026_2C8.json
|   │   │   └── ...
|   │   │
|   │   ├── Export/
|   │   │   ├── YOLO/
|   │   │   ├── COCO/
|   │   │   ├── PascalVOC/
|   │   │   └── CSV/
|   │   │
│   │   └── Backup/
│   ├── js/
│   │   ├── app.js
│   │   ├── canvas.js
│   │   ├── annotation.js
│   │   ├── toolbar.js
│   │   ├── history.js
│   │   ├── detector.js
│   │   ├── api.js
│   │   ├── export.js
│   │   ├── shortcuts.js
│   │   └── utils.js
│   │
│   ├── icons/
│   ├── fonts/
│   └── models/
│       └── yolov11n.onnx
│
│
├── backend/
│   │
│   ├── GoogleAppsScript/
│   │   ├── Code.gs
│   │   ├── Config.gs
│   │   └── appsscript.json
│   │
│   └── Documentation/
│
├── docs/
│   ├── screenshots/
│   ├── workflow.md
│   └── api.md
│
└── tools/
    ├── generate_manifest.py
    ├── convert_to_yolo.py
    ├── convert_to_coco.py
    └── statistics.py
```
## Workflow
* After image uploding to `frontend/dataset/RawPicture/` 
```
bash ./tools/generate_manifest.sh
```  