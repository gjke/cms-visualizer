from __future__ import annotations
import json
from typing import Optional, List, Text, Dict
from dataclasses import dataclass
from .topography import Topography


@dataclass
class Pedestrian:
    id: int
    radius: int
    label: Optional[Text]


@dataclass
class Position:
    x: int
    y: int


SimulationStep = Dict[int, Position]


class Simulation:
    def __init__(self, topography: Topography, pedestrians: List[Pedestrian], n_steps: int, simulation_steps: List[SimulationStep]) -> None:
        """Crowd simulation with topography and simulation steps 

        Args:
            topography (Topography): Topography in which the simulation took place
            pedestrians (List[Pedestrian]): List of pedestrians participating in the simulation
            n_steps (int): Number of simulation steps
            simulation_steps (List[SimulationStep]): List of simulation steps
        """
        self.topography = topography
        self.pedestrians = pedestrians
        self.n_steps = n_steps
        self.simulation_steps = []
        for simulation_step in simulation_steps:
            self.add_simulation_step(simulation_step)

    def _is_valid_simulation_step(self, simulation_step: SimulationStep) -> bool:
        """A simulation step is valid if there are positions for every defined pedestrian
        and these positions are valid

        Args:
            simulation_step (SimulationStep): Simulation step to check

        Returns:
            bool: True if the simulation step is valid
        """
        return (
            all([pedestrian.id in simulation_step for pedestrian in self.pedestrians]) and
            all([self._is_valid_position(simulation_step[pedestrian.id])
                for pedestrian in self.pedestrians])
        )

    def _is_valid_position(self, position: Position) -> bool:
        """A position is valid if it is inside the given topography

        Args:
            position (Position): Position to check

        Returns:
            [bool]: True if position is valid
        """
        return 0 <= position.x < self.topography.width and 0 <= position.y < self.topography.height

    def is_simulation_complete(self) -> bool:
        """ A simulation is complete if it has n_steps simulation steps

        Returns:
            [bool]: True if simulation is complete
        """
        return len(self.simulation_steps) == self.n_steps

    def add_simulation_step(self, simulation_step: SimulationStep) -> None:
        """Add a simulation step

        Args:
            simulation_step (SimulationStep): The simulation step to add

        Raises:
            CannotAddSimulationStepException: Raised if the simulation is already complete
            InvalidSimulationStepException: Raised if the simulation step is invalid
        """
        if self.is_simulation_complete():
            raise CannotAddSimulationStepException(simulation_step)
        if not self._is_valid_simulation_step(simulation_step):
            raise InvalidSimulationStepException(simulation_step)

        self.simulation_steps.append(simulation_step)

    @classmethod
    def from_json(cls, path: str) -> Simulation:
        """Instantiate a simulation from a JSON file

        Args:
            path (str): Path to the JSON file

        Raises:
            SimulationReconstructionException: Raised if the simulation could not be reconstructed 

        Returns:
            Simulation: 
        """
        with open(path) as f:
            data = json.load(f)
        topography = Topography.from_dict(data['topography'])

        if 'pedestrians' not in data:
            raise SimulationReconstructionException(
                "Object must include 'pedestrians'")
        pedestrians = [Pedestrian(o["id"], o.get("label", None))
                       for o in data['pedestrians']]
        if 'n_steps' not in data:
            raise SimulationReconstructionException(
                "Object must include 'n_steps'")
        if 'simulation_steps' not in data:
            raise SimulationReconstructionException(
                "Object must include 'simulation_steps'")
        simulation_steps: List[SimulationStep] = []
        for step in data['simulation_steps']:
            simulation_steps.append({
                pp["id"]: Position(*pp["position"]) for pp in step["pedestrian_positions"]
            })
        return Simulation(topography, pedestrians, data['n_steps'], simulation_steps)

    def to_json(self, path: str) -> None:
        """Serialize the simulation to a JSON file

        Args:
            path (str): Path to the JSON file
        """
        d = {
            "topography": self.topography.to_dict(),
            "pedestrians": [vars(pedestrian) for pedestrian in self.pedestrians],
            "n_steps": self.n_steps,
            "simulation_steps": [
                {
                    "step": i,
                    "pedestrian_positions": [
                        {
                            "id": key,
                            "position": [simulation_step[key].x, simulation_step[key].y]
                        } for key in simulation_step.keys()
                    ]
                }
                for i, simulation_step in enumerate(self.simulation_steps)
            ]
        }
        with open(path, "w+") as f:
            json.dump(d, f, indent=4)


class InvalidSimulationStepException(Exception):
    def __init__(self, simulation_step: SimulationStep):
        super().__init__("{} is invalid for this Topography.".format(str(simulation_step)))


class CannotAddSimulationStepException(Exception):
    def __init__(self, simulation_step: SimulationStep):
        super().__init__("Simulation is full. Cannot add {}.".format(str(simulation_step)))


class SimulationReconstructionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
