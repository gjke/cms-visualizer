from __future__ import annotations
from typing import Optional, List, Text, Dict
from dataclasses import dataclass
from .topography import Topography


@dataclass
class Pedestrian:
    id: int
    label: Optional[Text]


@dataclass
class Position:
    x: int
    y: int


SimulationStep = Dict[int, Position]


class Simulation:
    def __init__(self, topography: Topography, pedestrians: List[Pedestrian], n_steps: int, simulation_steps: List[SimulationStep]) -> None:
        self.topography = topography
        self.pedestrians = pedestrians
        self.n_steps = n_steps
        self.simulation_steps = simulation_steps

    def _is_valid_simulation_step(self, simulation_step: SimulationStep) -> bool:
        '''
        A simulation step is valid if there are coordinates for every defined pedestrian
        and the coordinates lie within the defined topography
        '''
        return (
            all([pedestrian.id in simulation_step for pedestrian in self.pedestrians]) and
            all([self._is_valid_position(simulation_step[pedestrian.id])
                for pedestrian in self.pedestrians])
        )

    def _is_valid_position(self, position: Position):
        return 0 <= position.x < self.topography.width and 0 <= position.y < self.topography.height

    def is_simulation_complete(self):
        return len(self.simulation_steps) == self.n_steps

    def add_simulation_step(self, simulation_step: SimulationStep):
        if self.is_simulation_complete():
            raise CannotAddSimulationStepException(simulation_step)
        if not self._is_valid_simulation_step(simulation_step):
            raise InvalidSimulationStepException(simulation_step)

        self.simulation_steps.append(simulation_step)


class InvalidSimulationStepException(Exception):
    def __init__(self, simulation_step: SimulationStep):
        super().__init__("{} is invalid for this Topography.".format(str(simulation_step)))


class CannotAddSimulationStepException(Exception):
    def __init__(self, simulation_step: SimulationStep):
        super().__init__("Simulation is full. Cannot add {}.".format(str(simulation_step)))
