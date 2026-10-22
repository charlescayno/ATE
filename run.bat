@Echo off
REM Default launcher: virtual simulation (same as run_simulation.bat). Bench: run_hardware.bat
cd /d "%~dp0"
call "%~dp0run_simulation.bat" %*
exit /b %ERRORLEVEL%
