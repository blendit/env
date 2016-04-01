import numpy as np
import shapely.geometry as geom
from scipy.integrate import odeint

from src.feature import Feature


class Urban(Feature):
    """Urban class

    Road generation
    ===============

    The roads are generated as the stream lines of the eigenvectors of a tensor
    field (essentially a function from points to 2x2 matrices). The main
    component of the field is computed from a linear combination of basic
    fields, weighted by an exponential decay in the square of the distance to
    their center. There are 4 types of basic fields:
        1. Grid
        2. Radial
        3. Boundary
        4. Height
    See the documentation of the corresponding classes for details.

    Note: all basic fields are symmetric hence so is the final field, which
    implies that streets always cross perpendicularly (can be modified later if
    needed).

    Reference: [CEW+08]
        Chen G., Esch G., Wonka P., Müller P., Zhang E.: Interactive procedural street modeling.
        ACM Transactions on Graphics (SIGGRAPH) 27, 3 (2008), 103:1–103:10.
        http://www.peterwonka.net/Publications/pdfs/2008.SG.Chen.InteractiveProceduralStreetModeling.pdf

    """

    def __init__(self, shape, road_fields=None):
        self.shape = shape
        if road_fields is None:
            road_fields = []
        self.road_fields = road_fields

    def z(self, coord):
        return 0

    def influence(self, coord):
        if self.shape.contains(coord):
            return 1
        else:
            return 0

    def tensor(self, point):
        """Sum of all fields at the given point"""
        tensor = np.zeros((2, 2))
        for field in self.road_fields:
            tensor += field.tensor(point)
        return tensor

    def draw_street(self, start, length, step, major=True, reverse=False):
        """Draw a street as a stream line of the tensor field."""
        vect_index = int(major)
        sign = (-1) ** int(reverse)
        def stream_vector(point, _):
            return sign * np.linalg.eigh(self.tensor(point))[1][vect_index]
        times = np.arange(0, length, step)
        return geom.LineString(odeint(stream_vector, start, times))


class TensorField:
    """Base class for basic tensor fields."""

    def tensor(self, pos):
        """Return the value of the tensor field at a given point"""
        return np.zeros((2, 2))


def tensor_from_vector(vector):
    """Compute the tensor following the direction of a given vector.

    Uses equation (1) from [CEW+08], but without scaling by the norm of the
    vector.
    """
    x, y = vector
    angle = 2 * np.arctan2(y, x)
    a, b = np.cos(angle), np.sin(angle)
    return np.array(((a, b), (b, - a)))


class GridField(TensorField):
    """Tensor field creating a grid along a certain direction.

    Given a direction vector vec, the generated field (without decay) is a
    constant field with vec as major eigenvector.
    """

    def __init__(self, vector, center, decay):
        self.vector = vector
        self.center = center
        self.decay = decay
        self._tensor = tensor_from_vector(vector)

    def tensor(self, pos):
        dist = self.center.distance(geom.Point(pos))
        return self._tensor * np.exp(dist * dist * self.decay)


class RadialField(TensorField):
    """Tensor field creating a radial pattern around its center"""

    def __init__(self, center, decay):
        self.center = np.array(center)
        self.decay = decay

    def tensor(self, pos):
        x, y = v = self.center - pos
        a, b = y * y - x * x, -2 * x * y
        return np.array(((a, b), (b, - a))) * np.exp(np.dot(v, v) * self.decay)


class BoundaryField(TensorField):
    """Tensor field that adapts to a polyline boundary.

    This field is a combination of grid fields following each segment of the
    boundary and decaying with the distance to the segment (not to a particular
    point of it).
    """

    def __init__(self, boundary, decay):
        self.boundary = []
        self.decay = decay
        # Split the boundary into a list of segments
        start = None
        for end in np.array(boundary):
            if start is not None:
                self.boundary.append(geom.LineString((start, end)))
            start = end

    def tensor(self, pos):
        tensor = np.zeros((2, 2))
        for seg in self.boundary:
            start, end = np.array(seg)
            dist = seg.distance(pos)
            tensor += tensor_from_vector(end - start) * np.exp(dist * dist * self.decay)
        return tensor


class HeightField(TensorField):
    """Tensor field following an height map.

    The major stream lines of this field are at constant height, i.e.
    perpendicular to the gradient, and the minor stream lines follow the
    gradient.

    To simplify the computations, the field is parametered by the *gradient* of
    the height map, not by the height map itself.
    """

    def __init__(self, gradient):
        self.gradient = gradient

    def tensor(self, pos):
        dHx, dHy = self.gradient(pos)
        return tensor_from_vector((dHy, - dHx))
