import numpy
import unittest
from src.landscape import Mountain
import shapely.geometry as geom


class TestMountain(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMountain, self).__init__(*args, **kwargs)
        self.m1 = Mountain(1, 0)

    def test_z(self):
        z = self.m1.z((0, 0))
        out_of_radius_1 = self.m1.center_pos + numpy.array((self.m1.radius + 1, 0))
        out_of_radius_2 = self.m1.center_pos + numpy.array((0, self.m1.radius + 1))
        out_of_radius_3 = self.m1.center_pos + numpy.array((1, self.m1.radius))
        self.assertEqual(self.m1.z(out_of_radius_1), 0)
        self.assertEqual(self.m1.z(out_of_radius_2), 0)
        self.assertEqual(self.m1.z(out_of_radius_3), 0)

    def test_influence_weight(self):
        self.assertEqual(self.m1.influence_weight((0, 0)), 1)
