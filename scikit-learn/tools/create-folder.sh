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

# Check if the 'scikit-learn' folder exists and create it if not
if [ ! -d "$ROOT/scikit-learn" ]; then
    mkdir "$ROOT/scikit-learn"
fi

# Create 'train', 'model', and 'test' folders inside 'scikit-learn' if they don't exist
[ ! -d "$ROOT/scikit-learn/train" ] && mkdir "$ROOT/scikit-learn/train"
[ ! -d "$ROOT/scikit-learn/model" ] && mkdir "$ROOT/scikit-learn/model"
[ ! -d "$ROOT/scikit-learn/test" ] && mkdir "$ROOT/scikit-learn/test"

echo "Directory structure created successfully."
