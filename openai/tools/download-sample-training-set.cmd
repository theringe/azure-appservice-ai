@echo off
set "ROOT=Z:\openai\train"
set "ZIP_URL=https://github.com/rishabhmisra/News-Headlines-Dataset-For-Sarcasm-Detection/archive/refs/heads/master.zip"
set "ZIP_FILE=%ROOT%\headlines.zip"
set "UNZIP_FOLDER=%ROOT%\headlines"

REM Step 1: Download the ZIP file if it does not already exist
if not exist "%ZIP_FILE%" (
    echo Downloading headlines dataset...
    powershell -command "Invoke-WebRequest -Uri %ZIP_URL% -OutFile %ZIP_FILE%"
) else (
    echo ZIP file already exists, skipping download.
)

REM Step 2: Create the 'headlines' folder if it does not already exist
if not exist "%UNZIP_FOLDER%" (
    echo Creating headlines folder...
    mkdir "%UNZIP_FOLDER%"
) else (
    echo Folder headlines already exists, skipping creation.
)

REM Step 3: Unzip files if they have not already been extracted
REM We check if the 'headlines' folder is empty before unzipping
for %%f in ("%UNZIP_FOLDER%\*") do (
    if exist "%%f" (
        echo Files already unzipped, skipping extraction.
        goto :EOF
    )
)

REM Using PowerShell to unzip (if the folder was empty)
echo Unzipping files...
powershell -ExecutionPolicy Bypass -command "Expand-Archive -Path %ZIP_FILE% -DestinationPath %UNZIP_FOLDER% -Force"

echo Setup complete.
