from logging import log
from flightdata.fields import Field
import streamlit as st

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from flightanalysis import Section, FlightLine, Schedule
from flightanalysis.flightline import Box
from flightdata import Flight, Fields
from flightplotting.traces import meshes, cgtrace, tiptrace, boxtrace

from flightplotting.model import OBJ
from geometry import Point, Quaternion, Transformation, Coord
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
    col1, col2 = st.beta_columns(2)
    scan_folder = col1.text_input("folder to scan", "/media/")
    if col2.button("scan"):
        register.register_folder(Path(scan_folder))

    bdb = st.checkbox("select from db")

    fp = st.file_uploader("select bin file", "BIN")

if bdb:
    sumdf = register.summary().iloc[::-1]
    st.dataframe(sumdf)
    logid = st.number_input("enter log id", 0, sumdf.id.max(), register.current_log().id)
    if st.button("confirm"):
        register.set_current(logid)

if fp:
    log = register.register_log(fp)
else:
    log = register.current_log()

loading = st.empty()
loading.text("reading log .....")

@st.cache
def read_log(csv):
    return Flight.from_csv(csv)

if not os.path.exists(log.csv_file):
    flight = log.flight()
else:
    flight = read_log(log.csv_file)

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

@st.cache(hash_funcs={Coord: str})
def get_section(flight, flightline):
    return Section.from_flight(flight, flightline)

seq = get_section(flight, flightline)

loading.empty()

with st.sidebar.beta_expander("Plot Controls"):
    npoints = st.number_input("Number of Models", 0, 100, value=40)
    scale = st.number_input("Model Scale Factor", 1.0, 50.0, value=5.0)
    scaled_obj = obj.scale(scale)
    showmesh = st.checkbox("Show Models", True)

    cg_trace = st.checkbox("Show CG Trace", False)
    ttrace = st.checkbox("Show Tip Trace", True)
    btrace = st.checkbox("Show Box Trace", True)

    perspective = st.checkbox("perspective", True)



plot_range = st.slider(
    "plot range", 0.0, flight.duration, (0.0, flight.duration))


with st.sidebar.beta_expander("Sequence Setup"):
    col1, col2 = st.beta_columns(2)
    sequence = col1.text_input("Enter Sequence Name", log.sequence.name if log.sequence else "Unknown")
    if col2.button("save sequence selection"):
        register.set_sequence(log, sequence)

    direction = col1.radio("entry direction", ["left", "right"], 0)
    if col2.button("save entry direction"):
        register.set_direction(log, direction)

    @st.cache
    def read_schedule(name, dir):
        return Section.from_schedule(Schedule.from_json("FlightAnalysis/schedules/{}.json".format(name)), 170.0, dir)

    start = st.number_input("start", 0.0, seq.data.index[-1], plot_range[0])
    stop = st.number_input("end", 0.0, seq.data.index[-1], plot_range[1])

    rundtw = st.checkbox("run_dtw")

if rundtw:
    template = read_schedule(sequence, direction)

    @st.cache
    def do_dtw(sec, temp):
        return Section.align(sec.subset(start, stop), temp)

    dist, aligned = do_dtw(seq, template)

    with st.sidebar.beta_expander("manoeuvre selection"):
        manoeuvre = st.radio("select manoeuvre", aligned.manoeuvre.unique())
    plotsec = Section(aligned.data.loc[aligned.manoeuvre==manoeuvre, :])

    # TODO regenerate scaled template here
    
    perfect = Section(template.data.loc[template.manoeuvre==manoeuvre, :])  
    showtemplate = st.checkbox("show template")
else:
    plotsec = seq.subset(*plot_range)
    showtemplate = False


def _make_plot_data(sec,  npoints, showmesh, cgtrace, ttrace, color="grey"):
    traces = []
    if showmesh:
        traces += [mesh for mesh in meshes(scaled_obj, npoints, sec, color)]
    if cg_trace:
        traces += [cgtrace(sec)]
    if ttrace:
        traces += tiptrace(sec, scale * 1.85)
    if btrace:
        traces += boxtrace()
    return traces

def make_plot_data():
    traces = _make_plot_data(plotsec, npoints, showmesh, cgtrace, ttrace, "grey") 
    if showtemplate:
        traces += _make_plot_data(perfect, npoints, showmesh, cgtrace, ttrace, "orange") 
    return traces

st.plotly_chart(
    go.Figure(
        make_plot_data(),
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