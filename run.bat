@Echo off
REM PI ATE launcher — runs THIS git folder (not pi_ate 1 or other Downloads copies).
cd /d "%~dp0"
set "PI_ATE_ROOT=%CD%"
for /f "delims=" %%h in ('git rev-parse --short HEAD 2^>nul') do set PI_ATE_GIT=%%h
if not defined PI_ATE_GIT set PI_ATE_GIT=unknown
echo.
echo ============================================================
echo   PI ATE  git %PI_ATE_GIT%
echo   %PI_ATE_ROOT%
echo ------------------------------------------------------------
echo   Add Tests ^> Test Type: dual-output / 2-port tests at top
echo   Steady-State Poll Waveform 2 Port: Poll Interval and
echo   Poll Duration fields on the main Add Tests form
echo   Virtual bench: run_simulation.bat
echo ============================================================
echo.
call "%~dp0run_hardware.bat" %*
exit /b %ERRORLEVEL%
