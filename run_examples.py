import flightplotting.templates
from flightplotting.plots import plotsec, plotdtw
from flightplotting.model import OBJ
from examples.dtw import *
from examples.elms import *

obj = OBJ.from_obj_file('data/models/ColdDraftF3APlane.obj').transform(Transformation(
    Point(0.75, 0, 0), Quaternion.from_euler(Point(np.pi, 0, -np.pi/2))
))


compplot = plotsec(makev8(), obj, 7, 50, color='orange')
compplot = plotsec(flown_vertical_8, obj, 7, 50, compplot, color='grey')
compplot.show()

v8plot = plotdtw(flown_vertical_8, v8segments)
v8plot.show()

gbplot = plotdtw(flown_golfball, gbsegments)
gbplot.show()

compplot2 = plotsec(makegb(), obj, 7, 50, color='orange')
compplot2 = plotsec(flown_golfball, obj, 7, 50, compplot2, color='grey')
compplot2.show()


from flightanalysis import Section
from flightanalysis.schedule import Schedule
from json import load
from io import open

with open("FlightAnalysis/schedules/P21.json", "r") as f:

    p21 = Section.from_schedule(
        Schedule.from_dict(load(f)),
        170, "left"
        )

plotsec(p21, obj, 7, 100, color='orange').show()

