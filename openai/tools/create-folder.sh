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

# Check if the 'openai' folder exists and create it if not
if [ ! -d "$ROOT/openai" ]; then
    mkdir "$ROOT/openai"
fi

# Create 'train', 'model', and 'test' folders inside 'openai' if they don't exist
[ ! -d "$ROOT/openai/train" ] && mkdir "$ROOT/openai/train"
[ ! -d "$ROOT/openai/model" ] && mkdir "$ROOT/openai/model"
[ ! -d "$ROOT/openai/test" ] && mkdir "$ROOT/openai/test"

echo "Directory structure created successfully."
