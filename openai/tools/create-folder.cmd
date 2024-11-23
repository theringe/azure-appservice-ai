@echo off
REM Set the root folder
set "ROOT=Z:\"

REM Check if the root folder exists
if not exist "%ROOT%" (
    echo Root folder %ROOT% does not exist.
    exit /b 1
)

REM Check if the 'openai' folder exists and create it if not
if not exist "%ROOT%openai\" (
    mkdir "%ROOT%openai"
)

REM Create 'train', 'model', and 'test' folders inside 'openai' if they don't exist
if not exist "%ROOT%openai\train" (
    mkdir "%ROOT%openai\train"
)
if not exist "%ROOT%openai\model" (
    mkdir "%ROOT%openai\model"
)
if not exist "%ROOT%openai\test" (
    mkdir "%ROOT%openai\test"
)

echo Directory structure created successfully.
