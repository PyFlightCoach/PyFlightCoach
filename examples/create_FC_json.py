from flightanalysis import Section, Schedule, FlightLine
import numpy as np
import pandas as pd
from geometry import Points, Quaternions
from json import dump, load
from io import open

p21 = Schedule.from_json("FlightAnalysis/schedules/P21.json")
template = Section.from_schedule(p21, 170.0, "left")


fcdata = pd.DataFrame(columns=["N","E","D","VN","VE","VD","r","p","yw","wN","wE","roll","pitch","yaw"])

#fcdata["time"] = template.data.index
fcdata["N"] = template.x
fcdata["E"] = -template.y
fcdata["D"] = -template.z

wvels = template.body_to_world(Points.from_pandas(template.bvel))

fcdata["VN"] = wvels.x
fcdata["VE"] = -wvels.y
fcdata["VD"] = -wvels.z

ex, ey, ez = Quaternions.from_pandas(template.att).to_euler()


fcdata["roll"] = ex
fcdata["pitch"] = -ey
fcdata["yaw"] = -ez

fcdata["r"] = np.degrees(fcdata["roll"])
fcdata["p"] = np.degrees(fcdata["pitch"])
fcdata["yw"] = np.degrees(fcdata["yaw"])

fcdata["wN"] = np.zeros(len(ex))
fcdata["wE"]= np.zeros(len(ex))


fcdata = fcdata.reset_index()
fcdata.columns = ["time", "N","E","D","VN","VE","VD","r","p","yw","wN","wE","roll","pitch","yaw"]
dout = fcdata.to_dict("records")


with open("FCJsonHeader.json", "r") as f:
    data = load(f)

data["data"] = dout

with open("testjson.json", "w") as f:
    dump(data, f)
