import numpy
import unittest

from src.landscape import Mountain, Road, RoadNetwork
from src.height_map import HeightMap
from src.feature_tree import FeatureTree

import shapely.geometry as geom
from PIL import Image

from tests.test_feature_tree import FeatureTest


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


class TestRoads(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRoads, self).__init__(*args, **kwargs)

        self.background = FeatureTest(100, "notall", 1)
        self.r1 = Road([(40,40), (70,50)], 10, 100)
        self.r2 = Road([(20,20), (60,60), (20, 70)], 10, 100)

    def test_basic_road(self):
        hm1 = HeightMap(100, 100, self.r2.z)
        hm1.export("mroad1.png")

        original = Image.open("tests/img/mroad1.png")
        gen = Image.open("mroad1.png")
        self.assertEqual(original, gen)

    def test_two_roads(self):
        tree = FeatureTree([self.background, self.r1, self.r2])
        hm2 = HeightMap(80, 80, tree.z)
        
