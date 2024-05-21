pip install pymavlink
conda install --yes conda-build
conda install --yes --file requirements.txt
for SUBMODULE in ArdupilotLogReader geometry FlightData FlightAnalysis FlightPlotting
do
    cd $SUBMODULE
    conda-develop .
    cd ..
done