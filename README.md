# Auto Unzip Watcher

Automatically monitors your Downloads folder and extracts zip files to organized subfolders.

## Features
- ✅ Monitors Downloads folder for new zip files
- ✅ Creates subfolders named after zip files
- ✅ Extracts contents automatically
- ✅ Deletes original zip file
- ✅ Runs in background on Windows startup
- ✅ Minimal performance impact

## Installation

### Prerequisites
- Windows 10/11
- Python 3.6 or higher

### Quick Setup
1. Download the files
2. Open PowerShell as Administrator
3. Run: `powershell -ExecutionPolicy Bypass -File setup_startup.ps1`
4. Download a zip file to test!

## Usage
- Download any zip file to your Downloads folder
- Watch it automatically extract to a subfolder
- Original zip file gets deleted

## Files
- `auto_unzip_watcher_improved.py` - Main watcher script
- `setup_startup.ps1` - Automatic startup setup
- `test_auto_unzip.bat` - Test script

## Configuration
Edit the downloads path in the Python script if needed:
```python
downloads_dir = Path(r"C:\Users\rener\Dropbox\Assets\Downloads")
```

## Troubleshooting
- Check log file: `auto_unzip_watcher.log`
- Ensure Python and watchdog are installed
- Verify Downloads folder exists
