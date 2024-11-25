@echo off
setlocal enabledelayedexpansion

REM Set the root directory of the project and virtual environment root
set "ROOT=%~dp0\..\.."
set "VENV_ROOT=%ROOT%\.venv"

REM Normalize the root path to remove trailing backslashes
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
for %%I in ("%VENV_ROOT%") do set "VENV_ROOT=%%~fI"

REM Create the .venv directory if it doesn't exist
if not exist "%VENV_ROOT%" (
    mkdir "%VENV_ROOT%"
)

REM Create and set up virtual environments for tensorflow-webjob and tensorflow
for %%E in (tensorflow-webjob tensorflow) do (
    set "VENV_NAME=%%E"
    set "VENV_PATH=%VENV_ROOT%\!VENV_NAME!"
    
    REM Create the virtual environment folder if it doesn't exist
    if not exist "!VENV_PATH!" (
        python -m venv "!VENV_PATH!"
        
        REM Check if the environment was created successfully before proceeding
        if exist "!VENV_PATH!\Scripts\activate.bat" (
            REM Activate the virtual environment
            call "!VENV_PATH!\Scripts\activate.bat"
            
            REM Install requirements based on the environment
            if "!VENV_NAME!"=="tensorflow-webjob" (
                "!VENV_PATH!\Scripts\pip" install -r "!ROOT!\tensorflow\webjob\requirements.txt"
            ) else (
                "!VENV_PATH!\Scripts\pip" install -r "!ROOT!\tensorflow\requirements.txt"
            )
            
            REM Deactivate the virtual environment
            call "!VENV_PATH!\Scripts\deactivate.bat" 2>NUL
        ) else (
            echo Failed to create virtual environment in "!VENV_PATH!"
        )
    ) else (
        echo Virtual environment already exists at "!VENV_PATH!"
    )
)

endlocal
echo Virtual environments created successfully in %VENV_ROOT%
