:: This script requires 'python' and 'virtualenv' to be in path!
@echo off
cd %~dp0
mkdir .\venv
virtualenv .\venv
.\venv\Scripts\pip.exe install Pillow

pause