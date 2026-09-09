@Echo off
REM Launch PI ATE in Virtual Simulation Mode (No Physical Hardware Needed)
set PATH=%PATH%;%USERPROFILE%\Anaconda3
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Library\bin
@Echo on
call setup/activate_env.bat
python main.py --simulation

