import numpy
from numpy import random
import shapely.geometry as geom
from random import randrange

from src.feature import Feature, FeatureLine
from src.model import Model, AbstractModel


class Landscape(Feature):
    """Landscape class"""

    def __init__(self):
        super(Landscape, self).__init__()


class Mountain(Landscape):
    """A mountain"""

    def __init__(self, radius, center_z, center_pos=(0, 0), freqs=[random.random() for x in range(10)], amplis=[random.exponential(10) for x in range(10)], noise=None):
        """NB: len(freqs) should equal len(amplis)"""
        super(Mountain, self).__init__()
        self.radius = int(numpy.sqrt(radius))**2  # rescaling
        if(noise is None):
            self.default_noise_grid = random.normal(0, 1, self.radius**2).reshape(self.radius, self.radius)
            self.noise = self.default_noise
        else:
            self.noise = noise
        center = geom.Point(*center_pos)
        self.center_pos = numpy.array(center)
        self.center_z = center_z
        # By default, buffer approximates the circle with a regular 16-gon
        self.shape = center.buffer(radius)
        self.freqs = freqs
        self.amplis = amplis
        print("A Mountain, of parameters %d and %d, %d" % (radius, center_pos[0], center_pos[1]))
        
    def default_noise(self, coord):
        try:
            return self.default_noise_grid[int(coord[0]), int(coord[1])]
        except IndexError:
            print("\tABADABOUUUUUUUm\t" + str(coord))
            raise IndexError

    def z(self, coord):
        """Generation of a height given a plane coordinate. Formula from [GGP+15], subsection 4.1"""
        x = coord[0] - self.center_pos[0]
        y = coord[1] - self.center_pos[1]
        if(x**2 + y**2 <= self.radius**2):
            return self.center_z + sum(a_i * self.noise((x * s_i, y * s_i))**3 for (a_i, s_i) in zip(self.amplis, self.freqs))
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0

from PIL import Image
import os
from random import choice


class MountainImg(Landscape):
    """A mountain extracted from heightmaps"""

    def __init__(self, shape, center=(0,0)):
        """NB: len(freqs) should equal len(amplis)"""
        super(MountainImg, self).__init__()
        center_ = geom.Point(*center)
        self.center_pos = numpy.array(center_)
        self.center_z = 0
        self.shape = shape
        # By default, buffer approximates the circle with a regular 16-gon
        self.bb = self.shape.bounds
        self.img = Image.open("../../models/mountains/" + random.choice(os.listdir("../../models/mountains/")))
        while(self.img.size[0] < self.bb[2] and self.img.size[1] < self.bb[3]):
            print("(MountainImg) Image to small, (want %d x %d) trying something else" % (self.bb[2], self.bb[3]))
            self.img = Image.open("../../models/mountains/" + choice(os.listdir("../../models/mountains/")))
        self.img_center_x = random.randint(0, self.img.size[0] - (self.bb[2] - self.bb[0]))
        self.img_center_y = random.randint(0, self.img.size[1] - (self.bb[3] - self.bb[1]))
        if(self.img.mode == 'I'):
            self.div = 255
        else:
            self.div = 1
        mini = self.img.getpixel((self.img_center_x + (self.bb[2] - self.bb[0]) // 2, self.img_center_y + (self.bb[3] - self.bb[1]) // 2))
        maxi = mini
        print(mini, maxi)
        print("Center at : " + str(self.center_pos))
        for x in range(int(self.bb[2] - self.bb[0])):
            for y in range(int(self.bb[3] - self.bb[1])):
                c = geom.Point((x, y))
                if(c.within(self.shape)):
                    val = self.img.getpixel((x + self.img_center_x, y + self.img_center_y))
                    mini = min(mini, val)
                    maxi = max(maxi, val)
        self.coeff = 255 / (maxi - mini)
        self.mini = mini
        print("x, y : %d %d" % (x, y))
        print("A MountainImg, of parameters %d, %d, mode %s, div %s" % (self.center_pos[0], self.center_pos[1], self.img.mode, self.div))

    def z(self, coord):
        """Generation of a height given a plane coordinate. Formula from [GGP+15], subsection 4.1"""
        x = coord[0] - self.center_pos[0]
        y = coord[1] - self.center_pos[1]
        c = geom.Point((x, y))
        if(self.shape.touches(c) or self.shape.contains(c)):
            return int((self.img.getpixel((self.img_center_x + x, self.img_center_y + y)) - self.mini) * self.coeff)
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0


class Road(FeatureLine):
    """A single road"""

    def __init__(self, points, thickness, height=0):
        """- *points* is the set of oints of the road
        - *thickness* is the width of the road
        - *height* (default **0**) is the constant height of the road"""
        super(Road, self).__init__(points, thickness)
        
        self.height = height

    def z(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return self.height
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0


class RoadNetwork(Feature):
    """A network of roads"""

    def __init__(self):
        super(RoadNetwork, self).__init__()
        

class Vegetation(Feature):
    """Vegetation class.
    
    Attributes:
    * pos: top-left origin of the region of the vegetation
    * influence_map
    * models
    * base_model: abstract model used for the vegetation """

    def __init__(self, shape, model=AbstractModel(), tree_number=100):
        super().__init__()
        self.base_model = model
        self.shape = shape
        
        self.generate_models(tree_number)

    def generate_models(self, number):
        self.model = []
        (minx, miny, maxx, maxy) = self.shape.bounds

        i = 0
        while i < number:
            x = randrange(int(minx), int(maxx))
            y = randrange(int(miny), int(maxy))

            coord = geom.Point((x, y))
            if self.shape.touches(coord) or self.shape.contains(coord):
                self.models.append(Model((x, y), self.base_model))
                i += 1
            
    def z(self, pos):
        return 0
        
    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0

    def interaction(self):
        return "addition"
