pip install pymavlink
conda install --yes --file requirements.txt
for SUBMODULE in ArdupilotLogReader geometry FlightData FlightAnalysis FlightPlotting
do
    cd $SUBMODULE
    pip install -e . --config-settings editable_mode=compat
    cd ..
done