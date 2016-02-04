import numpy
import unittest
from src.height_map import HeightMap
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
