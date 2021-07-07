from __future__ import annotations
from typing import List, Tuple, Iterable, Set, Dict
from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from enum import Enum


class TopographyObjectType(Enum):
    RECTANGULAR = "RECTANGULAR"


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


source_class_mapping = {
    TopographyObjectType.RECTANGULAR.value: RectangularSource
}

target_class_mapping = {
    TopographyObjectType.RECTANGULAR.value: RectangularTarget
}

obstacles_class_mapping = {
    TopographyObjectType.RECTANGULAR.value: RectangularObstacle
}


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

    @classmethod
    def from_dict(cls, d: Dict) -> Topography:
        if 'sources' not in d:
            raise TopographyReconstructionException(
                "Object must include 'sources'")
        sources = []
        for source_dict in d['sources']:
            if source_dict['type'] in TopographyObjectType.__members__:
                sources.append(source_class_mapping[source_dict['type']](
                    **{key: source_dict[key] for key in source_dict if key != 'type'}))
            else:
                raise UndefinedTopographyObjectType(source_dict['type'])
        if 'targets' not in d:
            raise TopographyReconstructionException(
                "Object must include 'targets'")
        targets = []
        for target_dict in d['targets']:
            if target_dict['type'] in TopographyObjectType.__members__:
                targets.append(target_class_mapping[target_dict['type']](
                    **{key: target_dict[key] for key in target_dict if key != 'type'}))
            else:
                raise UndefinedTopographyObjectType(target_dict['type'])
        if 'obstacles' not in d:
            raise TopographyReconstructionException(
                "Object must include 'obstacles'")
        obstacles = []
        for obstacle_dict in d['obstacles']:
            if obstacle_dict['type'] in TopographyObjectType.__members__:
                obstacles.append(source_class_mapping[obstacle_dict['type']](
                    **{key: obstacle_dict[key] for key in obstacle_dict if key != 'type'}))
            else:
                raise UndefinedTopographyObjectType(obstacle_dict['type'])
        if 'width' not in d or 'height' not in d:
            raise TopographyReconstructionException(
                "Object must include 'width' and 'height'")

        return Topography(d['width'], d['height']).with_sources(sources).with_targets(targets).with_obstacles(obstacles)


class InvalidTopographyObjectException(Exception):
    def __init__(self, obj: TopographyObject):
        super().__init__("{} is invalid for this Topography.".format(str(obj)))


class DuplicateTopographyObjectIdException(Exception):
    def __init__(self, id: int):
        super().__init__("Topography object with id {} already exists in this Topography".format(id))


class TopographyReconstructionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UndefinedTopographyObjectType(Exception):
    def __init__(self, type: str):
        super().__init__(type)
