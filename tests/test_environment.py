import unittest
import shapely.geometry as geom

from tests.base import FeatureTest, FeatureTestReplace

from src.feature_tree import FeatureTree
from src.height_map import HeightMap
from src.landscape import Vegetation
from src.environment import Environment


class TestClassEnvironment(unittest.TestCase):
    def setUp(self):
        self.background = FeatureTest(100, influence="notall", val_influence=1)
        self.background.shape = geom.box(5, 5, 45, 45)
        
        self.up = FeatureTest(150, influence="notall", val_influence=1)
        self.up.shape = geom.box(10, 10, 30, 30)
        
        self.rep = FeatureTestReplace(0, influence="notall", val_influence=1)
        self.rep.shape = geom.box(10, 10, 20, 20)
        
        self.forest = Vegetation(pos=(5, 5), size=(40, 40), tree_number=50)

        self.env = Environment([self.rep, self.up, self.background, self.forest])
        
    def test_models(self):
        self.assertLess(len(self.env.models), 50)
        self.assertGreater(len(self.env.models), 35)

        self.env.export_heightmap("temp_env.png", 50, 50)

        
from tests.base import compare_imgs
from src.landscape import Mountain
        
class TestImageEnvironment(unittest.TestCase):
    def test_mountain(self):
        m2 = Mountain(10**3, 0, (50, 50))
        t = Environment([m2])
        t.export_heightmap("mountain_as_env.png", res_x=100, res_y=100)

