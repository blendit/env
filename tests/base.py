import shapely.geometry as geom
from src.feature_tree import BlendNode, ReplaceNode, AdditionNode, FeatureTree
from src.feature import Feature

from PIL import Image
import warnings


class FeatureTest(Feature):
    """A 1-1 square feature for tests."""
    def __init__(self, z_const=2, influence="all", val_influence=0.8):
        super().__init__()
        self.z_const = z_const
        self.shape = geom.box(0.0, 0.0, 1.0, 1.0)
        self.influ = influence
        self.val_influ = val_influence

    def z(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return self.z_const
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.influ == "all":
            return self.val_influ
        else:
            if self.shape.touches(coord) or self.shape.contains(coord):
                return self.val_influ
            else:
                return 0

                
class FeatureTestReplace(FeatureTest):
    """"The same 1-1 test square, but with replacing interaction."""
    def interaction(self):
        return "replace"


class FeatureTestAddition(FeatureTest):
    """"The same 1-1 test square, but with additive interaction."""
    def interaction(self):
        return "addition"


def compare_imgs(i1, i2, test_case):
    """Compare two images saved on the disk.
    * *i1*, *i2* are the paths of the two images.
    * *test_case* is a unittest.TestCase object, where the comparison have to be done."""
    # Ignore non-closed files
    warnings.simplefilter("ignore", ResourceWarning)
    
    original = Image.open(i1)
    gen = Image.open(i2)
    test_case.assertEqual(original, gen)
