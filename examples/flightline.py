from flightdata import Flight, Fields
from geometry import GPSPosition
from flightanalysis.flightline import Box

#pilot = Flight.from_log("data/logs/flightlines/pilot_pos.BIN")
pilot = Flight.from_log("/media/tom/LOGS/APM/LOGS/00000053.BIN")

#centre = Flight.from_log("data/logs/flightlines/centre_point.BIN")
centre = Flight.from_log("/media/tom/LOGS/APM/LOGS/00000054.BIN")

_p = pilot.read_fields(Fields.GLOBALPOSITION).iloc[-1]
p = GPSPosition(_p.global_position_latitude, _p.global_position_longitude)

_c = centre.read_fields(Fields.GLOBALPOSITION).iloc[-1]
c = GPSPosition(_c.global_position_latitude, _c.global_position_longitude)


box = Box.from_points("example_box", p,c)


print(p)
print(c)

from json import dump
from io import open
with open("temp.json", "w") as f:
    dump({"pilot": p.to_dict(), "center": c.to_dict()}, f)

