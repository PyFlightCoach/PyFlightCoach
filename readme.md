# Collection of Python Packages for Handling Flight Log Data

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/FAI_P21.png?raw=true)

## to clone use the recurse-submodules option
git clone --recurse-submodules

## to update
git pull
git submodule update --init --recursive

## to setup (must have conda installed)
### Bash:
source make_conda_env.sh pyflightcoach

## then to use the environment in a jupyter notebook and make plots
conda install ipykernel plotly ipywidgets
python -m ipykernel install --user --name flightcoach
