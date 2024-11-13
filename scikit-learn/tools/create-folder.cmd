@echo off
REM Set the root folder
set "ROOT=Z:\"

REM Check if the root folder exists
if not exist "%ROOT%" (
    echo Root folder %ROOT% does not exist.
    exit /b 1
)

REM Check if the 'scikit-learn' folder exists and create it if not
if not exist "%ROOT%scikit-learn\" (
    mkdir "%ROOT%scikit-learn"
)

REM Create 'train', 'model', and 'test' folders inside 'scikit-learn' if they don't exist
if not exist "%ROOT%scikit-learn\train" (
    mkdir "%ROOT%scikit-learn\train"
)
if not exist "%ROOT%scikit-learn\model" (
    mkdir "%ROOT%scikit-learn\model"
)
if not exist "%ROOT%scikit-learn\test" (
    mkdir "%ROOT%scikit-learn\test"
)

echo Directory structure created successfully.
