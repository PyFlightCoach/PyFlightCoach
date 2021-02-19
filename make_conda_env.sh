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

while read requirement; 
do 
    conda install --yes -c conda-forge $requirement || pip install $requirement 
done < requirements.txt

for SUBMODULE in ArdupilotLogReader FlightData geometry FlightAnalysis
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done