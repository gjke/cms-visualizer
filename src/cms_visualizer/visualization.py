from .simulation import Simulation
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
        self.canvas = Canvas(width = canvas_width,height = canvas_height,sync_image_data=True)
        self.canvas.on_mouse_down(self.handle_mouse_down)
        self.show_trajectories = False
        self.current_step = 0
        self.color_pedestrian = '#ff0006'
        self.color_obstacle = '#000000'
        self.color_source = '#0006ff'
        self.color_target = '#32d12e'
        self.color_grid = '#000000'
        self.color_trajectorie = '#ff0006'
        self.highlighted_pedestrian = 1
        
        self.pedestrian_info = widgets.Textarea(
                                    value='tmp',
                                    placeholder='',
                                    description='String:',
                                    disabled=False
                                )
        self.update_pedestrian_info()

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
            self.canvas.stroke_style = self.color_grid
            self.canvas.stroke_rects(
                x=column_indices * self.cell_width,
                y=row_indices * self.cell_height,
                width=self.cell_width,
                height=self.cell_height
            )
            
            #draw pedestrian
            pedestrians_coordinates = [s for s in self.simulation.simulation_steps[step].values()]
            pedestrian_radius = [p.radius for p in self.simulation.pedestrians]
            self.canvas.fill_style = self.color_pedestrian
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in pedestrians_coordinates],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in pedestrians_coordinates],
                width=[round(radius*unit_width/self.cell_width)*self.cell_width for radius in pedestrian_radius],
                height=[round(radius*unit_width/self.cell_height)*self.cell_height for radius in pedestrian_radius]
            )
            #highlight the highlighted pedestrian
            self.canvas.fill_style = 'yellow'
            self.canvas.fill_rect(
                x=round(pedestrians_coordinates[self.highlighted_pedestrian].x*unit_width/self.cell_width)*self.cell_width,
                y=round(pedestrians_coordinates[self.highlighted_pedestrian].y*unit_height/self.cell_height)*self.cell_height,
                width=round(pedestrian_radius[self.highlighted_pedestrian]*unit_width/self.cell_width)*self.cell_width,
                height=round(pedestrian_radius[self.highlighted_pedestrian]*unit_width/self.cell_height)*self.cell_height
            )
            # draw obstacles
            self.canvas.fill_style = self.color_obstacle
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.obstacles],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.obstacles],
                width=[round(p.width * unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.obstacles],
                height=[round(p.height * unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.obstacles]
            )
            # draw target
            self.canvas.fill_style = self.color_target
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.targets],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.targets],
                width=[round(p.width * unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.targets],
                height=[round(p.height * unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.targets]
            )
            # draw sources
            self.canvas.fill_style = self.color_source
            self.canvas.fill_rects(
                x=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.sources],
                y=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.sources],
                width=[round(p.width* unit_width/self.cell_width)*self.cell_width for p in self.simulation.topography.sources],
                height=[round(p.height*unit_height/self.cell_height)*self.cell_height for p in self.simulation.topography.sources]
            )
            #Draw Trajectories:
            self.canvas.stroke_style = self.color_trajectorie
            if self.show_trajectories:
                keys = [p.id for p in self.simulation.pedestrians]
                for k in keys:
                    self.canvas.begin_path()
                    position = self.simulation.simulation_steps[0][k]
                    x = round(position.x*unit_width/self.cell_width)*self.cell_width+ self.cell_width*0.5
                    y = round(position.y*unit_height/self.cell_width)*self.cell_width+ self.cell_height*0.5
                    self.canvas.move_to(x,y)
                    for i in range(1,step+1):
                        position = self.simulation.simulation_steps[i][k]
                        x = round(position.x*unit_width/self.cell_width)*self.cell_width + self.cell_width*0.5
                        y = round(position.y*unit_height/self.cell_width)*self.cell_width + self.cell_height*0.5
                        self.canvas.line_to(x,y)
                    self.canvas.stroke()
                
        display(self.canvas)

        
    def handle_mouse_down(self,x,y):
        '''
        This function is called when the user clicks on the canvas.
        :param x: x-coordinate of the mouse position
        :param y: y-coordinate of the mouse position
        :return: None
        '''
        unit_width = self.canvas.width/self.simulation.topography.width
        unit_height = self.canvas.height/self.simulation.topography.height
        
        pedestrians_coordinates = [s for s in self.simulation.simulation_steps[self.current_step].values()]
        pedestrian_radius = [p.radius for p in self.simulation.pedestrians]
        
        px=[round(p.x*unit_width/self.cell_width)*self.cell_width for p in pedestrians_coordinates]
        py=[round(p.y*unit_height/self.cell_height)*self.cell_height for p in pedestrians_coordinates]
        pwidth=[round(radius*unit_width/self.cell_width)*self.cell_width for radius in pedestrian_radius]
        pheight=[round(radius*unit_width/self.cell_height)*self.cell_height for radius in pedestrian_radius]
        
        for i in range(len(pedestrians_coordinates)):
            if x > px[i] and x < px[i]+pwidth[i] and y > py[i] and y < py[i]+pheight[i]:
                self.highlighted_pedestrian = i
                self.update_pedestrian_info()
        self.draw(self.current_step)
            
    def toggle_trajectories(self,toggle_info):
        '''
        This function activates or deactivates the trajectorie visualization
        :param toggle_info: Information from the toggle button widget
        :return: None
        '''
        self.show_trajectories = not self.show_trajectories
        
    def current_canvas_to_png(self, button_info):
        '''
        This function creates a png of the current step
        :param button_info: Information from the button widget
        :return: None
        '''
        self.canvas.to_file(str(self.current_step) + '.png')
        
    def update_step(self,change):
        '''
        This function updates the current step
        :param change: The new information coming from the slider
        :return: None
        '''
        if(change['name'] == 'value'):
            self.current_step = change['new']
            self.update_pedestrian_info()
    
    #Color adjusting functions
    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    def adjust_pedestrian_color(self,change):
        self.color_pedestrian = change['new']
        self.draw(self.current_step)
        
    def adjust_obstacle_color(self,change):
        self.color_obstacle = change['new']
        self.draw(self.current_step)
        
    def adjust_source_color(self,change):
        self.color_source = change['new']
        self.draw(self.current_step)
        
    def adjust_target_color(self,change):
        self.color_target = change['new']
        self.draw(self.current_step)
        
    def adjust_grid_color(self,change):
        self.color_grid = change['new']
        self.draw(self.current_step)
        
    def adjust_trajectorie_color(self,change):
        self.color_trajectorie = change['new']
        self.draw(self.current_step)
    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    
    def update_highlighted_pedestrian(self,change):
        '''
        This function updates highlighted pedestrian via the dropdown
        :param change: The new information coming from the dropdown
        :return: None
        '''
        self.highlighted_pedestrian = change['new']
        self.update_pedestrian_info()
        self.draw(self.current_step)
        
    def update_pedestrian_info(self):
        '''
        This function updates the pedestrian info shown in the textbox
        :return: None
        '''
        pedestrians_coordinates = [s for s in self.simulation.simulation_steps[self.current_step].values()]
        self.pedestrian_info.value = 'id:' + str(self.highlighted_pedestrian) + '\n' 
        self.pedestrian_info.value = self.pedestrian_info.value + 'X: ' + str(pedestrians_coordinates[self.highlighted_pedestrian].x) + '\n'
        self.pedestrian_info.value = self.pedestrian_info.value + 'Y: ' + str(pedestrians_coordinates[self.highlighted_pedestrian].y) + '\n'
        self.pedestrian_info.value = self.pedestrian_info.value + 'Radius: ' + str(self.simulation.pedestrians[self.highlighted_pedestrian].radius) + '\n'
    
    def build_gui(self):
        '''
        This function creates the entire layout with all the interactive functionalities and the rendering.
        :param: None
        :return: Final layout with all the widgets
        '''
        #Play and Slider
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
        widgets.jslink((play, 'value'), (slider, 'value'))
        
        #Trajectories
        trajectories = widgets.ToggleButton(
            value=False,
            description='Show Trajectories',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Toggles the trajectories of the pedestrians',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        trajectories.observe(self.toggle_trajectories, names='value')
        
        #Print Button
        print_as_png = widgets.Button(
            description='Save as .png',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save as -png',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        print_as_png.on_click(self.current_canvas_to_png)
        
        #Colorpickers
        pedestrian_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Pedestrian',
                                    value=self.color_pedestrian,
                                    disabled=False
                                )
        
        obstacle_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Obstacle',
                                    value=self.color_obstacle,
                                    disabled=False
                                )
        
        source_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Source',
                                    value=self.color_source,
                                    disabled=False
                                )
        
        target_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Target',
                                    value=self.color_target,
                                    disabled=False
                                )
        
        grid_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Grid',
                                    value=self.color_grid,
                                    disabled=False
                                )
        
        trajectorie_colorpicker = widgets.ColorPicker(
                                    concise=False,
                                    description='Trajectories',
                                    value=self.color_trajectorie,
                                    disabled=False
                                )
        
        pedestrian_colorpicker.observe(self.adjust_pedestrian_color,names='value')
        obstacle_colorpicker.observe(self.adjust_obstacle_color,names='value')
        source_colorpicker.observe(self.adjust_source_color,names='value')
        target_colorpicker.observe(self.adjust_target_color,names='value')
        grid_colorpicker.observe(self.adjust_grid_color,names='value')
        trajectorie_colorpicker.observe(self.adjust_trajectorie_color,names='value')
        
        #Dropdown
        pedestrian_numbers = []
        pedestrian_numbers.extend(range(0,len(self.simulation.pedestrians)))
        print(pedestrian_numbers)
        
        pedestrian_picker = widgets.Dropdown(
                        options=pedestrian_numbers,
                        value=1,
                        description='Number:',
                        disabled=False,
                )
        pedestrian_picker.observe(self.update_highlighted_pedestrian,names='value')
        
        #Set Layout
        layout = interactive(self.draw, step=play)
        horizontal = widgets.HBox([widgets.VBox([trajectories,print_as_png]),
                                   widgets.VBox([grid_colorpicker,trajectorie_colorpicker,pedestrian_colorpicker,obstacle_colorpicker,source_colorpicker,target_colorpicker]),
                                   widgets.VBox([pedestrian_picker,self.pedestrian_info])])
        return widgets.VBox([horizontal,slider, layout])
