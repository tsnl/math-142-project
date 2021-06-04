#!/usr/bin/env python3.9

import math

from datetime import datetime

import pygame
from pygame_widgets import Button
from pygame_widgets import TextBox, Slider
import pygame_menu

import app
import fluids


def create_sim(sim_size, viscosity_input, diffusion_input, time_rate_input, velocity_field):
    sim = fluids.simulator.Simulator(
        sim_size,
        init_diffusion=diffusion_input,
        init_viscosity=viscosity_input,
        time_rate=time_rate_input
        
    )
    reset_sim(sim, velocity_field)
    return sim
    
def reset_sim(sim, velocity_field):
    #need a function called clear to wipe all densities and velocities
    
    # adding a solid square of fluid with constant velocity
    square_density = 1.0
    square_x_velocity = 10
    square_y_velocity = 10
    square_x_offset = 10
    square_y_offset = 10
    square_size = 8
    
    for x in range(square_x_offset, square_size + square_x_offset):
        for y in range(square_y_offset +  int(square_y_offset/4), square_size + int(3*square_y_offset/4)):
            sim.add_density((x, y), square_density)
    
    if (velocity_field == 'Outflow'):
        print('Outflow velocity confirmed')
        for x in range(square_x_offset, square_size + square_x_offset):
            for y in range(square_y_offset, square_size + square_y_offset):
                # modulating velocity by Y-component
                
                vx = 10*(x - (square_size/2 + square_x_offset))
                vy = 10*(y - (square_size/2 + square_y_offset))
                sim.add_velocity((x, y), (vx, vy))
                
    elif (velocity_field == 'Spiral'):
        print('Spiral velocity confirmed')
        for x in range(int(square_x_offset/2), 2*square_size + square_x_offset):
            for y in range(int(square_y_offset/2), 2*square_size + square_y_offset):
                # modulating velocity by Y-component
                
                x_diff = x - (square_size/2 + square_x_offset)
                y_diff = y - (square_size/2 + square_y_offset)
                if x_diff>0:
                    theta = math.atan(y_diff/(x_diff+.00001))
                
                else:
                    theta = math.atan(y_diff/(x_diff+.00001)) + math.pi
                """
                elif (x_diff == 0) && (y_diff > 0):
                    theta = math.pi/2
                """
                    
                rad = math.sqrt(x_diff**2 + y_diff**2)
                
                vx = 100*rad*(math.sin(theta))
                vy = 100*rad*(math.cos(theta))
                sim.add_velocity((x, y), (vx, vy))
    elif (velocity_field == 'Up'):
        for x in range(square_x_offset, square_size + square_x_offset):
            for y in range(square_y_offset, square_size + square_y_offset):
                vx = 0
                vy = 100
                sim.add_velocity((x, y), (vx, vy))
    else:
        print('Error in velo field')
        
                
    """
    
    for x in range(square_x_offset, square_size + square_x_offset):
        for y in range(square_y_offset, square_size + square_y_offset):
            # modulating velocity by Y-component
            yn = math.pi * (y / square_size)
            vx = square_x_velocity
            vy = square_y_velocity * math.sin(yn)
            sim.add_velocity((x, y), (vx, vy))
    """

    


