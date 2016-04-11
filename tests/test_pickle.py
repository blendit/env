import pickle
import unittest
import shapely.geometry as geom

from src.feature import Feature, ImageFeature
from src.height_map import HeightMap
from src.environment import Environment
from src.landscape import Vegetation
from src.model import Model, AbstractModel

import os
import sys


class TestPickle(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPickle, self).__init__(*args, **kwargs)

    def test_pickle(self):
        a = Environment([Feature()])
        # moche mais en attendant que ça marche...
        a.init_heightmap(10, 10)
        b = HeightMap(10, 10, z_func=lambda z: 100 * z[0] + z[1])
        a.heightmap = b

        f = open('/tmp/waves.p', 'wb')
        pickle.dump(a, f)
        f.close()

        g = open('/tmp/waves.p', 'rb')
        b = pickle.load(g)
        g.close()

        self.assertEqual(a.heightmap, b.heightmap)

    def test_mountains(self):
        mount = ImageFeature("tests/img/mount_200.png")
        
        gen_model = AbstractModel(os.path.abspath(os.path.dirname(sys.argv[0])) + "/tests/models/pine_tree/Pine_4m.obj", 0.01, (0, 0))
        v1 = Vegetation(geom.box(20, 20, 180, 180), gen_model, 10)
        v1.models.append(Model((5, 5), gen_model))
        v1.models.append(Model((195, 195), gen_model))

        env = Environment([mount, v1])
        env.init_heightmap(200, 200)
        
        f = open('mountains.pickle', 'wb')
        pickle.dump(env, f)
        f.close()

        env.export_heightmap("bla.png", 200, 200)
