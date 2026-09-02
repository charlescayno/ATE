For NEW setup (fresh install)
Run "setup.bat" to setup the conda environment and the necessary libraries

For EXISTING setup
Run "install_dependency.bat" to update the necessary libraries

To generate package list
conda list --export > requirements.txt

To install packages in requirements.txt
conda install --file requirements.txt


If there is an issue with Execution Policy when running virtual env
-first run below in power shell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser


To set the correct environment in VSCODE
1. Ctrl + Shift + P > Python:Select Interpreter
2. Select environment


To set up debugging in VSCODE
1. Go to run and debug
2. Set up json
3. Set "justMyCode": false

To always run only main.py in debugging mode, paste the code below in launch.json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
    

        {
            "name": "Python: Main.py",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}