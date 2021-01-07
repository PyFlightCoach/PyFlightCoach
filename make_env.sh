
echo -n "Add to active environment (y/n)? "
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo Yes
else
    echo No

    echo -n "Enter new environment name "
    read newenv


    conda init bash
    conda activate $newenv
    
fi

pip install pymavlink
for SUBMODULE in ArdupilotLogReader FlightData geometry
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done