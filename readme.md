# Collection of Python Packages for Handling Flight Log Data

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/goodvertical8.png?raw=true)

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/FAI_P21.png?raw=true)

### To setup

install the requirements in requirements.txt, then cd to each submodule and do: python setup.py develop.
Note the submodules are interdependent, and currently not published anywhere else, so you need to install them in order:
1 ArdupilotLogReader
2 FlightData
3 geometry
4 FlightAnalysis

TODO move the streamlit stuff from flightplotting into examples, make flightplotting installable

### Easy setup (with conda) Bash:

source make_conda_env.sh

## To use the environment in a jupyter notebook

conda install ipykernel plotly ipywidgets

python -m ipykernel install --user --name flightcoach
