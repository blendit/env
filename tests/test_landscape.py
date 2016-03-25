import numpy
import unittest
from tests.base import FeatureTest, compare_imgs

from src.landscape import Mountain, Road, RoadNetwork, Vegetation
from src.height_map import HeightMap
from src.feature_tree import FeatureTree
from src.model import *

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


class TestRoads(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRoads, self).__init__(*args, **kwargs)

        self.background = FeatureTest(200, "notall", 1)
        self.background.shape = geom.box(10, 10, 90, 90)
        self.r1 = Road([(15, 40), (70, 30)], 3, 100)
        self.r2 = Road([(20, 20), (60, 60), (20, 70)], 10, 100)

    def test_basic_road(self):
        hm1 = HeightMap(100, 100, self.r2.z)
        hm1.export("mroad1.png")
        compare_imgs("tests/img/mroad1.png", "mroad1.png", self)

    def test_two_roads(self):
        tree = FeatureTree([self.background, self.r1, self.r2])
        hm2 = HeightMap(80, 80, tree.z)
        hm2.export("mroad2.png")
        compare_imgs("tests/img/mroad2.png", "mroad2.png", self)


class TestVegetation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gen_model = AbstractModel("test.3ds", 2, (0, 0))

    def test_shape(self):
        v1 = Vegetation(self.gen_model, (20, 20), (100, 100), 100)
        
        self.assertEqual(v1.z((10, 10)), 0)
        self.assertEqual(v1.z((50, 50)), 0)
        self.assertEqual(v1.z((140, 140)), 0)
        
        self.assertEqual(v1.influence((10, 10)), 0)
        self.assertEqual(v1.influence((50, 50)), 255)
        self.assertEqual(v1.influence((140, 140)), 0)
