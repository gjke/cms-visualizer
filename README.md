---
description: |
    API documentation for modules: src, src.simulation, src.topography, src.visualization.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `src` {#src}




    
## Sub-modules

* [src.simulation](#src.simulation)
* [src.topography](#src.topography)
* [src.visualization](#src.visualization)






    
# Module `src.simulation` {#src.simulation}







    
## Classes


    
### Class `CannotAddSimulationStepException` {#src.simulation.CannotAddSimulationStepException}




>     class CannotAddSimulationStepException(
>         simulation_step: SimulationStep
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidSimulationStepException` {#src.simulation.InvalidSimulationStepException}




>     class InvalidSimulationStepException(
>         simulation_step: SimulationStep
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `Pedestrian` {#src.simulation.Pedestrian}




>     class Pedestrian(
>         id: int,
>         label: Optional[Text]
>     )


Pedestrian(id: 'int', label: 'Optional[Text]')




    
#### Class variables


    
##### Variable `id` {#src.simulation.Pedestrian.id}



Type: `int`



    
##### Variable `label` {#src.simulation.Pedestrian.label}



Type: `Union[str, NoneType]`






    
### Class `Position` {#src.simulation.Position}




>     class Position(
>         x: int,
>         y: int
>     )


Position(x: 'int', y: 'int')




    
#### Class variables


    
##### Variable `x` {#src.simulation.Position.x}



Type: `int`



    
##### Variable `y` {#src.simulation.Position.y}



Type: `int`






    
### Class `Simulation` {#src.simulation.Simulation}




>     class Simulation(
>         topography: Topography,
>         pedestrians: List[Pedestrian],
>         n_steps: int,
>         simulation_steps: List[SimulationStep]
>     )


Crowd simulation with topography and simulation steps 


Args
-----=
**```topography```** :&ensp;<code>Topography</code>
:   Topography in which the simulation took place


**```pedestrians```** :&ensp;<code>List\[[Pedestrian](#src.simulation.Pedestrian "src.simulation.Pedestrian")]</code>
:   List of pedestrians participating in the simulation


**```n_steps```** :&ensp;<code>int</code>
:   Number of simulation steps


**```simulation_steps```** :&ensp;<code>List\[SimulationStep]</code>
:   List of simulation steps








    
#### Static methods


    
##### `Method from_json` {#src.simulation.Simulation.from_json}




>     def from_json(
>         path: str
>     ) ‑> src.simulation.Simulation


Instantiate a simulation from a JSON file


Args
-----=
**```path```** :&ensp;<code>str</code>
:   Path to the JSON file



Raises
-----=
<code>[SimulationReconstructionException](#src.simulation.SimulationReconstructionException "src.simulation.SimulationReconstructionException")</code>
:   Raised if the simulation could not be reconstructed 



Returns
-----=
Simulation:


    
#### Methods


    
##### Method `add_simulation_step` {#src.simulation.Simulation.add_simulation_step}




>     def add_simulation_step(
>         self,
>         simulation_step: SimulationStep
>     ) ‑> NoneType


Add a simulation step


Args
-----=
**```simulation_step```** :&ensp;<code>SimulationStep</code>
:   The simulation step to add



Raises
-----=
<code>[CannotAddSimulationStepException](#src.simulation.CannotAddSimulationStepException "src.simulation.CannotAddSimulationStepException")</code>
:   Raised if the simulation is already complete


<code>[InvalidSimulationStepException](#src.simulation.InvalidSimulationStepException "src.simulation.InvalidSimulationStepException")</code>
:   Raised if the simulation step is invalid



    
##### Method `is_simulation_complete` {#src.simulation.Simulation.is_simulation_complete}




>     def is_simulation_complete(
>         self
>     ) ‑> bool


A simulation is complete if it has n_steps simulation steps


Returns
-----=
<code>\[bool]</code>
:   True if simulation is complete



    
##### Method `to_json` {#src.simulation.Simulation.to_json}




>     def to_json(
>         self,
>         path: str
>     ) ‑> NoneType


Serialize the simulation to a JSON file


Args
-----=
**```path```** :&ensp;<code>str</code>
:   Path to the JSON file



    
### Class `SimulationReconstructionException` {#src.simulation.SimulationReconstructionException}




>     class SimulationReconstructionException(
>         message: str
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `src.topography` {#src.topography}







    
## Classes


    
### Class `DuplicateTopographyObjectIdException` {#src.topography.DuplicateTopographyObjectIdException}




>     class DuplicateTopographyObjectIdException(
>         id: int
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `InvalidTopographyObjectException` {#src.topography.InvalidTopographyObjectException}




>     class InvalidTopographyObjectException(
>         obj: TopographyObject
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `RectangularObstacle` {#src.topography.RectangularObstacle}




>     class RectangularObstacle(
>         id: int,
>         x: int,
>         y: int,
>         width: int,
>         height: int
>     )


RectangularTopographyObject(id: 'int', x: 'int', y: 'int', width: 'int', height: 'int')


    
#### Ancestors (in MRO)

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)
* [src.topography.TopographyObject](#src.topography.TopographyObject)
* [abc.ABC](#abc.ABC)



    
#### Class variables


    
##### Variable `height` {#src.topography.RectangularObstacle.height}



Type: `int`



    
##### Variable `width` {#src.topography.RectangularObstacle.width}



Type: `int`






    
### Class `RectangularSource` {#src.topography.RectangularSource}




>     class RectangularSource(
>         id: int,
>         x: int,
>         y: int,
>         width: int,
>         height: int
>     )


RectangularTopographyObject(id: 'int', x: 'int', y: 'int', width: 'int', height: 'int')


    
#### Ancestors (in MRO)

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)
* [src.topography.TopographyObject](#src.topography.TopographyObject)
* [abc.ABC](#abc.ABC)



    
#### Class variables


    
##### Variable `height` {#src.topography.RectangularSource.height}



Type: `int`



    
##### Variable `width` {#src.topography.RectangularSource.width}



Type: `int`






    
### Class `RectangularTarget` {#src.topography.RectangularTarget}




>     class RectangularTarget(
>         id: int,
>         x: int,
>         y: int,
>         width: int,
>         height: int
>     )


RectangularTopographyObject(id: 'int', x: 'int', y: 'int', width: 'int', height: 'int')


    
#### Ancestors (in MRO)

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)
* [src.topography.TopographyObject](#src.topography.TopographyObject)
* [abc.ABC](#abc.ABC)



    
#### Class variables


    
##### Variable `height` {#src.topography.RectangularTarget.height}



Type: `int`



    
##### Variable `width` {#src.topography.RectangularTarget.width}



Type: `int`






    
### Class `RectangularTopographyObject` {#src.topography.RectangularTopographyObject}




>     class RectangularTopographyObject(
>         id: int,
>         x: int,
>         y: int,
>         width: int,
>         height: int
>     )


RectangularTopographyObject(id: 'int', x: 'int', y: 'int', width: 'int', height: 'int')


    
#### Ancestors (in MRO)

* [src.topography.TopographyObject](#src.topography.TopographyObject)
* [abc.ABC](#abc.ABC)


    
#### Descendants

* [src.topography.RectangularObstacle](#src.topography.RectangularObstacle)
* [src.topography.RectangularSource](#src.topography.RectangularSource)
* [src.topography.RectangularTarget](#src.topography.RectangularTarget)


    
#### Class variables


    
##### Variable `height` {#src.topography.RectangularTopographyObject.height}



Type: `int`



    
##### Variable `width` {#src.topography.RectangularTopographyObject.width}



Type: `int`






    
#### Methods


    
##### Method `get_max_coordinates` {#src.topography.RectangularTopographyObject.get_max_coordinates}




>     def get_max_coordinates(
>         self
>     ) ‑> Tuple[int, int]




    
##### Method `get_min_coordinates` {#src.topography.RectangularTopographyObject.get_min_coordinates}




>     def get_min_coordinates(
>         self
>     ) ‑> Tuple[int, int]




    
### Class `Topography` {#src.topography.Topography}




>     class Topography(
>         width: int,
>         height: int
>     )


A topography for a crowd simulation


Args
-----=
**```width```** :&ensp;<code>int</code>
:   width of the area


**```height```** :&ensp;<code>int</code>
:   height of the area






    
#### Class variables


    
##### Variable `object_ids` {#src.topography.Topography.object_ids}



Type: `Set[int]`



    
##### Variable `obstacles` {#src.topography.Topography.obstacles}



Type: `List[src.topography.TopographyObject]`



    
##### Variable `sources` {#src.topography.Topography.sources}



Type: `List[src.topography.TopographyObject]`



    
##### Variable `targets` {#src.topography.Topography.targets}



Type: `List[src.topography.TopographyObject]`





    
#### Static methods


    
##### `Method from_dict` {#src.topography.Topography.from_dict}




>     def from_dict(
>         d: Dict
>     ) ‑> src.topography.Topography


Instanciate a topography object from a dictionary


Args
-----=
**```d```** :&ensp;<code>Dict</code>
:   Dictionary representation of the topography



Raises
-----=
<code>[TopographyReconstructionException](#src.topography.TopographyReconstructionException "src.topography.TopographyReconstructionException")</code>
:   Raised if the topography could not be reconstructed 


<code>[UndefinedTopographyObjectType](#src.topography.UndefinedTopographyObjectType "src.topography.UndefinedTopographyObjectType")</code>
:   Raised if an unknown topography object has been detected



Returns
-----=
Topography:


    
#### Methods


    
##### Method `to_dict` {#src.topography.Topography.to_dict}




>     def to_dict(
>         self
>     ) ‑> Dict[str, Any]


Convert the topography to a dictionary


Returns
-----=
<code>Dict\[str, Any]</code>
:   Dictionary representation of the topography



    
##### Method `with_obstacles` {#src.topography.Topography.with_obstacles}




>     def with_obstacles(
>         self,
>         new_obstacles: Iterable[Obstacle]
>     ) ‑> src.topography.Topography


Add obstacles


Args
-----=
**```new_targets```** :&ensp;<code>Iterable\[[TopographyObject](#src.topography.TopographyObject "src.topography.TopographyObject")]</code>
:   Obstacles to add 



Raises
-----=
<code>[InvalidTopographyObjectException](#src.topography.InvalidTopographyObjectException "src.topography.InvalidTopographyObjectException")</code>
:   Raised if the provided obstacle is an invalid topography object


<code>[DuplicateTopographyObjectIdException](#src.topography.DuplicateTopographyObjectIdException "src.topography.DuplicateTopographyObjectIdException")</code>
:   Raised if such object id already exists



Returns
-----=
<code>[Topography](#src.topography.Topography "src.topography.Topography")</code>
:   Topography with updated obstacles



    
##### Method `with_sources` {#src.topography.Topography.with_sources}




>     def with_sources(
>         self,
>         new_sources: Iterable[Source]
>     ) ‑> src.topography.Topography


Add sources 


Args
-----=
**```new_sources```** :&ensp;<code>Iterable\[[TopographyObject](#src.topography.TopographyObject "src.topography.TopographyObject")]</code>
:   Sources to add



Raises
-----=
<code>[InvalidTopographyObjectException](#src.topography.InvalidTopographyObjectException "src.topography.InvalidTopographyObjectException")</code>
:   Raised if the provided source is an invalid topography object


<code>[DuplicateTopographyObjectIdException](#src.topography.DuplicateTopographyObjectIdException "src.topography.DuplicateTopographyObjectIdException")</code>
:   Raised if such object id already exists



Returns
-----=
<code>[Topography](#src.topography.Topography "src.topography.Topography")</code>
:   Topography with updated sources



    
##### Method `with_targets` {#src.topography.Topography.with_targets}




>     def with_targets(
>         self,
>         new_targets: Iterable[Target]
>     ) ‑> src.topography.Topography


Add targets


Args
-----=
**```new_targets```** :&ensp;<code>Iterable\[[TopographyObject](#src.topography.TopographyObject "src.topography.TopographyObject")]</code>
:   Targets to add 



Raises
-----=
<code>[InvalidTopographyObjectException](#src.topography.InvalidTopographyObjectException "src.topography.InvalidTopographyObjectException")</code>
:   Raised if the provided target is an invalid topography object


<code>[DuplicateTopographyObjectIdException](#src.topography.DuplicateTopographyObjectIdException "src.topography.DuplicateTopographyObjectIdException")</code>
:   Raised if such object id already exists



Returns
-----=
<code>[Topography](#src.topography.Topography "src.topography.Topography")</code>
:   Topography with updated targets



    
### Class `TopographyObject` {#src.topography.TopographyObject}




>     class TopographyObject(
>         id: int,
>         x: int,
>         y: int
>     )


TopographyObject(id: 'int', x: 'int', y: 'int')


    
#### Ancestors (in MRO)

* [abc.ABC](#abc.ABC)


    
#### Descendants

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)


    
#### Class variables


    
##### Variable `id` {#src.topography.TopographyObject.id}



Type: `int`



    
##### Variable `type` {#src.topography.TopographyObject.type}



Type: `src.topography.TopographyObjectType`



    
##### Variable `x` {#src.topography.TopographyObject.x}



Type: `int`



    
##### Variable `y` {#src.topography.TopographyObject.y}



Type: `int`





    
#### Static methods


    
##### `Method get_max_coordinates` {#src.topography.TopographyObject.get_max_coordinates}




>     def get_max_coordinates() ‑> Tuple[int, int]




    
##### `Method get_min_coordinates` {#src.topography.TopographyObject.get_min_coordinates}




>     def get_min_coordinates() ‑> Tuple[int, int]





    
#### Methods


    
##### Method `to_dict` {#src.topography.TopographyObject.to_dict}




>     def to_dict(
>         self
>     ) ‑> Dict[str, Any]




    
### Class `Source` {#src.topography.TopographyObject}




>     class Source(
>         id: int,
>         x: int,
>         y: int
>     )


TopographyObject(id: 'int', x: 'int', y: 'int')


    
#### Ancestors (in MRO)

* [abc.ABC](#abc.ABC)


    
#### Descendants

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)


    
#### Class variables


    
##### Variable `id` {#src.topography.TopographyObject.id}



Type: `int`



    
##### Variable `type` {#src.topography.TopographyObject.type}



Type: `src.topography.TopographyObjectType`



    
##### Variable `x` {#src.topography.TopographyObject.x}



Type: `int`



    
##### Variable `y` {#src.topography.TopographyObject.y}



Type: `int`





    
#### Static methods


    
##### `Method get_max_coordinates` {#src.topography.TopographyObject.get_max_coordinates}




>     def get_max_coordinates() ‑> Tuple[int, int]




    
##### `Method get_min_coordinates` {#src.topography.TopographyObject.get_min_coordinates}




>     def get_min_coordinates() ‑> Tuple[int, int]





    
#### Methods


    
##### Method `to_dict` {#src.topography.TopographyObject.to_dict}




>     def to_dict(
>         self
>     ) ‑> Dict[str, Any]




    
### Class `Target` {#src.topography.TopographyObject}




>     class Target(
>         id: int,
>         x: int,
>         y: int
>     )


TopographyObject(id: 'int', x: 'int', y: 'int')


    
#### Ancestors (in MRO)

* [abc.ABC](#abc.ABC)


    
#### Descendants

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)


    
#### Class variables


    
##### Variable `id` {#src.topography.TopographyObject.id}



Type: `int`



    
##### Variable `type` {#src.topography.TopographyObject.type}



Type: `src.topography.TopographyObjectType`



    
##### Variable `x` {#src.topography.TopographyObject.x}



Type: `int`



    
##### Variable `y` {#src.topography.TopographyObject.y}



Type: `int`





    
#### Static methods


    
##### `Method get_max_coordinates` {#src.topography.TopographyObject.get_max_coordinates}




>     def get_max_coordinates() ‑> Tuple[int, int]




    
##### `Method get_min_coordinates` {#src.topography.TopographyObject.get_min_coordinates}




>     def get_min_coordinates() ‑> Tuple[int, int]





    
#### Methods


    
##### Method `to_dict` {#src.topography.TopographyObject.to_dict}




>     def to_dict(
>         self
>     ) ‑> Dict[str, Any]




    
### Class `Obstacle` {#src.topography.TopographyObject}




>     class Obstacle(
>         id: int,
>         x: int,
>         y: int
>     )


TopographyObject(id: 'int', x: 'int', y: 'int')


    
#### Ancestors (in MRO)

* [abc.ABC](#abc.ABC)


    
#### Descendants

* [src.topography.RectangularTopographyObject](#src.topography.RectangularTopographyObject)


    
#### Class variables


    
##### Variable `id` {#src.topography.TopographyObject.id}



Type: `int`



    
##### Variable `type` {#src.topography.TopographyObject.type}



Type: `src.topography.TopographyObjectType`



    
##### Variable `x` {#src.topography.TopographyObject.x}



Type: `int`



    
##### Variable `y` {#src.topography.TopographyObject.y}



Type: `int`





    
#### Static methods


    
##### `Method get_max_coordinates` {#src.topography.TopographyObject.get_max_coordinates}




>     def get_max_coordinates() ‑> Tuple[int, int]




    
##### `Method get_min_coordinates` {#src.topography.TopographyObject.get_min_coordinates}




>     def get_min_coordinates() ‑> Tuple[int, int]





    
#### Methods


    
##### Method `to_dict` {#src.topography.TopographyObject.to_dict}




>     def to_dict(
>         self
>     ) ‑> Dict[str, Any]




    
### Class `TopographyObjectType` {#src.topography.TopographyObjectType}




>     class TopographyObjectType(
>         value,
>         names=None,
>         *,
>         module=None,
>         qualname=None,
>         type=None,
>         start=1
>     )


An enumeration.


    
#### Ancestors (in MRO)

* [enum.Enum](#enum.Enum)



    
#### Class variables


    
##### Variable `RECTANGULAR` {#src.topography.TopographyObjectType.RECTANGULAR}









    
### Class `TopographyReconstructionException` {#src.topography.TopographyReconstructionException}




>     class TopographyReconstructionException(
>         message: str
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `UndefinedTopographyObjectType` {#src.topography.UndefinedTopographyObjectType}




>     class UndefinedTopographyObjectType(
>         type: str
>     )


Common base class for all non-exit exceptions.


    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `src.visualization` {#src.visualization}







    
## Classes


    
### Class `Visualizer` {#src.visualization.Visualizer}




>     class Visualizer(
>         simulation: src.simulation.Simulation,
>         cell_width: int,
>         cell_height: int,
>         canvas_width: int,
>         canvas_height: int
>     )










    
#### Methods


    
##### Method `build_gui` {#src.visualization.Visualizer.build_gui}




>     def build_gui(
>         self
>     )




    
##### Method `draw` {#src.visualization.Visualizer.draw}




>     def draw(
>         self,
>         step: int
>     )


:param step: Which simulation step of the simulation should be drawn
:return: canvas with the drawn image


-----
Generated by *pdoc* 0.9.2 (<https://pdoc3.github.io>).
