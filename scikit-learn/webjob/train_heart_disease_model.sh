#!/bin/bash

# Shell and Zip files are only for Azure WebJobs
# Every change in this script requires a new zip file to be uploaded to the Azure portal

# Initialize the PATH variable
export PATH=$PATH:/bin:/usr/bin:/usr/local/bin

# Base directory for virtual environments
VENV_BASE="/home/.venv"

# Find the latest (largest) epoch folder
LATEST_EPOCH=$(ls -1d $VENV_BASE/* | sort -n | tail -1)

# Check if a valid epoch folder exists
if [ -z "$LATEST_EPOCH" ] || [ ! -d "$LATEST_EPOCH/scikit-learn-webjob" ]; then
    echo "No valid virtual environment found in $VENV_BASE."
    exit 1
fi

# Activate the virtual environment
VENV_PATH="$LATEST_EPOCH/scikit-learn-webjob"
source "$VENV_PATH/bin/activate"

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Failed to activate virtual environment at $VENV_PATH."
    exit 1
fi

echo "Activated virtual environment: $VENV_PATH"

# Run the Python script
python /home/site/wwwroot/webjob/train_heart_disease_model.py

# Deactivate the virtual environment
deactivate

echo "Script execution completed."
