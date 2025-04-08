for SUBMODULE in ArdupilotLogReader Schemas geometry FlightData Plotting DroneInterface; do
    cd packages/$SUBMODULE
    pip install -e . --config-settings editable_mode=compat
    cd ../..
done
