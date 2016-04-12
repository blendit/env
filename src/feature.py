import shapely.geometry as geom
from PIL import Image
import warnings


class Feature():
    """The Feature class.
    Things like landscapes, water, ... will inherit from this call"""

    def __init__(self):
        """coord_x, coord_y is the "middle-point" ?
        Shape is the 2D-shape (x & y axis) of our feature"""
        self.pos = (0, 0)

        self.shape = geom.Polygon()

        self.models = []

    def intersect(self, feature2):
        """Returns *true* if the feature intersects *feature2*.
        NB: this should be symmetric."""
        return self.shape.intersects(feature2.shape)

    def z(self, coord):
        """Export the heightmap given a feature and a plane coordinate"""
        return 0

    def influence(self, coord):
        """Export influence heightmap"""
        return 0

    def interaction(self):
        """Give the interaction type of the feature with other features.
        Can be:
        * "blend" (default): the mean with the other features
        * "replace": one feature erase one other (**only two features**)
        * "addition": add one feature over another (**only two features**)."""
        return "blend"


class FeatureLine(Feature):
    """Feature corresponding to a linear zone: new functions to manipulate the curve of the feature."""

    def __init__(self, points, thickness):
        """Creates a line following the given points with a certain thickness."""
        self.line = geom.LineString(points)
        self.thickness = thickness
        self._update_shape()

        self.models = []

    def _update_shape(self):
        """Updates the shape to match the current path and thickness."""
        self.shape = self.line.buffer(self.thickness, cap_style=geom.CAP_STYLE.flat, join_style=geom.JOIN_STYLE.round)

    def interaction(self):
        """Give the interaction type of the feature with other features.
        Can be:
        * "blend": the mean with the other features
        * "replace" (default for FeatureLine): one feature erase one other (**only two features**)
        * "addition": add one feature over another (**only two features**)."""
        return "replace"


class ImageFeature(Feature):
    """A basic feature whose z is simply an image"""
    def __init__(self, image_path):
        super().__init__()

        # Ignore PIL warnings
        warnings.simplefilter("ignore", ResourceWarning)

        im = Image.open(image_path).convert('L')
        pixels = list(im.getdata())
        width, height = im.size
        self.pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

        self.shape = geom.box(0, 0, width, height)
        self.x = width
        self.y = height

    def z(self, coord):
        (x, y) = coord
        coord = geom.Point(coord)

        if x >= self.x or y >= self.y:
            return 0
        elif self.shape.touches(coord) or self.shape.contains(coord):
            return self.pixels[int(y)][int(x)]
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return 1
        else:
            return 0
