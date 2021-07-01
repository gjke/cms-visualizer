import unittest
from src.simulation import Pedestrian, RectangularTopographyObject, Simulation, Topography


class SimulationTest(unittest.TestCase):

    def test_simulation_creation(self):
        topography = Topography(
            width=100, height=100,
            sources=[RectangularTopographyObject(1, 5, 5, 1, 1)],
            targets=[RectangularTopographyObject(2, 95, 95, 1, 1)],
            obstacles=[RectangularTopographyObject(3, 50, 50, 1, 1)]
        )
        pedestrians = [
            Pedestrian(4, "a"),
            Pedestrian(5, "b")
        ]
        simulation = Simulation(topography, pedestrians, 20, [])
        self.assertIsInstance(simulation, Simulation)
