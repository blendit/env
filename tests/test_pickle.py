import pickle
import unittest
from src.feature import Feature
from src.height_map import HeightMap
from src.environment import Environment


class TestPickle(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPickle, self).__init__(*args, **kwargs)

    def test_pickle(self):
        a = Environment([Feature()])
        # moche mais en attendant que ça marche...
        a.init_heightmap(10, 10)
        b = HeightMap(10, 10, z_func=lambda z: 100 * z[0] + z[1])
        a.heightmap = b

        f = open('/tmp/bli', 'wb')
        pickle.dump(a, f)
        f.close()

        g = open('/tmp/bli', 'rb')
        b = pickle.load(g)
        g.close()

        self.assertEqual(a.heightmap, b.heightmap)
