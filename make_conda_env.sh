conda init bash
conda create -n $1 python=3.8 numpy pandas pint
conda activate $1

pip install pymavlink
for SUBMODULE in ArdupilotLogReader FlightData geometry
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done