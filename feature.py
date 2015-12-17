from sympy import Polygon


class Feature():
    """The Feature class.
    Things like landscapes, water, ... will inherit from this call"""

    def __init__(self):
        coord_x = 0
        coord_y = 0
        
        pass

    def intersect(self, feature2):
        """Intersection of two features (self and feature 2). NB: this should be symmetric """
        pass

    def z(self, coord):
        """Export the heightmap given a feature and a plane coordinate"""
        pass

    def influence_weight(self, coord):
        """Export influence heightmap"""
        pass


class FeatureLine(Feature):
    """Feature corresponding to a linear zone: new functions to manipulate the curve of the feature."""
