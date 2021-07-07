import unittest
from src.topography import (
    Topography, RectangularSource, RectangularTarget, RectangularObstacle)
from src.simulation import (Simulation, Pedestrian, Position, InvalidSimulationStepException,
                            CannotAddSimulationStepException, SimulationReconstructionException)


class SimulationTest(unittest.TestCase):
    # topography: Topography

    def setUp(self):
        self.topography = (
            Topography(width=100, height=100)
            .with_sources([RectangularSource(1, 5, 5, 1, 1)])
            .with_targets([RectangularTarget(2, 95, 95, 1, 1)])
            .with_obstacles([RectangularObstacle(3, 50, 50, 1, 1)])
        )
        self.pedestrians = [
            Pedestrian(11, None),
            Pedestrian(12, None)
        ]
        self.simulation = Simulation(self.topography, self.pedestrians, 3, [])

    def test_simulation_creation(self):
        self.assertIsInstance(self.simulation, Simulation)
        self.assertEqual(len(self.simulation.pedestrians), 2)
        self.assertEqual(self.simulation.n_steps, 3)

    def test_adding_simulation_step(self):
        self.simulation.add_simulation_step(
            {11: Position(3, 3), 12: Position(5, 5)}
        )
        self.assertEqual(len(self.simulation.simulation_steps), 1)
        self.assertFalse(self.simulation.is_simulation_complete())

    def test_invalid_simulation_step(self):
        with self.assertRaises(InvalidSimulationStepException):
            self.simulation.add_simulation_step(
                {11: Position(-1, 0), 12: Position(0, 101)}
            )

        with self.assertRaises(InvalidSimulationStepException):
            self.simulation.add_simulation_step(
                {12: Position(0, 81)}
            )

    def test_complete_simulation(self):
        self.simulation.add_simulation_step(
            {11: Position(4, 3), 12: Position(6, 5)}
        )
        self.simulation.add_simulation_step(
            {11: Position(4, 4), 12: Position(6, 6)}
        )
        self.simulation.add_simulation_step(
            {11: Position(5, 4), 12: Position(7, 6)}
        )

        self.assertTrue(self.simulation.is_simulation_complete())

        with self.assertRaises(CannotAddSimulationStepException):
            self.simulation.add_simulation_step(
                {11: Position(4, 3), 12: Position(6, 5)}
            )


class SimulationJsonTest(unittest.TestCase):
    def test_create_simulation_from_json(self):
        simulation = Simulation.from_json('tests/valid_simulation.json')
        self.assertIsInstance(simulation, Simulation)
        self.assertEqual(len(simulation.pedestrians), 2)
        self.assertEqual(simulation.n_steps, 3)

    def test_create_simulation_from_json_invalid(self):
        with self.assertRaises(SimulationReconstructionException):
            Simulation.from_json('tests/invalid_simulation.json')
