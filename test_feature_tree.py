import unittest
from feature import Feature
import shapely.geometry as geom
from feature_tree import BlendNode, ReplaceNode, AdditionNode


class FeatureTest(Feature):
    """A 1-1 square feature for tests."""
    def __init__(self, z_const=2):
        self.z_const = z_const
        self.shape = geom.box(0.0, 0.0, 1.0, 1.0)

    def z(self, coord):
        return self.z_const

    def influence(self, coord):
        return 1

        
class TestClassesNodes(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClassesNodes, self).__init__(*args, **kwargs)
        self.f1 = FeatureTest(1)
        self.f2 = FeatureTest(10)
        self.f3 = FeatureTest(100)
        
    def test_blend_node(self):
        node1 = BlendNode([self.f1, self.f2])
        self.assertEqual(node1.z((1, 1)), (1 + 10) / 2)
        self.assertEqual(node1.influence((1, 1)), 2)

        node2 = BlendNode([self.f1, self.f2, self.f3])
        self.assertEqual(node2.z((1, 1)), (1 + 10 + 100) / 3)
        self.assertEqual(node2.influence((1, 1)), 3)

if __name__ == '__main__':
    unittest.main()
