@Echo off
set PATH=%PATH%;%USERPROFILE%\Anaconda3
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Library\bin
@Echo on
call setup/activate_env.bat
python main.py