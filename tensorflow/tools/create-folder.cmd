@echo off
REM Set the root folder
set "ROOT=Z:\"

REM Check if the root folder exists
if not exist "%ROOT%" (
    echo Root folder %ROOT% does not exist.
    exit /b 1
)

REM Check if the 'tensorflow' folder exists and create it if not
if not exist "%ROOT%tensorflow\" (
    mkdir "%ROOT%tensorflow"
)

REM Create 'train', 'model', and 'test' folders inside 'tensorflow' if they don't exist
if not exist "%ROOT%tensorflow\train" (
    mkdir "%ROOT%tensorflow\train"
)
if not exist "%ROOT%tensorflow\model" (
    mkdir "%ROOT%tensorflow\model"
)
if not exist "%ROOT%tensorflow\test" (
    mkdir "%ROOT%tensorflow\test"
)

echo Directory structure created successfully.
