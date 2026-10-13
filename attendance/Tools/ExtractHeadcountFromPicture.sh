#!/bin/bash

# Set target directory from the first argument, or default to current directory
DIR="${1:-.}"

echo "Scanning images in: $DIR"
echo "----------------------------------------"

# Loop through common image formats
for img in "$DIR"/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
    # Skip if no matching files exist
    [ -e "$img" ] || continue
    
    # Crop top-left corner and run OCR, suppressing stderr and removing extra newlines
    headcount=$(convert "$img" -crop 10%x4%+0+0 -negate -resize 300% - | tesseract stdin stdout --psm 7 2>/dev/null | tr -d '\r\n')
    
    # Print the result
    echo "File: $(basename "$img") | Result: $headcount"
done

echo "----------------------------------------"
echo "Done!"
