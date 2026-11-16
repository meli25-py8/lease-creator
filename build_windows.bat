@echo off
cd /d "%~dp0"
py -3 -m venv .venv-build
if errorlevel 1 goto error
.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
if errorlevel 1 goto error
.venv-build\Scripts\python.exe build_desktop.py
if errorlevel 1 goto error
echo Application created: dist\LeaseCreator\LeaseCreator.exe
pause
exit /b 0
:error
echo Build failed. See the message above.
pause
exit /b 1
