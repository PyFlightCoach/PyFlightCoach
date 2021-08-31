from flightdata import Flight, Fields
from geometry import GPSPosition
from flightanalysis.flightline import Box

#pilot = Flight.from_log("data/logs/flightlines/pilot_pos.BIN")
pilot = Flight.from_log("/home/tom/Desktop/logs210626/00000248.BIN")

#centre = Flight.from_log("data/logs/flightlines/centre_point.BIN")
behind_centre = Flight.from_log("/media/tom/LOGS/APM/LOGS/00000003.BIN")


_p = pilot.read_fields(Fields.GLOBALPOSITION).iloc[-1]
p = GPSPosition(_p.global_position_latitude, _p.global_position_longitude)

_bc = behind_centre.read_fields(Fields.GLOBALPOSITION).iloc[-1]
bc = GPSPosition(_bc.global_position_latitude, _bc.global_position_longitude)

c = p.offset(p - bc)


#_c = centre.read_fields(Fields.GLOBALPOSITION).iloc[-1]
#c = GPSPosition(_c.global_position_latitude, _c.global_position_longitude)
#


#box = Box.from_points("morning_left_1", p,c)

print(bc)
print(p)
print(c)

from json import dump
from io import open
with open("temp.json", "w") as f:
    dump({"pilot": p.to_dict(), "center": c.to_dict()}, f)

###box.to_json("data/flightlines/duckhole_180821.json")