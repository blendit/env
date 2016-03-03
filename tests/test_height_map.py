import numpy
import unittest
from tests.base import FeatureTest, FeatureTestReplace, FeatureTestAddition, compare_imgs

from src.height_map import HeightMap
from src.feature_tree import *

import shapely.geometry as geom


class TestHeightMap(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHeightMap, self).__init__(*args, **kwargs)
        self.m1 = HeightMap(100, 100)
        self.m2 = HeightMap(100, 100, lambda z: z[0] + 1 + z[1])

    def test_hmap(self):
        self.assertEqual(self.m1.hmap[0][0], 0)
        self.assertEqual(self.m2.hmap[0][0], 1)
        self.assertEqual(self.m2.hmap[1][2], 4)

    def test_export(self):
        self.assertRaises(None, self.m1.export("m1.png"))
        self.assertRaises(None, self.m2.export("m2.png"))
        self.assertRaises(None, self.m2.export("m3.png", 2))

        compare_imgs("tests/img/m1.png", "m1.png", self)
        compare_imgs("tests/img/m2.png", "m2.png", self)
        compare_imgs("tests/img/m3.png", "m3.png", self)

    def test_change_res(self):
        res = 2
        self.m = HeightMap(10, 10, lambda z: z[0]+10*z[1])
        self.assertEqual(self.m.hmap[9][9], 99)
        self.m.change_res(2)
        self.assertEqual(self.m.hmap[19][19], 99)
        self.assertEqual(self.m.hmap[19][18], 99)
        self.assertEqual(self.m.hmap[18][19], 99)
        self.assertEqual(self.m.hmap[18][18], 99)


class TestHeightMapTree(unittest.TestCase):
    def test_tree_hmap(self):
        f1 = FeatureTest(100, influence="notall")
        f2 = FeatureTest(200, influence="notall")
        f3 = FeatureTestReplace(100, influence="notall", val_influence=1)
        f4 = FeatureTestAddition(100, influence="notall")

        f1.shape = geom.box(0, 0, 50, 50)
        f2.shape = geom.box(30, 30, 80, 80)
        f3.shape = geom.box(0, 60, 50, 100)
        f4.shape = geom.box(60, 60, 100, 100)

        tree = FeatureTree([f1, f2, f3, f4])
        
        heightmap = HeightMap(100, 100, tree.z)

        self.assertRaises(None, heightmap.export("mtree.png"))
        compare_imgs("tests/img/mtree.png", "mtree.png", self)
