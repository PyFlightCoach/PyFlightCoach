for SUBMODULE in ArdupilotLogReader FlightData geometry FlightAnalysis FlightPlotting
do
    cd $SUBMODULE
    pip install -e .
    cd ..
done