import unittest
from src.feature import Feature, FeatureLine, ImageFeature
import shapely.geometry as geom


class FeatureTest(Feature):
    def __init__(self, x1, y1, x2, y2):
        self.shape = geom.box(x1, y1, x2, y2)


class TestFeature(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFeature, self).__init__(*args, **kwargs)
        self.f1 = FeatureTest(0, 0, 0.9, 0.9)
        self.f2 = FeatureTest(1, 1, 2, 2)
        self.f3 = FeatureTest(0, 0, 2, 2)

        self.l1 = FeatureLine([(0, 0), (2, 2)], 1)
        self.l2 = FeatureLine([(-0.1, -0.1), (-1, -1)], 1)
        self.l3 = FeatureLine([(0, 0), (0, -1)], 1)

    def test_intersect_ff(self):
        """Intersection between two features"""
        self.assertFalse(self.f1.intersect(self.f2))
        self.assertFalse(self.f2.intersect(self.f1))

        self.assertTrue(self.f1.intersect(self.f3))
        self.assertTrue(self.f3.intersect(self.f1))

        self.assertTrue(self.f2.intersect(self.f3))
        self.assertTrue(self.f3.intersect(self.f2))

    def test_intersect_fl(self):
        """Intersection feature/featureline"""
        self.assertTrue(self.l1.intersect(self.f3))
        self.assertTrue(self.f3.intersect(self.l1))

        self.assertFalse(self.l2.intersect(self.f1))
        self.assertFalse(self.f1.intersect(self.l2))

    def test_intersect_ll(self):
        """Intersection featureline/featureline"""
        self.assertFalse(self.l1.intersect(self.l2))
        self.assertFalse(self.l2.intersect(self.l1))

        self.assertTrue(self.l1.intersect(self.l3))
        self.assertTrue(self.l3.intersect(self.l1))

    def test_z(self):
        self.f1.z((0, 0))

    def test_influence(self):
        self.f1.influence((0, 0))


from src.height_map import HeightMap
from tests.base import compare_imgs


class TestImageFeature(unittest.TestCase):
    def test_image_feature(self):
        feat = ImageFeature("tests/img/mtree.png")
        hm = HeightMap(100, 100, feat.z)
        hm.export("imagefeat.png")

        compare_imgs("tests/img/mtree.png", "imagefeat.png", self)
