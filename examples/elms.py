
from flightanalysis import Section
from geometry import Point, Quaternion, Transformation
import numpy as np


def makev8(diam=160, hs=240, ds=180):
    box_height = diam*2
    initial = Transformation(\
        Point(-140, ds, hs),
        Quaternion.from_euler(Point(0, 0, 0))
    )
    line = Section.from_line(initial, 30, 60)
    roll = Section.from_line(line.get_state_from_index(-1).transform, 30, 80).superimpose_roll(0.5)
    radius = Section.from_loop(roll.get_state_from_index(-1).transform, 30, 1.0, box_height / 4)
    radius2 = Section.from_loop(radius.get_state_from_index(-1).transform, 30, -1.0, box_height / 4)
    roll2 = Section.from_line(radius2.get_state_from_index(-1).transform, 30, 80).superimpose_roll(0.5)
    line2 = Section.from_line(roll2.get_state_from_index(-1).transform, 30, 60).superimpose_roll(0.5)
    return Section.stack([line, roll, radius, radius2, roll2, line2])


def makegb(diam=160, hs=50, ds=180):
    initial = Transformation(
        Point(2.1*diam * np.pi / 5, ds, hs),
        Quaternion.from_euler(Point(0.0, 0.0, np.pi))
    )

    elms = []

    # entry line
    # 15 * pi * 2 meters
    elms.append(Section.from_line(initial, 30, 100))
    # 45 push
    elms.append(Section.from_loop(elms[-1].get_state_from_index(-1).transform, 30, 0.125, 80.0, False))
    # 45 upline
    elms.append(Section.from_line(elms[-1].get_state_from_index(-1).transform, 30, 100.0))
    # 45 push
    elms.append(Section.from_loop(elms[-1].get_state_from_index(-1).transform, 30, 0.125, 80.0, False))

    # integrated roll
    elms.append(Section.from_loop(elms[-1].get_state_from_index(-1).transform, 30, 0.5, 80.0, False).superimpose_roll(0.5))
    # 45 pull
    elms.append(Section.from_loop(elms[-1].get_state_from_index(-1).transform, 30, -0.125, 80.0, False))

    # 45 downline
    elms.append(Section.from_line(elms[-1].get_state_from_index(-1).transform, 30, 100.0))
    # 45 pull
    elms.append(Section.from_loop(elms[-1].get_state_from_index(-1).transform, 30, -0.125, 80.0, False))

    # exit line
    elms.append(Section.from_line(elms[-1].get_state_from_index(-1).transform, 30, 30.0))
    return Section.stack(elms)





