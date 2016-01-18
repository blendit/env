import unittest
from feature import Feature
import shapely.geometry as geom
from feature_tree import BlendNode, ReplaceNode, AdditionNode, FeatureTree


class FeatureTest(Feature):
    """A 1-1 square feature for tests."""
    def __init__(self, z_const=2, influence="all"):
        self.z_const = z_const
        self.shape = geom.box(0.0, 0.0, 1.0, 1.0)
        self.influ = influence

    def z(self, coord):
        coord = geom.Point(coord)
        if self.shape.touches(coord) or self.shape.contains(coord):
            return self.z_const
        else:
            return 0

    def influence(self, coord):
        coord = geom.Point(coord)
        if self.influ == "all":
            return 0.8
        else:
            if self.shape.touches(coord) or self.shape.contains(coord):
                return 0.8
            else:
                return 0


class FeatureTestReplace(FeatureTest):
    """"The same 1-1 test square, but with replacing interaction."""
    def interaction(self):
        return "replace"

        
class TestClassesNodes(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClassesNodes, self).__init__(*args, **kwargs)
        self.f1 = FeatureTest(1)
        self.f2 = FeatureTest(10)
        self.f2.shape = geom.box(1.0, 0.0, 2.0, 1.0)
        self.f3 = FeatureTest(100)
        self.f3.shape = geom.box(1.0, 0.0, 3.0, 1.0)

        self.n1 = BlendNode([self.f1])
        self.n2 = BlendNode([self.f2])
        self.n3 = BlendNode([self.f3])
        
    def test_blend_node(self):
        node1 = BlendNode([self.f1, self.f2])
        self.assertEqual(node1.z((1, 1)), (1 + 10) / 2)
        self.assertEqual(node1.influence((1, 1)), 2 * 0.8)
        self.assertEqual(node1.shape.area, 2.0)

        node2 = BlendNode([self.f1, self.f2, self.f3])
        self.assertAlmostEqual(node2.z((1, 1)), (1 + 10 + 100) / 3)
        self.assertEqual(node2.influence((1, 1)), 3 * 0.8)
        self.assertEqual(node2.shape.area, 3.0)

        node3 = BlendNode([self.n1, self.n2, self.n3])
        self.assertAlmostEqual(node3.z((1, 1)), (1 + 10 + 100) / 3)
        self.assertEqual(node3.influence((1, 1)), 3 * 0.8)
        self.assertEqual(node3.shape.area, 3.0)
        
    def test_replace_node(self):
        node1 = ReplaceNode(self.n1, self.n2)
        self.assertEqual(node1.z((1, 1)), 10 * 0.8 + 1 * 0.2)
        self.assertEqual(node1.influence((1, 1)), 0.8)
        self.assertEqual(node1.shape.area, 2.0)

        node1.add_child(self.n3)
        self.assertEqual(self.n3.z((1, 1)), 100)
        self.assertAlmostEqual(node1.z((1, 1)), 10 * 0.8 + (1 + 100) / 2 * 0.2)
        self.assertEqual(node1.influence((1, 1)), 0.8 * 2)
        self.assertEqual(node1.shape.area, 3.0)

    def test_addition_node(self):
        node1 = AdditionNode(self.n1, self.n2)
        self.assertEqual(node1.z((1, 1)), 1 + 10 * 0.8)
        self.assertEqual(node1.influence((1, 1)), 0.8)
        self.assertEqual(node1.shape.area, 2.0)


class TestClasseFeatureTree(unittest.TestCase):
    def test_tree(self):
        f1 = FeatureTest(1)
        f2 = FeatureTest(10)
        f3 = FeatureTestReplace(100)
        
        f1.shape = geom.box(0.0, 0.0, 1.0, 1.0)
        f2.shape = geom.box(0.5, 0.5, 1.5, 1.5)
        f3.shape = geom.box(0.75, 0, 0.8, 2)
        
        tree = FeatureTree([f1, f2])
        
        self.assertEqual(tree.z((0, 0)), 1 / 2)
        self.assertEqual(tree.z((0.75, 0.75)), (1 + 10) / 2)
        self.assertEqual(tree.z((1.2, 1.2)), 10 / 2)

        f1.influ = "notall"
        f2.influ = "notall"
        f3.influ = "notall"
        tree2 = FeatureTree([f1, f2, f3])
        
        self.assertEqual(tree2.z((0, 0)), 1)
        self.assertEqual(tree2.z((0.5, 0.5)), (1 + 10) / 2)
        self.assertEqual(tree2.z((1.2, 1.2)), 10)
        self.assertEqual(tree2.z((0.78, 0.75)), 0.8 * 100 + 0.2 * ((1 + 10) / 2))


if __name__ == '__main__':
    unittest.main()
