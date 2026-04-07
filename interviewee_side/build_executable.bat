@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building the Standalone Application (.exe) for Windows...
echo This process might take 5-10 minutes depending on your CPU speed. Please do not close this window!
echo.

pyinstaller --name "AI_Hiring_Assistant" ^
            --console ^
            --noconfirm ^
            --clean ^
            --collect-all mediapipe ^
            --collect-all cv2 ^
            --hidden-import=cv2 ^
            --add-data "assets;assets" ^
            --add-data "src\.env;src" ^
            --add-data "data;data" ^
            main.py

echo.
echo.
echo Build Complete!
echo You can find your new standalone executable file at:
echo \dist\AI_Hiring_Assistant\AI_Hiring_Assistant.exe
pause
