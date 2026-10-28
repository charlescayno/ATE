@Echo off
REM PI ATE launcher — always runs THIS folder (not pi_ate 1 or other copies).
cd /d "%~dp0"
for /f "delims=" %%h in ('git rev-parse --short HEAD 2^>nul') do set PI_ATE_GIT=%%h
if not defined PI_ATE_GIT set PI_ATE_GIT=unknown
echo.
echo [PI ATE] Folder: %CD%
echo [PI ATE] Git:    %PI_ATE_GIT%  — Add Tests ^> Test Type includes Steady-State Waveform 2 Port and Steady-State Poll Waveform 2 Port
echo.
call "%~dp0run_hardware.bat" %*
exit /b %ERRORLEVEL%
