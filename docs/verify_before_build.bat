@echo off
REM Pre-Build Verification Script
REM Checks if all required files and dependencies are in place

echo ==========================================
echo   PRE-BUILD VERIFICATION SCRIPT
echo ==========================================
echo.

set ERROR_COUNT=0

REM Check 1: Python installed
echo [1/12] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] FAILED: Python not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Python installed
)

REM Check 2: PyInstaller installed
echo [2/12] Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [X] FAILED: PyInstaller not installed
    echo     Fix: pip install pyinstaller
    set /a ERROR_COUNT+=1
) else (
    echo [OK] PyInstaller installed
)

REM Check 3: Required Python packages
echo [3/12] Checking required packages...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [X] FAILED: PyQt6 not installed
    set /a ERROR_COUNT+=1
) else (
    echo [OK] PyQt6 installed
)

REM Check 4: pyproject.toml exists
echo [4/12] Checking pyproject.toml...
if not exist "pyproject.toml" (
    echo [X] FAILED: pyproject.toml not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] pyproject.toml exists
)

REM Check 5: Icon file
echo [5/12] Checking icon file...
if not exist "travel_billing_software\billing_app.ico" (
    echo [X] FAILED: billing_app.ico not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Icon file exists
)

REM Check 6: Auth data file
echo [6/12] Checking auth_data.json...
if not exist "travel_billing_software\auth_data.json" (
    echo [X] FAILED: auth_data.json not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] auth_data.json exists
)

REM Check 7: Config folder
echo [7/12] Checking config folder...
if not exist "travel_billing_software\config" (
    echo [X] FAILED: config folder not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] config folder exists
)

REM Check 8: Fonts folder
echo [8/12] Checking fonts folder...
if not exist "travel_billing_software\fonts" (
    echo [X] FAILED: fonts folder not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] fonts folder exists
)

REM Check 9: TravelBilling.spec
echo [9/12] Checking TravelBilling.spec...
if not exist "TravelBilling.spec" (
    echo [X] FAILED: TravelBilling.spec not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] TravelBilling.spec exists
)

REM Check 10: TravelBilling.iss
echo [10/12] Checking TravelBilling.iss...
if not exist "TravelBilling.iss" (
    echo [X] FAILED: TravelBilling.iss not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] TravelBilling.iss exists
)

REM Check 11: Inno Setup installed
echo [11/12] Checking Inno Setup...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo [OK] Inno Setup installed
) else (
    echo [!] WARNING: Inno Setup not found at default location
    echo     You can still build .exe, but installer creation will fail
    echo     Download from: https://jrsoftware.org/isinfo.php
)

REM Check 12: Auto-updater files
echo [12/12] Checking auto-updater files...
if not exist "travel_billing_software\utils\auto_updater.py" (
    echo [X] FAILED: auto_updater.py not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] auto_updater.py exists
)

if not exist "travel_billing_software\ui\update_dialog.py" (
    echo [X] FAILED: update_dialog.py not found
    set /a ERROR_COUNT+=1
) else (
    echo [OK] update_dialog.py exists
)

echo.
echo ==========================================
echo   VERIFICATION COMPLETE
echo ==========================================
echo.

if %ERROR_COUNT% equ 0 (
    echo [SUCCESS] All checks passed! ^_^
    echo.
    echo You are ready to build!
    echo Run: build_release.bat
    echo.
) else (
    echo [FAILED] %ERROR_COUNT% error(s) found!
    echo.
    echo Please fix the errors above before building.
    echo.
)

pause
