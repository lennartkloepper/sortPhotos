@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Photo Sorter - EXE Builder
echo ========================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Creating EXE file...
echo.

REM Create the EXE
pyinstaller --onefile --windowed --icon=NONE --name="PhotoSorter" photo_sorter.py

echo.
echo ========================================
echo Done!
echo The EXE file is located in: dist\PhotoSorter.exe
echo ========================================
pause
