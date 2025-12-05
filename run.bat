@echo off
echo YT Audio Converter Pro inditasa...

:: Ellenorizzuk, hogy letezik-e a virtualis kornyezet
if not exist .venv (
    echo Virtualis kornyezet letrehozasa...
    python -m venv .venv
)

:: Aktivaljuk a kornyezetet es telepitjuk a fuggosegeket
call .venv\Scripts\activate.bat
echo Fuggosegek ellenorzese...
pip install -r requirements.txt

:: Program inditasa
echo Program inditasa...
python main.py
pause