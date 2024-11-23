#!/bin/bash

# Set the root directory of the project
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_ROOT="$ROOT/.venv"

# Create the .venv directory if it doesn't exist
mkdir -p "$VENV_ROOT"

# Create and set up virtual environments for openai-webjob and openai
for env in openai-webjob openai; do
    VENV_PATH="$VENV_ROOT/$env"
    if [ ! -d "$VENV_PATH" ]; then
        python -m venv "$VENV_PATH"
        source "$VENV_PATH/bin/activate"
        requirements="$ROOT/openai/requirements.txt"
        [ "$env" == "openai-webjob" ] && requirements="$ROOT/openai/webjob/requirements.txt"
        "$VENV_PATH/bin/pip" install -r "$requirements"
        deactivate
    fi
done

echo "Virtual environments created successfully in $VENV_ROOT"
