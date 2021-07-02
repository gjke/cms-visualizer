import unittest
from src.topography import Topography, RectangularSource, RectangularTarget, RectangularObstacle, InvalidTopographyObjectException, DuplicateTopographyObjectIdException


class TopographyTest(unittest.TestCase):

    def test_topography_creation(self):
        topography = (
            Topography(width=200, height=200)
            .with_sources([RectangularSource(1, 5, 5, 1, 1)])
            .with_targets([RectangularTarget(2, 95, 95, 1, 1)])
            .with_obstacles([RectangularObstacle(3, 50, 50, 1, 1)])
        )
        self.assertIsInstance(topography, Topography)
        self.assertEqual(topography.width, 200)
        self.assertEqual(topography.height, 200)
        self.assertEqual(len(topography.sources), 1)
        self.assertEqual(len(topography.targets), 1)
        self.assertEqual(len(topography.obstacles), 1)

    def test_invalid_rect_source(self):
        with self.assertRaises(InvalidTopographyObjectException):
            Topography(width=100, height=100).with_sources(
                [RectangularSource(1, 105, 105, 1, 1)])

    def test_invalid_rect_target(self):
        with self.assertRaises(InvalidTopographyObjectException):
            Topography(width=100, height=100).with_targets(
                [RectangularTarget(1, -21, -21, 1, 1)])

    def test_invalid_rect_obstacle(self):
        with self.assertRaises(InvalidTopographyObjectException):
            Topography(width=100, height=100).with_obstacles(
                [RectangularObstacle(1, 5, 5, 0, 1)])

    def test_duplicate_id(self):
        with self.assertRaises(DuplicateTopographyObjectIdException):
            Topography(width=100, height=100).with_sources(
                [RectangularSource(1, 5, 5, 1, 1)]).with_targets(
                    [RectangularTarget(1, 25, 25, 1, 1)])

        with self.assertRaises(DuplicateTopographyObjectIdException):
            Topography(width=100, height=100).with_targets(
                [RectangularTarget(1, 5, 5, 1, 1)]).with_sources(
                    [RectangularSource(1, 25, 25, 1, 1)])

        with self.assertRaises(DuplicateTopographyObjectIdException):
            Topography(width=100, height=100).with_sources(
                [RectangularSource(1, 5, 5, 1, 1)]).with_obstacles(
                    [RectangularObstacle(1, 25, 25, 1, 1)])
