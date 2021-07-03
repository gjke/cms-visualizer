from src.simulation import Simulation
from ipycanvas import Canvas, hold_canvas
import numpy as np

import ipywidgets as widgets
from ipywidgets import interact, Play, interactive
from IPython.display import display

class Visualizer:
    def __init__(self,simulation: Simulation,cell_width: int, cell_height: int):
        self.simulation = simulation
        self.cell_width = cell_width
        self.cell_height = cell_height

    def draw(self, step: int):
        '''

        :param step: Which simulation step of the simulation should be drawn
        :return: canvas with the drawn image
        '''
        canvas = Canvas()
        canvas.clear()
        with hold_canvas(canvas):
            indices = np.indices((self.simulation.topography.width, self.simulation.topography.width))
            row_indices = indices[0].flatten()
            column_indices = indices[1].flatten()
            canvas.stroke_rects(
                x=column_indices * self.cell_width,
                y=row_indices * self.cell_height,
                width=self.cell_width,
                height=self.cell_height
            )

            pedestrians_coordinates = [s for s in self.simulation.simulation_steps[step].values()]
            canvas.fill_style = 'red'
            canvas.fill_rects(
                x=[p.x * self.cell_width for p in pedestrians_coordinates],
                y=[p.y * self.cell_height for p in pedestrians_coordinates],
                width=self.cell_width - 1,
                height=self.cell_height - 1
            )
            # draw obstacles
            canvas.fill_style = 'black'
            canvas.fill_rects(
                x=[p.x * self.cell_width for p in self.simulation.topography.obstacles],
                y=[p.y * self.cell_height for p in self.simulation.topography.obstacles],
                width=self.cell_width - 1,
                height=self.cell_height - 1
            )
            # draw target
            canvas.fill_style = 'green'
            canvas.fill_rects(
                x=[p.x * self.cell_width for p in self.simulation.topography.targets],
                y=[p.y * self.cell_height for p in self.simulation.topography.targets],
                width=self.cell_width - 1,
                height=self.cell_height - 1
            )
            # draw sources
            canvas.fill_style = 'blue'
            canvas.fill_rects(
                x=[p.x * self.cell_width for p in self.simulation.topography.sources],
                y=[p.y * self.cell_height for p in self.simulation.topography.sources],
                width=self.cell_width - 1,
                height=self.cell_height - 1
            )
        display(canvas)
        return canvas

    def build_gui(self):
        play = widgets.Play(
            value=0,
            min=0,
            max=2,
            step=1,
            description="Press play",
            disabled=False
        )
        slider = widgets.IntSlider(
            value=0,
            min=0,
            max=2,
            step=1)
        widgets.jslink((play, 'value'), (slider, 'value'))
        layout = interactive(self.draw, step=play)
        return widgets.VBox([slider, layout])