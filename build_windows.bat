@echo off
echo Windows Installer Build Script
echo ==============================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)

:: Create/Activate venv
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller pillow

:: Get CustomTkinter path for data inclusion
for /f "delims=" %%i in ('python -c "import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))"') do set CTK_PATH=%%i

echo CustomTkinter path: %CTK_PATH%

:: Build EXE
echo Building EXE...
pyinstaller --noconfirm --onefile --windowed --icon "ytdown.png" --name "YTDownMP3" --add-data "%CTK_PATH%;customtkinter" --add-data "localization.py;." main.py

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b
)

echo.
echo Build successful! The executable is in the 'dist' folder.
echo You can rename 'dist\YTDownMP3.exe' to whatever you like.
echo.
pause