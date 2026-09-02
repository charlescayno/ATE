@Echo off
set PATH=%PATH%;%USERPROFILE%\Anaconda3
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Library\bin
set PATH=%PATH%;C:\Anaconda3
set PATH=%PATH%;C:\Anaconda3\Scripts
set PATH=%PATH%;C:\Anaconda3\Library\bin
@Echo on
call setup/init_shell.bat

call setup/activate_env.bat

call setup/install_dependencies.bat

pause
