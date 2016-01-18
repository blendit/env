from shapely.geometry import Polygon


class Feature():
    """The Feature class.
    Things like landscapes, water, ... will inherit from this call"""

    def __init__(self):
        """coord_x, coord_y is the "middle-point" ?
        Shape is the 2D-shape (x & y axis) of our feature"""
        self.coord_x = 0
        self.coord_y = 0

        self.shape = Polygon()

    def intersect(self, feature2):
        """Returns *true* if the feature intersects *feature2*.
        NB: this should be symmetric."""
        return self.shape.intersects(feature2.shape)

    def z(self, coord):
        """Export the heightmap given a feature and a plane coordinate"""
        pass

    def influence(self, coord):
        """Export influence heightmap"""
        pass

    def interaction(self):
        """Give the interaction type of the feature with other features.
        Can be:
        * "blend" (default): the mean with the other features
        * "replace": one feature erase one other (**only two features**)
        * "addition": add one feature over another (**only two features**)."""
        return "Blend"


class FeatureLine(Feature):
    """Feature corresponding to a linear zone: new functions to manipulate the curve of the feature."""
    def interaction(self):
        """Give the interaction type of the feature with other features.
        Can be:
        * "blend": the mean with the other features
        * "replace" (default for FeatureLine): one feature erase one other (**only two features**)
        * "addition": add one feature over another (**only two features**)."""
        return "Replace"
