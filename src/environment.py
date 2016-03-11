from feature_tree import FeatureTree
from height_map import HeightMap



class Environment:
    """Environment class"""

    def __init__(self, features):
        self.tree = FeatureTree(features)
        self.heightmap_init = False

    def init_heightmap(res_x, res_y):
        self.heightmap = HeightMap(res_x, res_y, self.tree)
        self.heightmap_init = True

    def export_heightmap(filename, res_x=500, res_t=500):
        if not self.heightmap_init:
            slelf.init_heightmap(res_x, res_y)
        
        self.heightmap.export(filename)
