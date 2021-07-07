from flightplotting.model import OBJ
import numpy as np
from geometry import Point, Quaternion, Transformation, Coord, GPSPosition

obj = OBJ.from_obj_file('data/models/ColdDraftF3APlane.obj').transform(Transformation(
    Point(0.75, 0, 0), Quaternion.from_euler(Point(np.pi, 0, -np.pi/2))
))