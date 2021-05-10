from flightanalysis import Section, Schedule, FlightLine
import numpy as np
import pandas as pd
from geometry import Points, Quaternions, Transformation, Coord, Point
from json import dump, load
from io import open

def create_json(sec: Section, file: str):
    """Create a json file to input into the flight coach plotter (https://www.flightcoach.org/ribbon/plotter.html)
    

    Args:
        sec (Section): [description]
    """
    fcdata = pd.DataFrame(columns=["N","E","D","VN","VE","VD","r","p","yw","wN","wE","roll","pitch","yaw"])

    fcdata["N"] = sec.x
    fcdata["E"] = -sec.y
    fcdata["D"] = -sec.z

    wvels = sec.body_to_world(Points.from_pandas(sec.bvel))

    fcdata["VN"] = wvels.x
    fcdata["VE"] = -wvels.y
    fcdata["VD"] = -wvels.z
    transform = Transformation.from_coords(
        Coord.from_xy(Point(0,0,0), Point(1,0,0), Point(0,1,0)),
        Coord.from_xy(Point(0,0,0), Point(1,0,0), Point(0,-1,0))
        )

    eul = transform.quat(Quaternions.from_pandas(sec.att)).to_euler()
    ex, ey, ez =  eul.x, eul.y, eul.z


    fcdata["roll"] = ex
    fcdata["pitch"] = ey
    fcdata["yaw"] = ez

    fcdata["r"] = np.degrees(fcdata["roll"])
    fcdata["p"] = np.degrees(fcdata["pitch"])
    fcdata["yw"] = np.degrees(fcdata["yaw"])

    fcdata["wN"] = np.zeros(len(ex))
    fcdata["wE"]= np.zeros(len(ex))


    fcdata = fcdata.reset_index()
    fcdata.columns = ["time", "N","E","D","VN","VE","VD","r","p","yw","wN","wE","roll","pitch","yaw"]
    dout = fcdata.to_dict("records")

    with open("data/FCJsonHeader.json", "r") as f:
        data = load(f)

    data["data"] = dout

    temp = sec.data.reset_index()
    data["mans"][0]["stop"]=1
    for tman, fcman in zip(sec.manoeuvre.unique(), data["mans"][1:]):
        fcman["stop"] = int(temp.loc[temp.manoeuvre == tman].index[-1] + 1)
        fcman["start"] = int(temp.loc[temp.manoeuvre == tman].index[0])

    with open(file, "w") as f:
        dump(data, f)


if __name__ == "__main__":
    p21 = Schedule.from_json("FlightAnalysis/schedules/P21.json")
    sec = Section.from_schedule(p21, 170.0, "left")