
from flightanalysis import Section, State, FlightLine
from geometry import Point, Quaternion, Transformation, Points, Quaternions
import numpy as np
import plotly.graph_objects as go
from flightplotting.plots import tiptrace, meshes
from flightplotting.model import OBJ


def makev8(diam=160, hs=240, ds=180):

    initial = State(
        Point(-diam * np.pi / 5, ds, hs),
        Quaternion.from_euler(Point(0, 0, 0)),
        Point(diam * 10 * np.pi / 100, 0, 0),
        Point(np.pi / 2, 0, 0)
    )
    line = Section.from_line(initial, np.linspace(0, 2, 100))

    last_state = line.get_state_from_index(-1)
    last_state.brvel = Point(0, -np.pi / 5, 0)

    radius = Section.from_radius(last_state, np.linspace(0, 10, 200))

    last_state = radius.get_state_from_index(-1)
    last_state.brvel = Point(0, np.pi / 5, 0)

    radius2 = Section.from_radius(last_state, np.linspace(0, 10, 200))

    last_state = radius2.get_state_from_index(-1)
    last_state.brvel = Point(np.pi / 2, 0, 0)

    line2 = Section.from_line(last_state, np.linspace(0, 2, 100))

    return Section.stack([line, radius, radius2, line2])


def makegb(diam=160, hs=50, ds=180):
    initial = State(
        Point(2.1*diam * np.pi / 5, ds, hs),
        Quaternion.from_euler(Point(0.0, 0.0, np.pi)),
        Point(diam * np.pi / 10, 0.0, 0.0),
        Point(0.0, 0.0, 0.0)
    )

    elms = []

    #entry line
    elms.append(Section.from_line(initial, np.linspace(0, 2, 100))) # 15 * pi * 2 meters
    
    #45 push
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, -np.pi / 5, 0.0)
    elms.append(Section.from_radius(last_state, np.linspace(0, 1.25, 50)))

    #45 upline
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, 0.0, 0.0)
    elms.append(Section.from_line(last_state, np.linspace(0, 2, 100)))

    #45 push
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, -np.pi / 5, 0.0)
    last_state.bvel = Point(diam * np.pi / 10, 0, 0)
    elms.append(Section.from_radius(last_state, np.linspace(0, 1.25, 50)))

    #integrated roll

    #first make the loop
    last_state = elms[-1].get_state_from_index(-1)
    elms.append(Section.from_radius(last_state, np.linspace(0, 5, 200)))
    
    #then superimpose the roll
    t=np.linspace(0, 5, 200)
    angles = Points.from_point(Point(-np.pi / 5, 0.0, 0.0), len(t)) * t
    new_att = Quaternions.from_pandas(elms[-1].att).body_rotate(angles)

    elms[-1].data.loc[:,['rw', 'rx', 'ry', 'rz']] = new_att.data

    #45 pull
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, np.pi / 5, 0.0)
    last_state.bvel = Point(diam * np.pi / 10, 0, 0)
    elms.append(Section.from_radius(last_state, np.linspace(0, 1.25, 50)))

    #45 downline
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, 0.0, 0.0)
    elms.append(Section.from_line(last_state, np.linspace(0, 2, 100)))


    #45 pull
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, np.pi / 5, 0.0)
    last_state.bvel = Point(diam * np.pi / 10, 0, 0)
    elms.append(Section.from_radius(last_state, np.linspace(0, 1.25, 50)))

    #exit line
    last_state = elms[-1].get_state_from_index(-1)
    last_state.brvel = Point(0.0, 0.0, 0.0)
    elms.append(Section.from_line(last_state, np.linspace(0, 2, 100)))

    
   



    return Section.stack(elms)




obj = OBJ.from_obj_file('data/models/ColdDraftF3APlane.obj').transform(Transformation(
    Point(0.75, 0, 0), Quaternion.from_euler(Point(np.pi, 0, -np.pi/2))
))


def plotelms(flown, scale=10, nmodels=20, fig=None, color="orange"):
    if fig is None:
        fig = go.Figure()

    tt = tiptrace(flown, scale * 1.85)

    fig.add_trace(tt[0])
    fig.add_trace(tt[1])
    # fig.update_traces(line=dict(dash='dash'))
    #fig.update_traces(line=dict(width=3))

    for tr in fig['data']:
        tr['showlegend'] = False

    for mesh in meshes(obj.scale(scale), nmodels, flown, color):
        fig.add_trace(mesh)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            aspectmode='data', 
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False)
            ),
        legend=dict(
            font=dict(size=20),
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        scene_camera=dict(
            up=dict(x=0, y=0, z=0),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=0.0, y=-1.0, z=-0.5),
            projection=dict(type='perspective')
        )
        
        #zaxis= {'showgrid': False, 'zeroline': False, 'visible': False},
    )

    return fig


#plotelms(makev8(), 7, 50).show()
