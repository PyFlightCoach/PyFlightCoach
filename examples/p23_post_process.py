from flightdata import Flight
from flightanalysis import Section, get_schedule, Box     
from flightplotting.plots import plotsec, plotdtw
import plotly

from geometry import Point, GPSPosition
flight = Flight.from_csv("examples/logs/00000036.csv")

box = Box.from_f3a_zone("examples/logs/box.f3a")

flown = Section.from_flight(flight, box).subset(150, 576)

#plotsec(flown).show()



p23 = get_schedule("F3A", "P23")
template = p23.scale_distance(170).create_raw_template("left", 30.0, 170.0)

dist, aligned = Section.align(flown, template, 2 )

manid = 10
plotdtw(p23.manoeuvres[manid].get_data(aligned), p23.manoeuvres[manid].elements).show()


corrected_p23 = p23.match_intention(aligned).correct_intention()
corrected_template = corrected_p23.create_matched_template(aligned)
#
fig = plotsec(p23.manoeuvres[manid].get_data(aligned), ribb=True)
#
fig.add_traces(plotsec(p23.manoeuvres[10].get_data(corrected_template), color="blue", ribb=True).data).show()