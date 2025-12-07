@echo off
REM Build script for Travel Billing Software
REM This script automates the build process: PyInstaller -> Inno Setup

echo ========================================
echo Travel Billing Software Build Script
echo ========================================
echo.

REM Check if pyproject.toml exists
if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Read version from pyproject.toml
echo [1/5] Reading version from pyproject.toml...
for /f "tokens=2 delims==" %%a in ('findstr /C:"version = " pyproject.toml') do (
    set VERSION=%%a
)
REM Remove quotes, spaces, and leading/trailing whitespace from version
set VERSION=%VERSION:"=%
set VERSION=%VERSION: =%
echo Current version: %VERSION%
echo.

REM Clean previous builds
echo [2/5] Cleaning previous builds...
echo Attempting to close any running instances...
taskkill /F /IM TravelBilling.exe >nul 2>&1
timeout /t 2 /nobreak >nul
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "Output" rmdir /s /q Output
echo Clean complete.
echo.

REM Build with PyInstaller
echo [3/5] Building with PyInstaller...
pyinstaller TravelBilling.spec
if errorlevel 1 (
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)
echo PyInstaller build complete.
echo.

REM Check if Inno Setup is installed
echo [4/5] Creating installer with Inno Setup...
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo WARNING: Inno Setup not found at default location.
    echo Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo Or compile TravelBilling.iss manually.
    echo.
    echo Build executable is available at: dist\TravelBilling\TravelBilling.exe
    pause
    exit /b 0
)

REM Update version in Inno Setup script
echo Updating version in TravelBilling.iss...
cscript //Nologo update_iss_version.vbs "%VERSION%" "TravelBilling.iss"
if errorlevel 1 (
    echo WARNING: Could not update version automatically
    echo Please ensure TravelBilling.iss has the correct version
)

REM Compile with Inno Setup
%ISCC% TravelBilling.iss
if errorlevel 1 (
    echo ERROR: Inno Setup compilation failed!
    pause
    exit /b 1
)
echo Installer created successfully.
echo.

REM Summary
echo [5/5] Build Summary
echo ========================================
echo Version: %VERSION%
echo Executable: dist\TravelBilling\TravelBilling.exe
echo Installer: Output\TravelBilling_Setup_v%VERSION%.exe
echo ========================================
echo.
echo Build complete! You can now:
echo 1. Test the installer: Output\TravelBilling_Setup_v%VERSION%.exe
echo 2. Create GitHub release with tag: v%VERSION%
echo 3. Upload the installer to GitHub Releases
echo.
pause
