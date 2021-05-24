#!/usr/bin/env python3.9

import math

from datetime import datetime

import pygame

import app
import fluids

def create_sim(sim_size):
    sim = fluids.simulator.Simulator(
        sim_size,
        init_diffusion=1.0,
        init_viscosity=1.0,
        time_rate=0.01
    )

    # adding a solid square of fluid with constant velocity
    square_density = 1.0
    square_x_velocity = 10
    square_y_velocity = 10
    square_x_offset = 2
    square_y_offset = 2
    square_size = 8

    for x in range(square_x_offset, square_size + square_x_offset):
        for y in range(square_y_offset, square_size + square_y_offset):
            sim.add_density((x, y), square_density)

    for x in range(square_x_offset, square_size + square_x_offset):
        for y in range(square_y_offset, square_size + square_y_offset):
            # modulating velocity by Y-component
            yn = math.pi * (y / square_size)
            vx = square_x_velocity
            vy = square_y_velocity * math.sin(yn)
            sim.add_velocity((x, y), (vx, vy))

    return sim

def main():
    # configuring:
    pygame.font.init()
    debug_font = pygame.font.SysFont("monospace", 15)

    draw_grid_cells = False
    grid_size = 16
    sim_size = 32
    window_size = sim_size * grid_size
    grid_color = (0xff, 0xff, 0xff, 0x80)

    # setting up initial state:
    sim = create_sim(sim_size)

    frame_index = 0
    last_frame_time = datetime.now()

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

        # debug: ensure we actually render
        # screen.fill((255, 0, 0))

    app.run(window_size, window_size, "demo-3", render_cb, desired_updates_per_sec=60)

import pygame
from pygame_widgets import Button
from pygame_widgets import TextBox, Slider
def output():
    # Get text in the textbox
    print(textbox.getText())
    
pygame.init()
win = pygame.display.set_mode((600, 600))


resetButton = Button(
            win, 50, 50, 50, 25, text='Reset Simulation',
            fontSize=10, margin=5,
            inactiveColour=(125, 125, 125), hoverColour=(200,0,0),
            pressedColour=(0, 255, 0), radius=0,
            onRelease=lambda: pygame.quit()
         )


textbox = TextBox(win, 100, 500, 300, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=output, radius=10, borderThickness=5)

viscText = TextBox(win, 100, 250, 75, 25, fontSize=15,colour=(255,255,255),
                  borderColour=(255, 255, 255), textColour=(0, 0, 0),
                  onSubmit=output, radius=0, borderThickness=5)

viscInput = TextBox(win, 175, 250, 100, 25, fontSize=15,colour=(255,255,255),
                  borderColour=(0, 0, 0), textColour=(0, 200, 0),
                  onSubmit=output, radius=0, borderThickness=5)

slider = Slider(win, 100, 100,300, 40, min=1, max=100, step=1)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            pygame.quit()

    win.fill((255, 255, 255))
    
    slider.listen(events)
    slider.draw()
    #textbox.setText(slider.getValue())
    viscText.setText("Viscosity: ")
    viscText.draw()
    viscInput.listen(events)
    viscInput.draw()
    resetButton.listen(events)
    resetButton.draw()
    textbox.listen(events)
    
    textbox.draw()
    #textbox.onSubmit(args, kwargs)
    pygame.display.update()

    

    

if __name__ == "__main__":
    main()

