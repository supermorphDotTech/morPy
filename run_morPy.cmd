REM This script will execute a PowerShell script located in the same directory.
set "scriptName=run_morPy.ps1"
set "scriptDir=%~dp0"
PowerShell -NoProfile -ExecutionPolicy Bypass -WindowStyle hidden -File "%scriptDir%%scriptName%"