
REM Setup conda environment
set env_path=%cd%\conda_env
conda create -y -p conda_env python=3.10
conda config --append envs_dirs "%env_path%"
conda info --envs

