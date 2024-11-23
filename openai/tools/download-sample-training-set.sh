#!/bin/bash

# Detect OS and set ROOT accordingly
if [[ "$(uname)" == "Darwin" ]]; then
    ROOT="/Volumes/data-and-model/openai/train"
else
    ROOT="/mnt/data-and-model/openai/train"
fi

ZIP_URL="https://github.com/rishabhmisra/News-Headlines-Dataset-For-Sarcasm-Detection/archive/refs/heads/master.zip"
ZIP_FILE="$ROOT/headlines.zip"
UNZIP_FOLDER="$ROOT/headlines"
TMP_DIR="/tmp/headlines"

# Step 1: Download the ZIP file if it does not already exist
if [ ! -f "$ZIP_FILE" ]; then
    echo "Downloading heart disease dataset..."
    wget -O "$ZIP_FILE" "$ZIP_URL"
else
    echo "ZIP file already exists, skipping download."
fi

# Step 2: Create the 'headlines' folder if it does not already exist
if [ ! -d "$UNZIP_FOLDER" ]; then
    echo "Creating headlines folder..."
    mkdir "$UNZIP_FOLDER"
else
    echo "Folder headlines already exists, skipping creation."
fi

# Step 3: Unzip to a temporary local folder, then copy files using rsync
if [ -z "$(ls -A "$UNZIP_FOLDER")" ]; then
    echo "Unzipping files to temporary directory..."
    mkdir -p "$TMP_DIR"
    unzip "$ZIP_FILE" -d "$TMP_DIR"
    echo "Copying files to the target directory without preserving permissions or timestamps..."
    rsync -a --no-perms --no-owner --no-group --no-times "$TMP_DIR"/ "$UNZIP_FOLDER"/
    rm -r "$TMP_DIR"
else
    echo "Files already unzipped, skipping extraction."
fi

echo "Setup complete."
