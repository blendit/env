import unittest
from feature import Feature
import shapely.geometry as geom

class TestFeature(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFeature, self).__init__(*args, **kwargs)
        self.f1 = Feature()
        self.f1.shape = geom.box(0, 0, 1, 1)
        self.f2 = Feature()
        self.f2.shape = geom.box(1, 1, 2, 2)
        self.f3 = Feature()
        self.f3.shape = geom.box(0, 0, 2, 2)
        
    def test_intersect(self):
        self.assertFalse(self.f1.intersect(self.f2))
        self.assertFalse(self.f2.intersect(self.f1))
        self.assertTrue(self.f1.intersect(self.f3))
        self.assertTrue(self.f2.intersect(self.f3))
        self.assertTrue(self.f3.intersect(self.f2))
        self.assertTrue(self.f3.intersect(self.f1))


if __name__ == '__main__':
    unittest.main()
