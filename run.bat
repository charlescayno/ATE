@Echo off
REM Default launcher: physical bench (GPIB). Virtual bench: run_simulation.bat
cd /d "%~dp0"
call "%~dp0run_hardware.bat" %*
exit /b %ERRORLEVEL%
