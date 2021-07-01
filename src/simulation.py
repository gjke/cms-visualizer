from typing import Optional, List, Text
from dataclasses import dataclass


@dataclass
class TopographyObject:
    id: int
    x: int
    y: int


@dataclass
class RectangularTopographyObject(TopographyObject):
    width: int
    height: int


Source = TopographyObject
RectangularSource = RectangularTopographyObject

Target = TopographyObject
RectangularTarget = RectangularTopographyObject

Obstacle = TopographyObject
RectangularObstacle = RectangularTopographyObject


@dataclass
class Pedestrian:
    id: int
    label: Optional[Text]


@dataclass
class Topography:
    width: int
    height: int
    sources: List[Source]
    targets: List[Target]
    obstacles: List[Obstacle]


@dataclass
class SimulationStep:
    step: int


class Simulation:
    def __init__(self, topography: Topography, pedestrians: List[Pedestrian], n_steps: int, simulation_steps: List[SimulationStep]):
        self.topography = topography
        self.pedestrians = pedestrians
        self.n_steps = n_steps
        self.simulation_steps = simulation_steps
