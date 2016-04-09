import unittest
import shapely.geometry as geom
from src.landscape import Mountain, Road, RoadNetwork, Vegetation
from src.feature_tree import BlendNode, ReplaceNode, AdditionNode, FeatureTree
from src.height_map import HeightMap
from src.feature import Feature

from tests.base import FeatureTest, FeatureTestReplace, FeatureTestAddition, 


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

        node1.add_child(self.n3)
        self.assertEqual(self.n3.z((1, 1)), 100)
        self.assertAlmostEqual(node1.z((1, 1)), 10 * 0.8 + (1 + 100) / 2)
        self.assertEqual(node1.influence((1, 1)), 0.8 * 2)
        self.assertEqual(node1.shape.area, 3.0)


class TestClassFeatureTree(unittest.TestCase):
    def setUp(self):
        self.f1 = FeatureTest(1, influence="notall")
        self.f2 = FeatureTest(10, influence="notall")
        self.f3 = FeatureTestReplace(100, influence="notall")
        self.f4 = FeatureTestAddition(1000, influence="notall")

        self.f1.shape = geom.box(0.0, 0.0, 1.0, 1.0)
        self.f2.shape = geom.box(0.5, 0.5, 1.5, 1.5)
        self.f3.shape = geom.box(0.75, 0, 0.8, 2)
        self.f4.shape = geom.box(0.75, 0, 0.8, 2)

    def test_tree(self):
        self.f1.influ = "all"
        self.f2.influ = "all"
        tree = FeatureTree([self.f1, self.f2])

        self.assertEqual(tree.z((0, 0)), 1 / 2)
        self.assertEqual(tree.z((0.75, 0.75)), (1 + 10) / 2)
        self.assertEqual(tree.z((1.2, 1.2)), 10 / 2)

    def test_replace_tree(self):
        tree2 = FeatureTree([self.f1, self.f2, self.f3])

        self.assertEqual(tree2.z((0, 0)), 1)
        self.assertEqual(tree2.z((0.5, 0.5)), (1 + 10) / 2)
        self.assertEqual(tree2.z((1.2, 1.2)), 10)
        self.assertEqual(tree2.z((0.78, 0.75)), 0.8 * 100 + 0.2 * ((1 + 10) / 2))

    def test_addition_tree(self):
        tree3 = FeatureTree([self.f1, self.f2, self.f4])

        self.assertEqual(tree3.z((0, 0)), 1)
        self.assertEqual(tree3.z((0.5, 0.5)), (1 + 10) / 2)
        self.assertEqual(tree3.z((1.2, 1.2)), 10)
        self.assertAlmostEqual(tree3.z((0.78, 0.75)), 0.8 * 1000 + ((1 + 10) / 2))

    def test_mountain(self):
        m2 = Mountain(10**4, 0, (50, 50))
        t = FeatureTree([m2])
        u = HeightMap(100, 100, t.z)
        # u.export("mountain_as_ft.png")
