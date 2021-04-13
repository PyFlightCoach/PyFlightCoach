from logging import log
from flightdata.fields import Field
import streamlit as st

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from flightanalysis import Section, State, FlightLine
from flightdata import Flight, Fields
from flightplotting.plots import meshes, trace, tiptrace, boxtrace
from flightplotting.model import OBJ
from geometry import Point, Quaternion, Transformation
import os
import tkinter as tk


st.markdown(

    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
    }}
</style>
""",
    unsafe_allow_html=True,
)


fp = st.sidebar.file_uploader("select log csv", "csv")
bin = Flight.from_csv(fp)

# st.sidebar.text(fp.name)

flightline_type = st.sidebar.radio("flightline definition", [
                                   "covariance", "initial_position"], )


@st.cache
def load_data(bin):
    if flightline_type == "covariance":
        return bin, Section.from_flight(bin, FlightLine.from_covariance(bin))
    elif flightline_type == "initial_position":
        return bin, Section.from_flight(bin, FlightLine.from_initial_position(bin))


flight, seq = load_data(bin)

obj = OBJ.from_obj_file('data/models/ColdDraftF3APlane.obj').transform(Transformation(
    Point(0.75, 0, 0), Quaternion.from_euler(Point(np.pi, 0, -np.pi/2))
))


npoints = st.sidebar.number_input("Number of Models", 0, 100, value=40)
scale = st.sidebar.number_input("Model Scale Factor", 1.0, 50.0, value=5.0)

scaled_obj = obj.scale(scale)

showmesh = st.sidebar.checkbox("Show Models", True)
cgtrace = st.sidebar.checkbox("Show CG Trace", False)
ttrace = st.sidebar.checkbox("Show Tip Trace", True)
btrace = st.sidebar.checkbox("Show Box Trace", True)


plot_range = st.slider(
    "plot range", 0.0, flight.duration, (0.0, flight.duration))


def make_plot_data(seq, plot_range, npoints, showmesh, cgtrace, ttrace):
    sec = seq.subset(*plot_range)
    traces = []
    if showmesh:
        traces += [mesh for mesh in meshes(scaled_obj, npoints, sec)]
    if cgtrace:
        traces += [trace(sec)]
    if ttrace:
        traces += tiptrace(sec, scale * 1.85)
    if btrace:
        traces += boxtrace()
    return traces


st.plotly_chart(
    go.Figure(
        make_plot_data(seq, plot_range, npoints, showmesh, cgtrace, ttrace),
        layout=go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            scene=dict(aspectmode='data'),
            height=800,
            scene_camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0, y=-2.5, z=0)
            )
        )),
    use_container_width=True
)

