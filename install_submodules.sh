for SUBMODULE in ArdupilotLogReader geometry FlightData FlightAnalysis FlightPlotting
do
    cd $SUBMODULE
    conda develop .
    cd ..
done