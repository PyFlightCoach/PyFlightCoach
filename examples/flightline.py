from flightdata import Flight, Fields
from geometry import GPSPosition
from flightanalysis import Box, Section
import easygui
import sys
from pathlib import Path
from scipy.cluster.vq import kmeans


def path_or_browse(instruction, meth = easygui.fileopenbox):
    pilot_pos = input(instruction)
    if not pilot_pos:
        pilot_pos = meth()
    else:
        pilot_pos = str(list(Path("/media/tom/LOGS/APM/LOGS/").glob("*000{}.BIN".format(pilot_pos)))[0])
    return pilot_pos

flight = None
if input("use channel 5 switch positions?") in ["y", "Y", "yes"]:
    flight = Flight.from_log(path_or_browse("Pilot Position Bin path or empty for browse\n"))#path_or_browse("Flight Log Bin path or empty for browse\n"))
    c6on = Flight(flight.data.loc[flight.data.tx_controls_5>=1500])
    res = kmeans(c6on.read_fields(Fields.GLOBALPOSITION), 2)[0]


    p = GPSPosition(*res[0])
    c = GPSPosition(*res[1])

else:
    pilot = Flight.from_log(path_or_browse("Pilot Position Bin path or empty for browse\n"))
    centre = Flight.from_log(path_or_browse("Centre Position Bin path or empty for browse\n"))
    p = GPSPosition(*pilot.read_fields(Fields.GLOBALPOSITION).iloc[-1])
    c = GPSPosition(*centre.read_fields(Fields.GLOBALPOSITION).iloc[-1])


box = Box.from_points("new", p, c)

print(p)
print(c)
print(box.to_dict())

if input("create section csv?\n") in ["y", "Y", "yes"]:
    
    if not flight is None:
        use_current = input("use current log?\n")
    else:
        use_current = "n"
    if not use_current in ["y", "Y", "yes"]:
        flight = Flight.from_log(path_or_browse("Flight Log BIN File\n"))

    tx = flight.read_fields(Fields.TXCONTROLS)
    tx = tx - tx.iloc[0]
    tx = tx.iloc[:,:5]
    tx.columns = ["throttle", "aileron_1", "aileron_2", "elevator", "rudder"]

    sec = Section.from_flight(flight, box).append_columns(tx)

    sec.to_csv(path_or_browse("Save section csv location\n", easygui.filesavebox))
#
#
#
#
