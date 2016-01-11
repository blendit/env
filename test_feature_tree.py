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
        return 0.8

        
class TestClassesNodes(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClassesNodes, self).__init__(*args, **kwargs)
        self.f1 = FeatureTest(1)
        self.f2 = FeatureTest(10)
        self.f2.shape = geom.box(1.0, 0.0, 2.0, 1.0)
        self.f3 = FeatureTest(100)
        self.f3.shape = geom.box(2.0, 0.0, 3.0, 1.0)

        self.n1 = BlendNode([self.f1])
        self.n2 = BlendNode([self.f2])
        self.n3 = BlendNode([self.f3])
        
    def test_blend_node(self):
        node1 = BlendNode([self.f1, self.f2])
        self.assertEqual(node1.z((1, 1)), (1 + 10) / 2)
        self.assertEqual(node1.influence((1, 1)), 2*0.8)
        self.assertEqual(node1.shape.area, 2.0)

        node2 = BlendNode([self.f1, self.f2, self.f3])
        self.assertAlmostEqual(node2.z((1, 1)), (1 + 10 + 100) / 3)
        self.assertEqual(node2.influence((1, 1)), 3*0.8)
        self.assertEqual(node2.shape.area, 3.0)

        node3 = BlendNode([self.n1, self.n2, self.n3])
        self.assertAlmostEqual(node3.z((1, 1)), (1 + 10 + 100) / 3)
        self.assertEqual(node3.influence((1, 1)), 3*0.8)
        self.assertEqual(node3.shape.area, 3.0)
        
    def test_replace_node(self):
        node1 = ReplaceNode(self.n1, self.n2)
        self.assertEqual(node1.z((1, 1)), 10*0.8 + 1*0.2)
        self.assertEqual(node1.influence((1, 1)), 0.8)
        self.assertEqual(node1.shape.area, 2.0)

        node1.add_child(self.n3)
        self.assertEqual(self.n3.z((1,1)), 100)
        self.assertAlmostEqual(node1.z((1, 1)), 10*0.8 + (1+100)/2*0.2)
        self.assertEqual(node1.influence((1, 1)), 0.8*2)
        self.assertEqual(node1.shape.area, 3.0)


if __name__ == '__main__':
    unittest.main()
