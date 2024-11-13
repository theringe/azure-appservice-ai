#!/bin/bash

ROOT="/mnt/data-and-model/scikit-learn/train"
ZIP_URL="https://archive.ics.uci.edu/static/public/45/heart+disease.zip"
ZIP_FILE="$ROOT/heart+disease.zip"
UNZIP_FOLDER="$ROOT/heart_disease"

# Step 1: Download the ZIP file if it does not already exist
if [ ! -f "$ZIP_FILE" ]; then
    echo "Downloading heart disease dataset..."
    wget -O "$ZIP_FILE" "$ZIP_URL"
else
    echo "ZIP file already exists, skipping download."
fi

# Step 2: Create the 'heart_disease' folder if it does not already exist
if [ ! -d "$UNZIP_FOLDER" ]; then
    echo "Creating heart_disease folder..."
    mkdir "$UNZIP_FOLDER"
else
    echo "Folder heart_disease already exists, skipping creation."
fi

# Step 3: Unzip files if they have not already been extracted
if [ -z "$(ls -A "$UNZIP_FOLDER")" ]; then
    echo "Unzipping files..."
    unzip "$ZIP_FILE" -d "$UNZIP_FOLDER"
else
    echo "Files already unzipped, skipping extraction."
fi

echo "Setup complete."
