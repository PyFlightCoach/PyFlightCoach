from tkinter.constants import N
from flightdata import Flight, Fields, Origin, State
from geometry import GPS
from tkinter import filedialog
import sys
from pathlib import Path
from scipy.cluster.vq import kmeans
import os
from datetime import datetime
from pathlib import Path

logdir=Path("/home/td6834/projects/logs/")


dates = []
for p in logdir.iterdir():
    try:
        dates.append(datetime.strptime(p.stem, "%Y_%m_%d"))
    except Exception as ex:
        pass
basepath = logdir / max(dates).strftime('%Y_%m_%d')

def path_or_browse(instruction, meth = filedialog.askopenfilename, default=Path(basepath)):
    pilot_pos = input(instruction)
                
    while True:
        try:
            if pilot_pos is None:
                pilot_pos = meth(msg=instruction, default=default)
            
            if not Path(pilot_pos).is_file():
                pilot_pos = str(list(default.glob("*00{}.BIN".format(pilot_pos)))[0])
            
            return pilot_pos

        except:
            if not input("not found, try again?") in ['yes', 'y', "Y"]:
                exit()
    
flight = None
if input("use channel 5 switch positions?") in ["y", "Y", "yes"]:
    flight = Flight.from_log(path_or_browse("flight log Bin path or empty for browse\n"))#path_or_browse("Flight Log Bin path or empty for browse\n"))
    c6on = Flight(flight.data.loc[flight.data.rcin_c5>=1500])
    res = kmeans(c6on.gps, 2)[0]


    p = GPS(*res[0])
    c = GPS(*res[1])


else:
    pilot = Flight.from_log(path_or_browse("Pilot Position Bin path or empty for browse\n"))
    centre = Flight.from_log(path_or_browse("Centre Position Bin path or empty for browse\n"))
    p = GPS(*pilot.gps.iloc[-1])
    c = GPS(*centre.gps.iloc[-1])


box = Origin.from_points("new", p, c)

print(p)
print(c)
print(box.to_dict())


if input("save f3a zone?") in ["y", "Y", "yes"]:
    with open(Path(basepath) / "box.f3a" , "w") as f:
        f.write(box.to_f3a_zone()) 


if input("create section csv?\n") in ["y", "Y", "yes"]:
    
    if not flight is None:
        use_current = input("use current log?\n")
    else:
        use_current = "n"
    if not use_current in ["y", "Y", "yes"]:
        flight = Flight.from_log(path_or_browse("Flight Log BIN File\n"))

    sec = State.from_flight(flight, box)

    sec.to_csv(path_or_browse("Save section csv location\n", filedialog.asksaveasfilename))
#
#
#
#
