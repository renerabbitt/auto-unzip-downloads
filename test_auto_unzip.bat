@echo off
echo Testing Auto Unzip Watcher
echo =========================

REM Check if Downloads directory exists
if not exist "C:\Users\rener\Dropbox\Assets\Downloads" (
    echo ERROR: Downloads directory not found!
    echo Expected: C:\Users\rener\Dropbox\Assets\Downloads
    pause
    exit /b 1
)

echo Downloads directory found ✓

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not available!
    pause
    exit /b 1
)

echo Python is available ✓

REM Check if watchdog is installed
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Watchdog is not installed!
    echo Installing watchdog...
    pip install watchdog==3.0.0
    if errorlevel 1 (
        echo ERROR: Failed to install watchdog!
        pause
        exit /b 1
    )
)

echo Watchdog is installed ✓

REM Test the watcher script
echo Testing watcher script...
python auto_unzip_watcher.py --test >nul 2>&1
if errorlevel 1 (
    echo ERROR: Watcher script has issues!
    pause
    exit /b 1
)

echo Watcher script is working ✓

echo.
echo All tests passed! The Auto Unzip Watcher should be working correctly.
echo.
echo To start the watcher, run: python auto_unzip_watcher.py
echo To stop the watcher, press Ctrl+C
echo.

pause 