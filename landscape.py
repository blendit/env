from numpy import random

from feature import Feature


class Landscape(Feature):
    """Landscape class"""

    def __init__(self):
        pass


class Mountain(Landscape):
    """A mountain"""

    default_noise_grid = random.normal(0, 1, 100).reshape(10, 10)

    def default_noise(coord):
        return default_noise_grid[coord]

    def __init__(self, r, center_z, center_coord=(0, 0), noise=default_noise, f=[0.1, 0.2], a=[1, 2]):
        """NB: len(f) should equal len(a)"""
        radius = r
        cz = center_z
        noise_gen = default_noise
        frequencies = f
        amplitudes = a

    def z(self, coord):
        return cz + sum(a_i * noise_gen((coord[0] - center_coord[0], coord[1] - center_coord[1])) * s_i for (a_i, s_i) in zip(a, f))


class Roads(Feature):
    """Roads class"""

    def __init__(self):
        pass


class Vegetation(Feature):
    """Vegatation class"""

    def __init__(self):
        pass