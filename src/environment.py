from src.feature_tree import FeatureTree
from src.height_map import HeightMap


class Environment:
    """Environment class"""

    def __init__(self, features, x=200, y=200):
        self.res_x = x
        self.res_y = y
        
        self.tree = FeatureTree(features)
        self.models = self.tree.models

        # compute z coordinate and gather abstract models
        self.abstract_models = set()
        
        for model in self.models:
            (x, y) = model.pos
            z = self.tree.z(model.pos)
            model.pos3D = (x, y, z)

            self.abstract_models.add(model.model)
        
        self.heightmap_init = False

    # def translate_hm(self, coords):
    #     return self.tree.z((coords[0] + self.res_x // 2, coords[1] + self.res_y // 2))
        
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
