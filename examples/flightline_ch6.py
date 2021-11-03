from flightdata import Flight, Fields
from geometry import GPSPosition, Point
from flightanalysis.flightline import Box
import numpy as np
from scipy.cluster.vq import kmeans
#pilot = Flight.from_log("data/logs/flightlines/pilot_pos.BIN")
log = Flight.from_log("/media/tom/LOGS/APM/LOGS/00000133.BIN")


c6on = log.data.loc[log.data.tx_controls_5>=1500]

import plotly.express as px


#px.line(y=locs.index).show()

#
res = kmeans(c6on.index, 2)
#
mid = np.mean(res[0])
#
#
#
print(res)
pilot = c6on.loc[:mid, Fields.GLOBALPOSITION.names]
p = GPSPosition(*pilot.mean())
#
centre = c6on.loc[mid:, Fields.GLOBALPOSITION.names]

##
c = GPSPosition(*centre.mean())

#
#
#box = Box.from_points("example_box", p,c)
#
#
print(p)
print(c)

#from json import dump
#from io import open
#with open("temp.json", "w") as f:
#    dump({"pilot": p.to_dict(), "center": c.to_dict()}, f)