def main():
    # configuring:
    pygame.font.init()
    debug_font = pygame.font.SysFont("monospace", 15)
    viscosity_input = 1
    diffusion_input = 1
    time_rate_input = .01
    draw_grid_cells = False
    grid_size = 16
    sim_size = 32
    window_size = sim_size * grid_size
    grid_color = (0xff, 0xff, 0xff, 0x80)
    velocity_field = 'Outflow'
    # setting up initial state:
    sim = create_sim(sim_size,viscosity_input, diffusion_input, time_rate_input,velocity_field)

    frame_index = 0
    last_frame_time = datetime.now()

    #
    # defining handler callbacks:
    #
    """
    def output():
        # Get text in the textbox
        print(viscosity_input.getText())
    """

    reset_button = None
    textbox = None
    viscosity_text = None
    viscosity_input = None
    slider = None
    menu = None
    #sim = None
    def init_cb(screen, listener_list):
        nonlocal reset_button, textbox, viscosity_text, viscosity_input, slider, menu, sim, velocity_field
        #NEED TO CALL BACK MENU
        #velocity_field = 'Outflow'
        def set_difficulty(value, difficulty):
        # Do the job here !
            pass
    
        def start_the_game():
            nonlocal menu, sim, velocity_field
            # Do the job here !
            print('started')
            
            #want to begin the simulation now
            #save all the relevant info (velocity field, viscosity, density, etc) pass into the simulation function
            widget = menu.get_widget('Viscosity Input')
            viscosity_input =widget.get_value()
            sim.viscosity = float(viscosity_input)
            print(viscosity_input)
            
            widget = menu.get_widget('Diffusion Input')
            diffusion_input =widget.get_value()
            sim.diffusion = float(diffusion_input)
            print(diffusion_input)
            
            widget = menu.get_widget('Time Rate Input')
            time_step_input =widget.get_value()
            sim.time_rate = float(time_step_input)
            print(time_step_input)
            
            widget = menu.get_widget('Velocity Field')
            selected_velocity_field = widget.get_value()
            velocity_field = selected_velocity_field[0][0]
            print(selected_velocity_field)
            
            #close out the menu
            pygame_menu.events.CLOSE
            menu.disable()
            
        def reset_menu():
            nonlocal menu, sim
            menu = pygame_menu.Menu(400, 500, 'Welcome',
                           theme=pygame_menu.themes.THEME_BLUE)
    
            menu.add.text_input('Viscosity Input: ', default='.1', textinput_id='Viscosity Input')
            menu.add.text_input('Diffusion Input: ', default='1', textinput_id='Diffusion Input')
            menu.add.text_input('Time Rate Input: ', default='.001', textinput_id='Time Rate Input')
            
            velocity_fields = [('Spiral', 1), ('Outflow', 2), ('Up', 3)]
            menu.add.selector('Velocity Field: ', velocity_fields, onchange=set_difficulty, selector_id='Velocity Field')
            menu.add.button('Play', start_the_game, button_id='Play Button')
            menu.add.button('Quit', pygame_menu.events.EXIT)
            
            menu.mainloop(screen)
            reset_sim(sim, velocity_field)
            
            #pass
             
        reset_button = Button(
            screen, window_size/10, window_size*9/10, 80, 50, text='Reset Simulation',
            fontSize=13, margin=5,
            inactiveColour=(125, 125, 125), hoverColour=(200, 0, 0),
            pressedColour=(0, 255, 0), radius=0,
            onRelease=reset_menu
        )
        """
        textbox = TextBox(
            screen, 100, 500, 300, 80, fontSize=50,
            borderColour=(255, 0, 0), textColour=(0, 200, 0),
            onSubmit=output, radius=10, borderThickness=5
        )
        viscosity_text = TextBox(
            screen, 100, 250, 75, 25, fontSize=15, colour=(255, 255, 255),
            borderColour=(255, 255, 255), textColour=(0, 0, 0),
            onSubmit=lambda: print(viscosity_text.getText()), radius=0, borderThickness=5
        )
        viscosity_text.setText("Viscosity: ")
        viscosity_input = TextBox(
            screen, 175, 250, 100, 25, fontSize=15, colour=(255, 255, 255),
            borderColour=(0, 0, 0), textColour=(0, 200, 0),
            onSubmit=lambda: print(viscosity_input.getText()), radius=0, borderThickness=5
        )
        slider = Slider(screen, 100, 100, 300, 40, min=1, max=100, step=1)
        """
        listener_list += [reset_button]
        
            # trying out pygame menu
        
        
        #Create Menu 
            
        menu = pygame_menu.Menu(400, 500, 'Welcome',
                           theme=pygame_menu.themes.THEME_BLUE)
    
        menu.add.text_input('Viscosity Input: ', default='.1', textinput_id='Viscosity Input')
        menu.add.text_input('Diffusion Input: ', default='1', textinput_id='Diffusion Input')
        menu.add.text_input('Time Rate Input: ', default='.001', textinput_id='Time Rate Input')
        velocity_fields = [('Spiral', 1), ('Outflow', 2)]
        menu.add.selector('Velocity Field: ', velocity_fields, onchange=set_difficulty, selector_id='Velocity Field')
        menu.add.button('Play', start_the_game, button_id='Play Button')
        menu.add.button('Quit', pygame_menu.events.EXIT)
        
        menu.mainloop(screen)
        
        #get all relevant values from main menu
        """
        widget = menu.get_widget('Viscosity Input')
        viscosity_input = float(widget.get_value())
        print(viscosity_input)
        
        widget = menu.get_widget('Diffusion Input')
        diffusion_input = float(widget.get_value())
        print(diffusion_input)
        
        widget = menu.get_widget('Time Step Input')
        time_rate_input = float(widget.get_value())
        print(time_rate_input)
        
        widget = menu.get_widget('Velocity Field')
        selected_velocity_field = widget.get_value()
        print(selected_velocity_field)
        """
        
        #create simulation with values from the menu
        #sim = create_sim(sim_size, viscosity_input, diffusion_input, time_rate_input)
        #sim1 = create_sim(sim_size,viscosity_input, diffusion_input, time_rate_input)

    def render_cb(screen):
        nonlocal frame_index, last_frame_time

        # running K simulation steps:
        k = 1
        for i in range(k):
            sim.step()

        #
        # presenting:
        #

        density_array = sim.dump_density_array()
        vx_array = sim.dump_vx_array()
        vy_array = sim.dump_vy_array()
        for grid_x in range(sim.size):
            for grid_y in range(sim.size):
                # updating this cell's pixel rectangle:
                pixel_rect = (
                    grid_x * grid_size,
                    grid_y * grid_size,
                    (grid_x + 1) * grid_size,
                    (grid_y + 1) * grid_size
                )

                # converting the density to a constant in [0,255]:
                density = density_array[sim.ix(grid_x, grid_y)]
                try:
                    z = int(255.0 * density)
                    z = min(max(z, 0), 255)
                    color = (z, z, z)
                except ValueError:
                    color = (255, 0, 0)

                # setting the color:
                screen.fill(color, rect=pixel_rect)

                # drawing a bounding grid rectangle:
                if draw_grid_cells:
                    pygame.draw.rect(screen, grid_color, pixel_rect, width=1)

                # screen.set_at((grid_x, grid_y), color)

        # drawing FPS, updating accounting statistics:
        this_frame_time = datetime.now()

        frame_time = (this_frame_time - last_frame_time).microseconds / 1e6
        frame_rate = 1.0 / frame_time
        frame_time_s = str(frame_time)[:6]
        frame_rate_s = str(frame_rate)[:6]
        report = f"[ix={frame_index} | dt={frame_time_s} | fps={frame_rate_s}]"
        label = debug_font.render(report, False, (0xff, 0xff, 0xff, 0xff))
        screen.blit(label, (window_size - 300, window_size - 25))

        frame_index += 1
        last_frame_time = this_frame_time

        # drawing GUI widgets:
        #slider.draw()
        #viscosity_text.draw()
        #viscosity_input.draw()
        reset_button.draw()
        


        # debug: ensure we actually render
        # screen.fill((255, 0, 0))

    # running the app:
    app.run(
        window_size, window_size,
        "demo-3", init_cb=init_cb, render_cb=render_cb, desired_updates_per_sec=60
    )


if __name__ == "__main__":
    main()

