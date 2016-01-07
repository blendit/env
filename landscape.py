import numpy
from numpy import random
import shapely.geometry as geom

from feature import Feature, FeatureLine


class Landscape(Feature):
    """Landscape class"""

    def __init__(self):
        pass


class Mountain(Landscape):
    """A mountain"""

    default_noise_grid = random.normal(0, 1, 100).reshape(10, 10)

    def default_noise(coord):
        return default_noise_grid[coord]

    def __init__(self, radius, center_z, center_pos=(0, 0), freqs=[0.1, 0.2], amplis=[1, 2], noise=default_noise):
        """NB: len(freqs) should equal len(amplis)"""
        self.radius = radius
        center = geom.Point(*center_pos)
        self.center_pos = numpy.array(center)
        self.center_z = center_z
        # By default, buffer approximates the circle with a regular 16-gon
        self.shape = center.buffer(radius)
        self.noise = noise
        self.freqs = freqs
        self.amplis = amplis

    def z(self, coord):
        """Generation of a height given a plane coordinate. Formula from [GGP+15], subsection 4.1"""
        return self.center_z + sum(a_i * self.noise((self.center_pos - coord) * s_i) for (a_i, s_i) in zip(self.amplis, self.freqs))

    def influence_weight(self, coord):
        return 1


class Roads(FeatureLine):
    """Roads class"""

    def __init__(self):
        pass


class Vegetation(Feature):
    """Vegatation class"""

    def __init__(self):
        pass
