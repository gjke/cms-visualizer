from src.simulation import Simulation
from ipycanvas import Canvas, hold_canvas
import numpy as np

import ipywidgets as widgets
from ipywidgets import interact, Play, interactive
from IPython.display import display


class Visualizer:
    def __init__(self, simulation: Simulation, cell_width: int, cell_height: int,canvas_width: int,canvas_height:int):
        self.simulation = simulation
        self.cell_width = cell_width
        self.cell_height = cell_height
        #self.canvas = Canvas(width=self.simulation.topography.width *
        #                    cell_width, height=self.simulation.topography.height * cell_height)
        self.canvas = Canvas(width = canvas_width,height = canvas_height)

    def draw(self, step: int):
        '''

        :param step: Which simulation step of the simulation should be drawn
        :return: canvas with the drawn image
        '''
        unit_width = self.canvas.width/self.simulation.topography.width
        unit_height = self.canvas.height/self.simulation.topography.height
        self.canvas.clear()
        with hold_canvas(self.canvas):
            indices = np.indices((int(self.canvas.width/self.cell_width),int(self.canvas.height/self.cell_height)))
            row_indices = indices[0].flatten()
            column_indices = indices[1].flatten()
            self.canvas.stroke_rects(
                x=column_indices * self.cell_width,
                y=row_indices * self.cell_height,
                width=self.cell_width,
                height=self.cell_height
            )
            '''
            pedestrians_coordinates = [
                s for s in self.simulation.simulation_steps[step].values()]
            self.canvas.fill_style = 'red'
            self.canvas.fill_rects(
                x=[round(p.x*unit_width) for p in pedestrians_coordinates],
                y=[round(p.y*unit_height) for p in pedestrians_coordinates],
                width=self.cell_width - 1,
                height=self.cell_height - 1
            )
            '''
            # draw obstacles
            self.canvas.fill_style = 'black'
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.obstacles],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.obstacles],
                width=[round(p.width * unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.obstacles],
                height=[round(p.height * unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.obstacles]
            )
            # draw target
            self.canvas.fill_style = 'green'
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.targets],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.targets],
                width=[round(p.width * unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.targets],
                height=[round(p.height * unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.targets]
            )
            # draw sources
            self.canvas.fill_style = 'blue'
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.sources],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.sources],
                width=[round(p.width* unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.sources],
                height=[round(p.height*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.sources]
            )
        display(self.canvas)

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
