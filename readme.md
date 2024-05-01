## Flight Data Analysis Tools

This project contains a collection of packages for working with flight data, mostly aimed at plotting and analysing precision aerobatics, but many of the tools are useful for other applications. The project was the inspiration for Flight Coach, a web app that brings aerobatic flight plotting functionality to a wider audience: https://www.flightcoach.org/.

The following packages are included:
- **ardupilot-log-reader** - a wrapper round pymavlink to read an Ardupilot bin file
- **pfc-geometry** - Tools for handling 3D geometry. contains classes that wrap around a point, quaternion, coordinate frame etc. 
- **flightdata** - Datastructures for handling flight data
- **flightanalysis** - Tools for performing analysis on the flight data, such as rotating to a flightline, generating template flight data, parsing a sequence and aligning the generated template data to the flown data.
- **flightplotting** - Handy tools for creating plotly plots of the flightdata objects.

<img src="comet.png" alt="drawing" width="49%"/>
<img src="sql.png" alt="drawing" width="49%"/>

### Install from pypi
```bash
pip install ardupilot-log-reader
pip install pfc-geometry
pip install flightdata
pip install flightanalysis
pip install flightplotting
```

### Cloning
When cloning use the --recurse-submodules option:
```bash
git clone --recurse-submodules https://github.com/PyFlightCoach/PyFlightCoach.git
```
If you forget to use the --recurse-submodules option then do this:
```bash
git submodule update --init --recursive
```

### Easy setup (with conda):
```bash
source make_conda_env.sh
```
### Easy setup (with venv):
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
source install_submodules.sh
```
### To setup manually

install the requirements in requirements.txt, then cd to each submodule and do: 
```bash
pip install -e .
```

## Docker

Build the docker image:
```bash
docker build -t pyf .
docker run --rm -it pyf /bin/bash
```

get the latest released image from docker hub:
```bash
docker pull thomasdavid/pyflightcoach
```