for SUBMODULE in ArdupilotLogReader FlightData geometry FlightAnalysis FlightPlotting
do
    cd $SUBMODULE
    python setup.py develop
    cd ..
done