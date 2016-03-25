from src.feature_tree import FeatureTree
from src.height_map import HeightMap


class Environment:
    """Environment class"""

    def __init__(self, features):
        self.tree = FeatureTree(features)
        self.models = self.tree.models
        
        self.heightmap_init = False

    def init_heightmap(self, res_x, res_y):
        self.heightmap = HeightMap(res_x, res_y, self.tree.z)
        self.heightmap_init = True

    def export_heightmap(filename, res_x=500, res_y=500):
        if not self.heightmap_init:
            self.init_heightmap(res_x, res_y)
        
        self.heightmap.export(filename)
