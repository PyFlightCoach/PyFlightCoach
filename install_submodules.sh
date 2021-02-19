for SUBMODULE in ArdupilotLogReader FlightData geometry FlightAnalysis
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done