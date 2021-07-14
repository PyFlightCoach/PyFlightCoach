from logging import log
import streamlit as st

import plotly.graph_objects as go
from flightanalysis import Section, FlightLine
from flightanalysis.flightline import Box
from flightanalysis.schedule import p21#, f21

from flightdata import Flight
from flightplotting.traces import meshes, cgtrace, tiptrace, boxtrace, ribbon
import flightplotting.templates
from geometry import Coord, GPSPosition
import os
from pyflightcoach.log_register.access import new_session
from pathlib import Path
from json import load
from pyflightcoach.model import obj

# TODO new versions of streamlit give session state and callbacks which should simplify things

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
################################################################
### LOG SELECTION #################################
################################################################

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


################################################################
### FLIGHTLINE SELECTION #################################
################################################################

if log.boxreg:
    box = log.boxreg.box
else:
    box = Box.from_initial(flight)  # TODO replace with select closest box from DB or last used or something


with st.sidebar.beta_expander("flightline setup"):
    bdb_box = st.checkbox("Select from DB", False)

    fp2 = st.file_uploader("select flightline json", "json")
    if fp2:
        box = Box.from_json(fp2)
        if st.button("save box for flight"):
            register.set_box(log, box)

if bdb_box:
    sumdf_box = register.box_summary().iloc[::-1]
    st.dataframe(sumdf_box)
    boxid = st.number_input("enter box id", 0, sumdf_box.id.max(), sumdf_box.id.max())
    if st.button("confirm box"):
        register.set_box(log, boxid)


flightline = FlightLine.from_box(box,  GPSPosition(**flight.origin()))

loading.text("moving to flightline .....")

@st.cache(hash_funcs={Coord: str})
def get_section(flight, flightline):
    del st.session_state['seq_begin']
    del st.session_state['seq_end']
    return Section.from_flight(flight, flightline)

seq = get_section(flight, flightline)

loading.empty()


################################################################
### PLOT CONTROLS #################################
################################################################


with st.sidebar.beta_expander("Plot Controls"):
    npoints = st.number_input("Number of Models", 0, 100, value=40)
    scale = st.number_input("Model Scale Factor", 1.0, 50.0, value=5.0)
    scaled_obj = obj.scale(scale)
    showmesh = st.checkbox("Show Models", False)

    cg_trace = st.checkbox("Show CG Trace", False)
    ttrace = st.checkbox("Show Tip Trace", True)
    btrace = st.checkbox("Show Box Trace", True)
    rtrace = st.checkbox("Show Ribbon Trace", True)

    perspective = st.checkbox("perspective", True)


if 'seq_begin' not in st.session_state:
    if log.start_index:
        st.session_state['seq_begin'] = float(seq.data.index[log.start_index])
    else:
        st.session_state['seq_begin'] = 100.0 if float(seq.data.index[-1]) > 100 else 0.0

if 'seq_end' not in st.session_state:
    if log.end_index:
        st.session_state['seq_end'] = float(seq.data.index[log.end_index])
    else:
        st.session_state['seq_end'] = 500.0 if float(seq.data.index[-1]) > 500 else 0.0


plot_range = st.slider(
    "plot range", 0.0, flight.duration, (st.session_state['seq_begin'], st.session_state['seq_end']))

################################################################
### SEQUENCE SELECTION #################################
################################################################

with st.sidebar.beta_expander("Sequence Setup"):
    col1, col2 = st.beta_columns(2)

    sequence = col1.text_input("Enter Sequence Name", log.sequence.name if log.sequence else "Unknown")

    if col2.button("save sequence selection"):
        register.set_sequence(log, sequence)

    direction = col1.radio("entry direction", ["left", "right"], 0)
    if col2.button("save entry direction"):
        register.set_direction(log, direction)
    

    if st.button("copy slider start value"):
        st.session_state['seq_begin'] = plot_range[0]
    
    st.session_state['seq_begin'] = st.number_input("start", 0.0, seq.data.index[-1], st.session_state['seq_begin'])

    if st.button("copy slider end value"):
        st.session_state['seq_end'] = plot_range[1]
        
    st.session_state['seq_end'] = st.number_input("end", 0.0, seq.data.index[-1], st.session_state['seq_end'])

    if st.button("save sequence start & end"):
        register.set_start_end(log, seq.data.index.get_loc(st.session_state['seq_begin'], method="nearest"), seq.data.index.get_loc(st.session_state['seq_end'], method="nearest"))

    rundtw = st.checkbox("run_dtw")


################################################################
### SEQUENCE ALIGNMENT #################################
################################################################


if rundtw:
    #if sequence == "P21":
    sched = p21
    #elif sequence == "F21":
    #    sched = f21
    
    @st.cache
    def read_schedule(sched, dir):
        return sched.create_template(dir, 170.0)

    template = read_schedule(sched, direction)

    @st.cache
    def do_dtw(sec, temp):
        return Section.align(sec.subset(st.session_state['seq_begin'], st.session_state['seq_end']), temp)

    dist, aligned = do_dtw(seq, template)

    # TODO regenerate scaled template here

    with st.sidebar.beta_expander("manoeuvre selection"):
        man = st.radio("select manoeuvre", [man.name for man in sched.manoeuvres])
        manoeuvre = sched.manoeuvre(man)
        
    plotsec = manoeuvre.get_data(aligned)
    perfect = manoeuvre.get_data(template)
    showtemplate = st.checkbox("show template")
else:
    plotsec = seq.subset(*plot_range)
    showtemplate = False


################################################################
### PLOT #################################
################################################################

def _make_plot_data(sec,  npoints, showmesh, cg_trace, ttrace, color="grey"):
    traces = []
    if showmesh:
        traces += [mesh for mesh in meshes(scaled_obj, npoints, sec, color)]
    if cg_trace:
        traces += [cgtrace(sec)]
    if ttrace:
        traces += tiptrace(sec, scale * 1.85)
    if rtrace:
        traces += ribbon(sec, scale * 1.85)
    return traces

def make_plot_data():
    traces = _make_plot_data(plotsec, npoints, showmesh, cg_trace, ttrace, "grey") 
    if showtemplate:
        traces += _make_plot_data(perfect, npoints, showmesh, cg_trace, ttrace, "orange") 
    if btrace:
        traces += boxtrace()
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