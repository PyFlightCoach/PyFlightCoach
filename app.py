from logging import log
from flightdata.fields import Field
import streamlit as st

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from flightanalysis import Section, State, FlightLine
from flightanalysis.flightline import Box
from flightdata import Flight, Fields
from flightplotting.traces import meshes, cgtrace, tiptrace, boxtrace

from flightplotting.model import OBJ
from geometry import Point, Quaternion, Transformation
import os
import tkinter as tk
from pyflightcoach.log_register.access import new_session
from pyflightcoach.log_register.tables import Log
from pathlib import Path
from json import load

register = new_session()

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

obj = OBJ.from_obj_file('data/models/ColdDraftF3APlane.obj').transform(Transformation(
    Point(0.75, 0, 0), Quaternion.from_euler(Point(np.pi, 0, -np.pi/2))
))

with st.sidebar.beta_expander("log selection"):
    scan_folder = st.text_input("folder to scan", "/media/")
    if st.button("scan folder"):
        register.register_folder(Path(scan_folder))

    fp = st.file_uploader("select bin file", "BIN")
    if fp:
        log = register.register_log(fp)
    else:
        log = register.latest_log()

loading = st.empty()
loading.text("reading log .....")

flight = log.flight()  

with st.sidebar.beta_expander("flightline setup"):
    fltype = st.radio("method", ["json", "covariance", "initial position"], 0)
    if fltype == "json":
        fp2 = st.file_uploader("select flightline json", "json")
        if not fp2:
            box = Box.from_json('examples/notebooks/flightlines/gordano_box.json')
        else:
            box = Box(**load(fp2))
        flightline = FlightLine.from_box(box)
    elif fltype=="covariance":
        flightline = FlightLine.from_covariance(flight)
    elif fltype=="initial position":
        flightline = FlightLine.from_initial_position(flight)

loading.text("moving to flightline .....")


seq = Section.from_flight(flight, flightline)

loading.empty()

npoints = st.sidebar.number_input("Number of Models", 0, 100, value=40)
scale = st.sidebar.number_input("Model Scale Factor", 1.0, 50.0, value=5.0)
scaled_obj = obj.scale(scale)
showmesh = st.sidebar.checkbox("Show Models", True)

cg_trace = st.sidebar.checkbox("Show CG Trace", False)
ttrace = st.sidebar.checkbox("Show Tip Trace", True)
btrace = st.sidebar.checkbox("Show Box Trace", True)

perspective = st.sidebar.checkbox("perspective", True)



plot_range = st.slider(
    "plot range", 0.0, flight.duration, (0.0, flight.duration))


def make_plot_data(seq, plot_range, npoints, showmesh, cgtrace, ttrace):
    sec = seq.subset(*plot_range)
    traces = []
    if showmesh:
        traces += [mesh for mesh in meshes(scaled_obj, npoints, sec, 'orange')]
    if cg_trace:
        traces += [cgtrace(sec)]
    if ttrace:
        traces += tiptrace(sec, scale * 1.85)
    if btrace:
        traces += boxtrace()
    return traces


st.plotly_chart(
    go.Figure(
        make_plot_data(seq, plot_range, npoints, showmesh, cgtrace, ttrace),
        layout=go.Layout(
            template="flight3d+judge_view",
            height=800,
            scene_camera=dict(
                projection=dict(
                    type='perspective' if perspective else 'orthographic')
            ))
    ),
    use_container_width=True
)


sequence = st.sidebar.text_input("Enter Sequence Name", log.sequence.name if log.sequence else "Unknown")
if st.sidebar.button("save sequence selection"):
    register.set_sequence(log, sequence)


with st.beta_expander("Scores"):
    seqdf = pd.read_csv("data/sequences/{}.csv".format(sequence))
    st.dataframe(seqdf)