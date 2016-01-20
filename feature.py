import shapely.geometry as geom


class Feature():
    """The Feature class.
    Things like landscapes, water, ... will inherit from this call"""

    def __init__(self):
        """coord_x, coord_y is the "middle-point" ?
        Shape is the 2D-shape (x & y axis) of our feature"""
        self.coord_x = 0
        self.coord_y = 0

        self.shape = geom.Polygon()

    def intersect(self, feature2):
        """Returns *true* if the feature intersects *feature2*.
        NB: this should be symmetric."""
        return self.shape.intersects(feature2.shape)

    def z(self, coord):
        """Export the heightmap given a feature and a plane coordinate"""
        pass

    def influence_weight(self, coord):
        """Export influence heightmap"""
        pass


class FeatureLine(Feature):
    """Feature corresponding to a linear zone: new functions to manipulate the curve of the feature."""

    def __init__(self, points, thickness):
        """Creates a line following the given points with a certain thickness."""
        self.line = geom.LineString(points)
        self.thickness = thickness
        self._update_shape()

    def _update_shape(self):
        """Updates the shape to match the current path and thickness."""
        self.shape = self.line.buffer(self.thickness, cap_style=geom.CAP_STYLE.flat, join_style=geom.JOIN_STYLE.round)
