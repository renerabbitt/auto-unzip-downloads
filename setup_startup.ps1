# Auto Unzip Startup Setup PowerShell Script

Write-Host "Auto Unzip Startup Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "Setting up auto unzip watcher to start automatically" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Get the startup folder path
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ScriptPath = "C:\Program Files\Rabbitt Custom Programs\auto_unzip_watcher_improved.py"
$ShortcutPath = "$StartupFolder\Auto Unzip Watcher.lnk"

Write-Host "Creating startup shortcut..." -ForegroundColor Yellow

# Create the shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "pythonw"
$Shortcut.Arguments = $ScriptPath
$Shortcut.WorkingDirectory = "C:\Program Files\Rabbitt Custom Programs"
$Shortcut.Description = "Auto Unzip Watcher Startup"
$Shortcut.Save()

Write-Host "Startup shortcut created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "The auto unzip watcher will now:" -ForegroundColor Cyan
Write-Host "- Start automatically when Windows boots" -ForegroundColor White
Write-Host "- Run in the background without user intervention" -ForegroundColor White
Write-Host "- Monitor Downloads folder for zip files" -ForegroundColor White
Write-Host "- Automatically extract and delete zip files" -ForegroundColor White
Write-Host ""
Write-Host "Startup Management:" -ForegroundColor Cyan
Write-Host "- To disable: Delete the shortcut from $StartupFolder" -ForegroundColor White
Write-Host "- To enable: Run this script again" -ForegroundColor White
Write-Host ""
Write-Host "You can test it now by downloading a zip file to your Downloads folder." -ForegroundColor Green

Read-Host "Press Enter to continue" 