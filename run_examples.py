from examples.dtw import *
from examples.elms import *

compplot = plotelms(makev8(), 7, 50, color='orange')
compplot = plotelms(flown_vertical_8, 7, 50, compplot, color='grey')
compplot.show()

v8plot.show()
gbplot.show()

compplot2 = plotelms(makegb(), 7, 50, color='orange')
compplot2 = plotelms(flown_golfball, 7, 50, compplot2, color='grey')
compplot2.show()




