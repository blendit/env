import numpy
import unittest
from src.height_map import HeightMap
import shapely.geometry as geom
from PIL import Image

from tests.test_feature_tree import FeatureTest, FeatureTestReplace, FeatureTestAddition
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

        original1 = Image.open("tests/img/m1.png")
        original2 = Image.open("tests/img/m2.png")
        gen1 = Image.open("m1.png")
        gen2 = Image.open("m2.png")
        
        self.assertEqual(original1, gen1)
        self.assertEqual(original2, gen2)


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

        # Loads image and compare it to the data stored
        original = Image.open("tests/img/mtree.png")
        gen = Image.open("mtree.png")
        self.assertEqual(original, gen)
