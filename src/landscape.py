import numpy
from numpy import random
import shapely.geometry as geom

from src.feature import Feature, FeatureLine


class Landscape(Feature):
    """Landscape class"""

    def __init__(self):
        pass


class Mountain(Landscape):
    """A mountain"""

    def __init__(self, radius, center_z, center_pos=(0, 0), freqs=[0.1, 0.2], amplis=[1, 2], noise=None):
        """NB: len(freqs) should equal len(amplis)"""
        if(noise is None):
            self.default_noise_grid = random.normal(0, 1, 100).reshape(10, 10)
            self.noise = self.default_noise
        else:
            self.noise = noise
        self.radius = radius
        center = geom.Point(*center_pos)
        self.center_pos = numpy.array(center)
        self.center_z = center_z
        # By default, buffer approximates the circle with a regular 16-gon
        self.shape = center.buffer(radius)
        self.freqs = freqs
        self.amplis = amplis

    def default_noise(self, coord):
        return self.default_noise_grid[int(coord[0]), int(coord[1])]

    def z(self, coord):
        """Generation of a height given a plane coordinate. Formula from [GGP+15], subsection 4.1"""
        x = coord[0] - self.center_pos[0]
        y = coord[1] - self.center_pos[1]
        if(x**2 + y**2 <= self.radius):
            return self.center_z + sum(a_i * self.noise((self.center_pos - numpy.array(coord)) * s_i) for (a_i, s_i) in zip(self.amplis, self.freqs))
        else:
            return 0

    def influence_weight(self, coord):
        return 1


class Road(FeatureLine):
    """A single road"""

    def __init__(self, points, thickness, height=0):
        """- *points* is the set of oints of the road
        - *thickness* is the width of the road
        - *height* (default **0**) is the constant height of the road"""
        super(Road, self).__init__(points, thickness)
        
        self.height = height

    def z(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return self.height
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0


class RoadNetwork(Feature):
    """A network of roads"""

    def __init__(self):
        super(RoadNetwork, self).__init__()
        

class Vegetation(Feature):
    """Vegatation class"""

    def __init__(self):
        pass
