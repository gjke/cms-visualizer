from __future__ import annotations
from typing import List, Tuple, Iterable, Set
from abc import ABC, abstractclassmethod
from dataclasses import dataclass


@dataclass
class TopographyObject(ABC):
    id: int
    x: int
    y: int

    @abstractclassmethod
    def get_min_coordinates(self) -> Tuple[int, int]:
        raise NotImplementedError(
            "TopographyObject must implment get_min_coordinates()")

    @abstractclassmethod
    def get_max_coordinates(self) -> Tuple[int, int]:
        raise NotImplementedError(
            "TopographyObject must implment get_max_coordinates()")


@dataclass
class RectangularTopographyObject(TopographyObject):
    width: int
    height: int

    def get_min_coordinates(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def get_max_coordinates(self) -> Tuple[int, int]:
        return (self.x + self.width, self.y + self.height)


Source = TopographyObject


class RectangularSource(RectangularTopographyObject):
    def __str__(self):
        return "RectangularSource(x={}, y={}, width={}, height={})".format(self.x, self.y, self.width, self.height)


Target = TopographyObject


class RectangularTarget(RectangularTopographyObject):
    def __str__(self):
        return "RectangularTarget(x={}, y={}, width={}, height={})".format(self.x, self.y, self.width, self.height)


Obstacle = TopographyObject


class RectangularObstacle(RectangularTopographyObject):
    def __str__(self):
        return "RectangularObstacle(x={}, y={}, width={}, height={})".format(self.x, self.y, self.width, self.height)


class Topography:
    sources: List[Source]
    targets: List[Target]
    obstacles: List[Obstacle]
    object_ids: Set[int]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.sources = []
        self.targets = []
        self.obstacles = []
        self.object_ids = set([])

    def _is_valid_topography_object(self, obj: TopographyObject) -> bool:
        min_x, min_y = obj.get_min_coordinates()
        max_x, max_y = obj.get_max_coordinates()

        return (
            0 <= min_x < self.width and
            0 <= min_y < self.height and
            0 <= max_x < self.width and
            0 <= max_y < self.height and
            max_x - min_x > 0 and
            max_y - min_y > 0
        )

    def with_sources(self, new_sources: Iterable[Source]) -> Topography:
        for source in new_sources:
            if not self._is_valid_topography_object(source):
                raise InvalidTopographyObjectException(source)
            if not source.id in self.object_ids:
                self.sources.append(source)
                self.object_ids.add(source.id)
            else:
                raise DuplicateTopographyObjectIdException(source.id)
        return self

    def with_targets(self, new_targets: Iterable[Target]) -> Topography:
        for target in new_targets:
            if not self._is_valid_topography_object(target):
                raise InvalidTopographyObjectException(target)
            if not target.id in self.object_ids:
                self.targets.append(target)
                self.object_ids.add(target.id)
            else:
                raise DuplicateTopographyObjectIdException(target.id)
        return self

    def with_obstacles(self, new_obstacles: Iterable[Obstacle]) -> Topography:
        for obstacle in new_obstacles:
            if not self._is_valid_topography_object(obstacle):
                raise InvalidTopographyObjectException(obstacle)
            if not obstacle.id in self.object_ids:
                self.obstacles.append(obstacle)
                self.object_ids.add(obstacle.id)
            else:
                raise DuplicateTopographyObjectIdException(obstacle.id)
        return self


class InvalidTopographyObjectException(Exception):
    def __init__(self, obj: TopographyObject):
        super().__init__("{} is invalid for this Topography.".format(str(obj)))


class DuplicateTopographyObjectIdException(Exception):
    def __init__(self, id: int):
        super().__init__("Topography object with id {} already exists in this Topography".format(id))
