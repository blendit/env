import pickle
import unittest
from src.height_map import HeightMap


class TestPickle(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPickle, self).__init__(*args, **kwargs)

    def test_pickle(self):
        a = HeightMap(10, 10, z_func=lambda z: 10*z[0]+z[1])

        f = open('/tmp/bli', 'wb')
        pickle.dump(a, f)
        f.close()

        g = open('/tmp/bli', 'rb')
        b = pickle.load(g)
        g.close()

        self.assertEqual(a.hmap, b.hmap)
        self.assertEqual(a.size_x, b.size_x)
        self.assertEqual(a.size_y, b.size_y)
        


