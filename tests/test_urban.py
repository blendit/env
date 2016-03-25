import unittest

import numpy as np
import shapely.geometry as geom

from src.urban import *


class TestTensorFields(unittest.TestCase):
    def assertMajorEigen(self, matrix, vector):
        _, (minor, major) = np.linalg.eigh(matrix)
        self.assertAlmostEqual(np.linalg.det((major, vector)), 0)
        self.assertAlmostEqual(np.dot(minor, vector), 0)

    def assertMinorEigen(self, matrix, vector):
        _, (minor, major) = np.linalg.eigh(matrix)
        self.assertAlmostEqual(np.dot(major, vector), 0)
        self.assertAlmostEqual(np.linalg.det((minor, vector)), 0)

    def test_tensor_from_vector(self):
        vecs = np.array([
            (0, 1),
            (- 1 / np.sqrt(2), 1 / np.sqrt(2)),
            (np.sqrt(3) / 2, - 0.5),
            (42, 24),
            (np.exp(-7), np.exp(7)),
        ])
        for vec in vecs:
            with self.subTest(vec=vec):
                self.assertMajorEigen(tensor_from_vector(vec), vec)

    def test_grid_field(self):
        vec = np.array((3, 4))
        center = geom.Point(0, 0)
        field = GridField(vec, center, 1)
        mat0 = field.tensor(center)
        for dist in range(5):
            with self.subTest(distance=dist):
                mat = field.tensor(geom.Point(0, dist))
                self.assertAlmostEqual(np.linalg.norm(mat - mat0 * np.exp(dist * dist)), 0)
                self.assertMajorEigen(mat, vec)

    def test_radial_field(self):
        center = geom.Point(0, 0)
        field = RadialField(center, 1)
        points = np.array([(0, 1), (-1, -1), (-2, 1), (4, -3)])
        for point in points:
            with self.subTest(point=point):
                mat = field.tensor(point)
                self.assertMinorEigen(mat, point)

    def test_boundary_field(self):
        line = np.array([(1, 0), (0, 0), (0, 1)])
        field = BoundaryField(line, 1)
        for dist in range(5):
            point = np.array((dist, dist))
            with self.subTest(point=point):
                mat = field.tensor(geom.Point(point))
                self.assertMinorEigen(mat, point)

    def test_height_field(self):
        def gradient(pos):
            x, y = pos
            return x, y * y
        field = HeightField(gradient)
        points = np.array([(0, 1), (1, np.sqrt(2)), (2, 1)])
        for point in points:
            with self.subTest(point=point):
                mat = field.tensor(point)
                self.assertMinorEigen(mat, gradient(point))
