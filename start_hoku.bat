@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo [HOKU315] Repository root: %CD%

if not exist ".venv\Scripts\python.exe" (
  echo [HOKU315] Creating .venv with Python 3.11 ^(fallback 3.12^)...
  py -3.11 -m venv .venv
  if errorlevel 1 (
    py -3.12 -m venv .venv
  )
  if not exist ".venv\Scripts\python.exe" (
    echo [HOKU315] ERROR: Could not create .venv. Install Python 3.11 or 3.12 and ensure `py` launcher works.
    exit /b 1
  )
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [HOKU315] ERROR: Failed to activate .venv
  exit /b 1
)

python -m pip install -q -U pip
python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo [HOKU315] ERROR: pip install failed
  exit /b 1
)

python ops\env\runtime_sanity_check.py --fix
if errorlevel 1 (
  echo [HOKU315] ERROR: runtime_sanity_check failed
  exit /b 1
)

echo [HOKU315] Starting Reflex ^(Ctrl+C to stop^)...
python -m reflex run
set REFLEX_EXIT=%ERRORLEVEL%
exit /b %REFLEX_EXIT%
