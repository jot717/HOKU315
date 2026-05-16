@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
  echo [HOKU315] ERROR: No .venv found. Run start_hoku.bat once to create it.
  exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python ops\env\runtime_sanity_check.py --fix --strict-venv
if errorlevel 1 exit /b 1

python ops\env\reflex_compile_gate.py
if errorlevel 1 exit /b 1

python -m pytest tests\regression\ -v --tb=short
if errorlevel 1 exit /b 1

python -m tests.run_all_tests
if errorlevel 1 exit /b 1

echo [HOKU315] All checks passed.
exit /b 0
