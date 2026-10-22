@Echo off
REM PI ATE with physical bench (Anaconda env + GPIB). For virtual bench use run_simulation.bat or run.bat.
cd /d "%~dp0"
set PATH=%PATH%;%USERPROFILE%\Anaconda3
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Library\bin
@Echo on
call setup/activate_env.bat
python main.py %*
