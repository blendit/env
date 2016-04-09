from PIL import Image
import numpy


class HeightMap:
    """Height map structure. This is just a 2D array containing z-values"""

    def __default_z(pos):
        """Default initialization of the map: every point at z = 0"""
        return 0
    
    def __init__(self, sx, sy, z_func=__default_z, max_val=255):
        """We can pass another function to z_func to initialize directly to z_func((x,y))"""
        self.size_x = sx
        self.size_y = sy
        self.hmap = [[z_func((x, y)) for x in range(sx)] for y in range(sy)]

        # Resize too large points (threshold)
        for x in range(sx):
            for y in range(sy):
                if self.hmap[y][x] > max_val:
                    self.hmap[y][x] = max_val

    def __getitem__(self, index):
        return self.hmap[index]

    def __eq__(self, other):
        return (self.size_x == other.size_x) and (self.size_y == other.size_y) and (self.hmap == other.hmap)

    def change_res(self, res):
        new_h = [[self.hmap[y // res][x // res] for x in range(res * self.size_x)] for y in range(res * self.size_y)]
        self.size_x *= res
        self.size_y *= res
        self.hmap = new_h

    def export(self, path, res=1):
        if(res > 1):
            self.change_res(res)
        im = Image.fromarray(numpy.uint8(self.hmap), "L")
        # "L" specifies 8-bit grayscale integer
        im.save(path)
