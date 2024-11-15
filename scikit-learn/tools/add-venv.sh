#!/bin/bash

# Set the root directory of the project
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_ROOT="$ROOT/.venv"

# Create the .venv directory if it doesn't exist
mkdir -p "$VENV_ROOT"

# Create and set up virtual environments for scikit-learn-webjob and scikit-learn
for env in scikit-learn-webjob scikit-learn; do
    VENV_PATH="$VENV_ROOT/$env"
    if [ ! -d "$VENV_PATH" ]; then
        python -m venv "$VENV_PATH"
        source "$VENV_PATH/bin/activate"
        requirements="$ROOT/scikit-learn/requirements.txt"
        [ "$env" == "scikit-learn-webjob" ] && requirements="$ROOT/scikit-learn/webjob/requirements.txt"
        "$VENV_PATH/bin/pip" install -r "$requirements"
        deactivate
    fi
done

echo "Virtual environments created successfully in $VENV_ROOT"
