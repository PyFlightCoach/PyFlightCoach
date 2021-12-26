from flightanalysis import Section, get_schedule                
from flightplotting.plots import plotsec, plotdtw
import plotly

from geometry import Point

flown = Section.from_csv("examples/P23.csv").subset(102, 475)

p23 = get_schedule("F3A", "P23")
template = p23.scale_distance(170).create_raw_template("left", 30.0, 170.0)



dist, aligned = Section.align(flown, template, 2 )


manid = 10
plotdtw(p23.manoeuvres[manid].get_data(aligned), p23.manoeuvres[manid].elements).show()

corrected_p23 = p23.match_intention(aligned).correct_intention()
corrected_template = corrected_p23.create_matched_template(aligned)

fig = plotsec(p23.manoeuvres[manid].get_data(aligned), ribb=True)

fig.add_traces(plotsec(p23.manoeuvres[10].get_data(corrected_template), color="blue", ribb=True).data).show()