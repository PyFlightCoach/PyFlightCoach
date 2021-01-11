echo PyFlightCoach conda environment creations
echo use existing environment? y/n

read varname

if [ $varname == "n" ]; then
    echo enter new env name
    read envname

    conda create -n $envname python=3.8
    conda init bash
    conda activate $envname
fi

conda install numpy pandas pint fire
pip install pymavlink
for SUBMODULE in ArdupilotLogReader FlightData geometry
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done