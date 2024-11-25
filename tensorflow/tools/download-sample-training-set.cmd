@echo off
set "ROOT=Z:\tensorflow\train"
set "ZIP_URL=https://github.com/Neoanarika/MBTI/archive/refs/heads/master.zip"
set "ZIP_FILE=%ROOT%\mbti.zip"
set "UNZIP_FOLDER=%ROOT%\mbti"

REM Step 1: Download the ZIP file if it does not already exist
if not exist "%ZIP_FILE%" (
    echo Downloading mbti dataset...
    powershell -command "Invoke-WebRequest -Uri %ZIP_URL% -OutFile %ZIP_FILE%"
) else (
    echo ZIP file already exists, skipping download.
)

REM Step 2: Create the 'mbti' folder if it does not already exist
if not exist "%UNZIP_FOLDER%" (
    echo Creating mbti folder...
    mkdir "%UNZIP_FOLDER%"
) else (
    echo Folder mbti already exists, skipping creation.
)

REM Step 3: Unzip files if they have not already been extracted
REM We check if the 'mbti' folder is empty before unzipping
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
