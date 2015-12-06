class Feature():
    """The Feature class. Things like landscapes, water, ... will inherit from this call"""

    coord_x
    coord_y
        """Center coordinates"""

    radius
        """Feature radius"""

    def __init__(self):
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
