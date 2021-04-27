from flightdata import Flight
from flightanalysis import Section, FlightLine
from flightplotting.plots import meshes, tiptrace, create_3d_plot
from flightplotting.model import OBJ
from geometry import Transformation, Quaternion
import plotly.graph_objects as go


import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from geometry import Point, Points

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def elmdf(row, n):
    df = pd.DataFrame(data=[row for i in range(
        n)], columns="roll_rate,pitch_rate,yaw_rate,element".split(","))
    return df


generated_vertical_8 = pd.concat(
    [
        elmdf([0.0, 0.0, 0.0,      "elm1_entry_line"], 20),
        elmdf([1.5, 0.0, 0.0,      "elm2_half_roll"], 20),
        elmdf([0.0, -0.5, 0.0,     "elm3_outside_loop"], 20),
        elmdf([0.0, 0.5, 0.0,      "elm4_inside_loop"], 20),
        elmdf([-1.5, 0.0, 0.0,     "elm5_half_roll"], 20),
        elmdf([0.0, 0.0, 0.0,      "elm6_exit_line"], 20)
    ], ignore_index=True)

_rolldf = pd.DataFrame(
    np.column_stack([-np.full(20, 0.2), -0.5*np.cos(np.linspace(
        0, np.pi, 20)), -0.5*np.sin(np.linspace(0, np.pi, 20))]),
    columns="roll_rate,pitch_rate,yaw_rate".split(","))
_rolldf["element"] = "elm5_integrated_roll"

generated_golfball = pd.concat(
    [
        elmdf([0.0, 0.0, 0.0,      "elm1_entry_line"], 20),
        elmdf([0.0, -0.5, 0.0,      "elm2_45_push"], 20),
        elmdf([0.0, 0.0, 0.0,     "elm3_45_line"], 20),
        elmdf([0.0, -0.5, 0.0,      "elm4_1/8_outside_loop"], 20),
        _rolldf,
        elmdf([0.0, 0.5, 0.0,      "elm6_1/8_inside_loop"], 20),
        elmdf([0.0, 0.0, 0.0,     "elm7_45_line"], 20),
        elmdf([0.0, 0.5, 0.0,      "elm8_45_pull"], 20),
        elmdf([0.0, 0.0, 0.0,      "elm9_exit_line"], 20),
    ], ignore_index=True)


def do_dtw(flown, generated):
    x = generated.iloc[:, [0, 1, 2]].to_numpy()
    y = flown.brvel.to_numpy()

    distance, path = fastdtw(x, y, dist=euclidean)
    return flown.data.reset_index().join(
        pd.DataFrame(path, columns="generated,flight".split(",")).set_index(
            "flight").join(generated.element, on="generated")
    )


def plotresults(flown, segments):
    fig = go.Figure()

    tt = tiptrace(flown, 10)

    fig.add_trace(tt[0])
    fig.add_trace(tt[1])
    # fig.update_traces(line=dict(dash='dash'))
    fig.update_traces(line=dict(width=3))

    for tr in fig['data']:
        tr['showlegend'] = False

    for segname in segments["element"].unique():
        seg = segments[segments.element == segname]
        fig.add_trace(go.Scatter3d(x=seg.x, y=seg.y, z=seg.z,
                      mode='lines', line=dict(width=6), name=segname))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(aspectmode='data')
    )
    fig.update_layout(legend=dict(
        font=dict(size=20),
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig


flight = Flight.from_csv("data/logs/00000136.csv")
sec = Section.from_flight(flight, FlightLine.from_covariance(flight))


flown_vertical_8 = sec.subset(102, 147)
flown_golfball = sec.subset(250, 280)


v8segments = do_dtw(flown_vertical_8, generated_vertical_8)
gbsegments = do_dtw(flown_golfball, generated_golfball)

v8plot = plotresults(flown_vertical_8, v8segments)
gbplot = plotresults(flown_golfball, gbsegments)

v8plot.show()
gbplot.show()
