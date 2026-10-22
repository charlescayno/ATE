@Echo off
cd /d "%~dp0"
set "PY=%~dp0conda_env\python.exe"
if not exist "%PY%" set "PY=C:\Users\Charles\.gemini\antigravity\scratch\ATE\conda_env\python.exe"
if not exist "%PY%" (
  echo [ERROR] No PI ATE conda env found.
  echo   Expected: %~dp0conda_env\python.exe
  echo   Or copy conda_env from your other ATE clone.
  exit /b 1
)
set PI_ATE_SIMULATION=1
echo [INFO] Simulation mode — using %PY%
"%PY%" main.py -s %*
