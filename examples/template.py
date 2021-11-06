from flightanalysis import get_schedule, Categories
from flightplotting.plots import plotsec

schedule = get_schedule(Categories.F3A, "P21").scale_distance(170)
template = schedule.create_raw_template("left", 30.0, 170)


plotsec(template).show()