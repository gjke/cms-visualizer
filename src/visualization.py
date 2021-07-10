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
        self.canvas = Canvas(width = canvas_width,height = canvas_height,sync_image_data=True)
        self.show_trajectories = False
        self.current_step = 0

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
            
            pedestrians_coordinates = [s for s in self.simulation.simulation_steps[step].values()]
            pedestrian_radius = [p.radius for p in self.simulation.pedestrians]
            self.canvas.fill_style = 'red'
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in pedestrians_coordinates],
                y=[round(p.y*unit_height/self.cell_width)*self.cell_width for p in pedestrians_coordinates],
                width=[round(radius*unit_width/self.cell_width)*self.cell_width for radius in pedestrian_radius],
                height=[round(radius*unit_width/self.cell_width)*self.cell_width for radius in pedestrian_radius]
            )
            
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
            #Draw Trajectories:
            if self.show_trajectories:
                keys = [p.id for p in self.simulation.pedestrians]
                for k in keys:
                    self.canvas.begin_path()
                    position = self.simulation.simulation_steps[0][k]
                    x = round(position.x*unit_width/self.cell_width)*self.cell_width+ self.cell_width*0.5
                    y = round(position.y*unit_height/self.cell_width)*self.cell_width+ self.cell_height*0.5
                    self.canvas.move_to(x,y)
                    for i in range(1,step+1):
                        position = self.simulation.simulation_steps[step][k]
                        x = round(position.x*unit_width/self.cell_width)*self.cell_width + self.cell_width*0.5
                        y = round(position.y*unit_height/self.cell_width)*self.cell_width + self.cell_height*0.5
                        self.canvas.line_to(x,y)
                    self.canvas.stroke()
                
        display(self.canvas)

    def toggle_trajectories(self,toggle_info):
        self.show_trajectories = not self.show_trajectories
        
    def current_canvas_to_png(self, button_info):
        self.canvas.to_file(str(self.current_step) + '.png')
        
    def update_step(self,change):
        if(change['name'] == 'value'):
            self.current_step = change['new']
        
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
        
        slider.observe(self.update_step)
        
        trajectories = widgets.ToggleButton(
            value=False,
            description='Show Trajectories',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Toggles the trajectories of the pedestrians',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        print_as_png = widgets.Button(
            description='Save as .png',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save as -png',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        print_as_png.on_click(self.current_canvas_to_png)
        
        trajectories.observe(self.toggle_trajectories, names='value')
        
        widgets.jslink((play, 'value'), (slider, 'value'))
        layout = interactive(self.draw, step=play)
        return widgets.VBox([slider,trajectories,print_as_png, layout])
