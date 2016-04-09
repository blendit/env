from src.feature_tree import FeatureTree
from src.height_map import HeightMap


class Environment:
    """Environment class"""

    def __init__(self, features):
        self.res_x = 200
        self.res_y = 200
        
        self.tree = FeatureTree(features)
        self.models = self.tree.models

        # compute z coordinate
        for model in self.models:
            (x, y) = model.pos
            z = self.tree.z(model.pos)
            model.pos3D = (x, y, z)
        
        self.heightmap_init = False

    def init_heightmap(self, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y
        self.heightmap = HeightMap(res_x, res_y, self.tree.z)
        self.heightmap_init = True

    def export_heightmap(self, filename, res_x=None, res_y=None):
        if res_x is None:
            res_x = self.res_x
        if res_y is None:
            res_y = self.res_y
        
        if not self.heightmap_init:
            self.init_heightmap(res_x, res_y)
        
        self.heightmap.export(filename)
