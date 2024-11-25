#!/bin/bash

# Detect OS and set ROOT accordingly
if [[ "$(uname)" == "Darwin" ]]; then
    ROOT="/Volumes/data-and-model"
else
    ROOT="/mnt/data-and-model"
fi

# Check if the root folder exists
if [ ! -d "$ROOT" ]; then
    echo "Root folder $ROOT does not exist."
    exit 1
fi

# Check if the 'tensorflow' folder exists and create it if not
if [ ! -d "$ROOT/tensorflow" ]; then
    mkdir "$ROOT/tensorflow"
fi

# Create 'train', 'model', and 'test' folders inside 'tensorflow' if they don't exist
[ ! -d "$ROOT/tensorflow/train" ] && mkdir "$ROOT/tensorflow/train"
[ ! -d "$ROOT/tensorflow/model" ] && mkdir "$ROOT/tensorflow/model"
[ ! -d "$ROOT/tensorflow/test" ] && mkdir "$ROOT/tensorflow/test"

echo "Directory structure created successfully."
