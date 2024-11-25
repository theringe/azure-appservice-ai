#!/bin/bash

# Ensure any active virtual environment is deactivated
deactivate 2>/dev/null || true  # Quietly deactivate, ignore errors if no virtual environment is active

# Remove any existing virtual environment directory to avoid conflicts
rm -rf /home/.venv

ROOT="/home/site/wwwroot"
VENV_ROOT="/home/.venv"

# Get the current epoch time as the new folder name
CURRENT_EPOCH=$(date +%s)
NEW_VENV_FOLDER="$VENV_ROOT/$CURRENT_EPOCH"

# Create a new folder based on the current epoch time
mkdir -p "$NEW_VENV_FOLDER"

# Create two virtual environments in the new folder and install requirements
for env in tensorflow-webjob tensorflow; do
    VENV_PATH="$NEW_VENV_FOLDER/$env"
    python -m venv $VENV_PATH
    source $VENV_PATH/bin/activate
    requirements="$ROOT/requirements.txt"
    [ "$env" == "tensorflow-webjob" ] && requirements="$ROOT/webjob/requirements.txt"
    $VENV_PATH/bin/pip install -r $requirements
    deactivate
done

# Start the application using the new tensorflow virtual environment
source $NEW_VENV_FOLDER/tensorflow/bin/activate
$NEW_VENV_FOLDER/tensorflow/bin/python $ROOT/api/app.py
