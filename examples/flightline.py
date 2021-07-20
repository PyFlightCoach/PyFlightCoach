from flightdata import Flight, Fields
from geometry import GPSPosition
from flightanalysis.flightline import Box

pilot = Flight.from_log("data/logs/flightlines/pilot_pos.BIN")
centre = Flight.from_log("data/logs/flightlines/centre_point.BIN")


_p = pilot.read_fields(Fields.GLOBALPOSITION).iloc[-1]
p = GPSPosition(_p.global_position_latitude, _p.global_position_longitude)

_c = centre.read_fields(Fields.GLOBALPOSITION).iloc[-1]
c = GPSPosition(_c.global_position_latitude, _c.global_position_longitude)



box = Box.from_points("evening_normal", p,c)
box.club = "BRCMAC"
box.country = "UK"



print(p)
print(c)


print(box)
box.to_json("data/flightlines/duckhole_evening_normal.json")