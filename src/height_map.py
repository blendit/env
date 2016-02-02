from PIL import Image
import numpy

class HeightMap:
    """Height map structure. This is just a 2D array containing z-values"""

    def default_z(pos):
        """Default initialization of the map: every point at z = 0"""
        return 0
    
    def __init__(self, sx, sy, z_func=default_z):
        """We can pass another function to z_func to initialize directly to z_func((x,y))"""
        self.size_x = sx
        self.size_y = sy
        self.hmap = [[z_func((x, y)) for x in range(sx)] for y in range(sy)]

    def __getitem__(self, index):
        return self.hmap[index]

    def export(self, path):
        im = Image.fromarray(numpy.uint8(self.hmap), "L") # "L" specifies 8-bit grayscale integer
        im.save(path)
