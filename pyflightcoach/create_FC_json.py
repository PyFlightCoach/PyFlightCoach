from flightanalysis import Section, Schedule, FlightLine
import numpy as np
import pandas as pd
from geometry import Points, Quaternions, Transformation, Coord, Point
from json import dump, load
from io import open

def create_json(sec: Section, file: str, header: str):
    """Create a json file to input into the flight coach plotter (https://www.flightcoach.org/ribbon/plotter.html)
    

    Args:
        sec (Section): [description]
    """
    print("creating {}".format(file))
    print("creating 6d data")
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

    with open(header, "r") as f:
        data = load(f)

    data["data"] = dout

    print("populating splitter")

    sec.data.loc[:3.5, ["manoeuvre"]] = "tkoff"

    temp = sec.data.reset_index()
    
    for tman, fcman in zip(sec.manoeuvre.unique(), data["mans"]):
        fcman["stop"] = int(temp.loc[temp.manoeuvre == tman].index[-1])+1
        fcman["start"] = int(temp.loc[temp.manoeuvre == tman].index[0])
        fcman["wd"]=100*sec.get_manoeuvre(tman).duration / sec.duration

    data["mans"][0]["wd"] = data["mans"][0]["wd"] + 0.3

    print("saving file")
    with open(file, "w") as f:
        dump(data, f)


if __name__ == "__main__":
    from flightanalysis.schedule.p21 import *
    from flightanalysis.schedule.p23 import *
    from flightanalysis.schedule.f21 import *
    from flightanalysis.schedule.f23 import *
    create_json(Section.from_schedule(p23, 150.0, "left"), "P23_template_150.json", "data/FCJsonHeader_p23.json")
    create_json(Section.from_schedule(p21, 150.0, "left"), "P21_template_150.json", "data/FCJsonHeader_p21.json")
    create_json(Section.from_schedule(f21, 150.0, "right"), "F21_template_150.json", "data/FCJsonHeader_f21.json")
    create_json(Section.from_schedule(f23, 150.0, "left"), "F23_template_150.json", "data/FCJsonHeader_f23.json")
    create_json(Section.from_schedule(p23, 170.0, "left"), "P23_template_170.json", "data/FCJsonHeader_p23.json")
    create_json(Section.from_schedule(p21, 170.0, "left"), "P21_template_170.json", "data/FCJsonHeader_p21.json")
    create_json(Section.from_schedule(f21, 170.0, "right"), "F21_template_170.json", "data/FCJsonHeader_f21.json")
    create_json(Section.from_schedule(f23, 170.0, "left"), "F23_template_170.json", "data/FCJsonHeader_f23.json")