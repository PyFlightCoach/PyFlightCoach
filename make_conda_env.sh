echo PyFlightCoach conda environment creations
echo use existing environment? y/n

read varname

conda create -n $1 python=3.8 numpy pandas pint fire


conda init bash
conda activate $1

pip install pymavlink
for SUBMODULE in ArdupilotLogReader FlightData geometry
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done