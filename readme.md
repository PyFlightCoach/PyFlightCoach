# Packages for Handling Flight Log Data

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/goodvertical8.png?raw=true)

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/FAI_P21.png?raw=true)


### Cloning
When cloning use the --recurse-submodules option:

git clone --recurse-submodules https://github.com/PyFlightCoach/PyFlightCoach.git

If you forget to use the --recurse-submodules option then do this:

git submodule update --init --recursive

### Easy setup (with conda) Bash:

source make_conda_env.sh

### Easy setup (with venv) & Bash:

python -m venv env
source env/bin/activate
pip install -r requirements.txt
source install_submodules.sh

### To setup manually

install the requirements in requirements.txt, then cd to each submodule and do: python setup.py develop.
Note the submodules are interdependent, and currently not published anywhere else, so you need to install them in order:
1 ArdupilotLogReader,
2 FlightData,
3 geometry,
4 FlightAnalysis,
5 FlightPlotting


## To use the environment in a jupyter notebook

conda install ipykernel plotly ipywidgets

python -m ipykernel install --user --name flightcoach
