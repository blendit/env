import unittest
from feature import Feature, FeatureLine
import shapely.geometry as geom

class FeatureTest(Feature):
    def __init__(self, x1, y1, x2, y2):
        self.shape = geom.box(x1, y1, x2, y2)


class TestFeature(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFeature, self).__init__(*args, **kwargs)
        self.f1 = FeatureTest(0, 0, 1, 1)
        self.f2 = FeatureTest(1, 1, 2, 2)
        self.f3 = FeatureTest(0, 0, 2, 2)

        self.l1 = FeatureLine([(0, 0), (2, 2)], 1)
        self.l2 = FeatureLine([(0, 0), (-1, -1)], 1)
        
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


if __name__ == '__main__':
    unittest.main()
