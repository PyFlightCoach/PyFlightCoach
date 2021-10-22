from flightdata import Flight, Fields
from geometry import GPSPosition
from flightanalysis.flightline import Box

#pilot = Flight.from_log("data/logs/flightlines/pilot_pos.BIN")
#"/mnt/D/APM/LOGS/00000100.BIN"
#"/mnt/c/projects/flight_analysis/logs/"
pilot = Flight.from_log("/mnt/c/projects/flight_analysis/logs/00000106.BIN")

#centre = Flight.from_log("data/logs/flightlines/centre_point.BIN")
centre = Flight.from_log("/mnt/c/projects/flight_analysis/logs/00000107.BIN")


p = GPSPosition(*pilot.read_fields(Fields.GLOBALPOSITION).iloc[-1])

c = GPSPosition(*centre.read_fields(Fields.GLOBALPOSITION).iloc[-1])


box = Box.from_points("example_box", p,c)


print(p)
print(c)

from json import dump
from io import open
with open("temp.json", "w") as f:
    dump(box.to_dict(), f)

