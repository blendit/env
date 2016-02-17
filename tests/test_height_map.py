import numpy
import unittest
from src.height_map import HeightMap
import shapely.geometry as geom

from tests.test_feature_tree import FeatureTest, FeatureTestReplace
from src.feature_tree import *

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

class TestHeightMapTree(unittest.TestCase):
    def test_tree_hmap(self):
        f1 = FeatureTest(10, influence="notall")
        f2 = FeatureTest(100, influence="notall")

        f1.shape = geom.box(0, 0, 20, 20)
        f2.shape = geom.box(50, 50, 60, 60)

        tree = FeatureTree([f1, f2])
        
        heightmap = HeightMap(100, 100, tree.z)

        self.assertRaises(None, heightmap.export("mtree.png"))
        
