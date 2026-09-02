@Echo off
set PATH=%PATH%;%USERPROFILE%\Anaconda3
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\Anaconda3\Library\bin
set PATH=%PATH%;C:\Anaconda3
set PATH=%PATH%;C:\Anaconda3\Scripts
set PATH=%PATH%;C:\Anaconda3\Library\bin
set PATH=%PATH%;%USERPROFILE%\\AppData\Local\anaconda3
set PATH=%PATH%;%USERPROFILE%\\AppData\Local\anaconda3\Scripts
set PATH=%PATH%;%USERPROFILE%\\AppData\Local\anaconda3\Library\bin


@Echo on
call setup/init_shell.bat

call setup/setup_env.bat

call setup/activate_env.bat

call setup/install_dependencies.bat

call setup/copy_template.bat

pause
