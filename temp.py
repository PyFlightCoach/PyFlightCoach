from flightdata import Flight, Fields
from flightanalysis import Section

flight = Flight.from_log("/mnt/c/projects/flight_analysis/logs/00000117.BIN")


tx = flight.read_fields(Fields.TXCONTROLS)
tx = tx - tx.iloc[0]
tx = tx.iloc[:,:5]
tx.columns = ["throttle", "aileron_1", "aileron_2", "elevator", "rudder"]

sec = Section.from_flight(flight, "snap_rolls.json" ).append_columns(tx)

sec.to_csv("FlightAnalysis/examples/snap_roll_section.csv")