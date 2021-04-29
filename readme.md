# Packages for Handling Flight Log Data

This project contains a collection of packages for playing with flight data, principally aimed at plotting and analysing precision aerobatics. 

The main focus on the work at the moment is to compare recorded flight data to equivalent, perfect, generated flight data. To do this the sequence definition needs to be parsed and the sections of recorded data corresponding to the manoeuvres and elements in the definition need to be identified. So far using dynamic time warping based on axis rates seems to be a promising solution to this problem.

The work here was the inspiration for flight coach, which is a web app that brings aerobatic flight plotting functionality to a wider audience: https://www.flightcoach.org/.

The following packages are included:

ArdupilotLogReader - reads the requested fields of an ardupilot bin file to a dict of Pandas Dataframes. 

FlightData - Picks up the relevant fields from the log reader and converts them to a consistent set of units. This is separate from the log reader as it should be independent of the type of log if more readers were needed.

geometry - Useful tools for handling geometry. contains classes that wrap around a point, quaternion, coordinate frame etc. 

FlightAnalysis - Tools for performing analysis on the flight data, such as rotating to a flightline, generating template flight data. Also contains some thoughts on parsing a sequence.

FlightPlotting - Handy tools for creating plotly plots of the flight data. The plots below were created using this package.

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/vertical_8_comparison.png?raw=true)
A flown vertical 8 recorded using the flight logger (in grey), compared to a generated template vertical 8 (in orange). 

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/gb_comparison.png?raw=true)
A flown golf ball recorded using the flight logger (in grey), compared to a generated template golf ball (in orange). 

![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/vertical_8_dtw.png?raw=true)
Automatically identifying the individual elements of the flown vertical 8 using dynamic time warping.


![alt text](https://github.com/PyFlightCoach/PyFlightCoach/blob/main/gb_dtw.png?raw=true)
Automatically identifying the individual elements of the flown golf ball using dynamic time warping.

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
