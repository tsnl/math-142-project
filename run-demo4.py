#!/usr/bin/env python3.9

import math

from datetime import datetime

import pygame
import pygame_menu

import app
import fluids


VELOCITY_FIELD_CODE_NONE = 'n'
VELOCITY_FIELD_CODE_OUTFLOW = 'o'
VELOCITY_FIELD_CODE_SPIRAL = 's'
VELOCITY_FIELD_CODE_UP = 'u'
VELOCITY_FIELD_CODE_DOWN = 'd'

DEFAULT_VELOCITY_FIELD_CODE = VELOCITY_FIELD_CODE_NONE
DEFAULT_VISCOSITY_VALUE = 1
DEFAULT_DIFFUSION_VALUE = 1
DEFAULT_TIME_RATE_VALUE = 0.001


def create_sim(
        sim_size,
        viscosity_input=DEFAULT_VISCOSITY_VALUE,
        diffusion_input=DEFAULT_DIFFUSION_VALUE,
        time_rate_input=DEFAULT_TIME_RATE_VALUE,
        velocity_field_code=DEFAULT_VELOCITY_FIELD_CODE
):
    sim = fluids.simulator.Simulator(
        sim_size,
        init_diffusion=diffusion_input,
        init_viscosity=viscosity_input,
        time_rate=time_rate_input

    )
    reset_sim(sim, velocity_field_code)
    return sim


def reset_sim(sim, velocity_field_code, clear_all=True):
    # positioning 'the square':
    square_density = 1.0
    square_size = 8
    square_x_offset = (sim.size - square_size) // 2
    square_y_offset = (sim.size - square_size) // 2

    # clearing simulation if requested:
    if clear_all:
        # wiping out everything currently in the sim cells: density and velocity tables.
        sim.clear_density_and_velocity()

        # re-adding a centered solid square of fluid with constant velocity
        for x in range(square_x_offset, square_size + square_x_offset):
            for y in range(square_y_offset, square_size + square_y_offset):
                sim.add_density((x, y), square_density)

    # FIXME: why is the velocity field only applied to the initial square?
    #       - why not the whole state?
    #       - must change bounds of `range` below: simple fix.

    # applying the appropriate initial velocity field:
    if velocity_field_code == VELOCITY_FIELD_CODE_OUTFLOW:
        strength_factor = 1.0

        for x in range(square_x_offset, square_size + square_x_offset):
            for y in range(square_y_offset, square_size + square_y_offset):
                # modulating velocity by Y-component
                vx = strength_factor * (10 * (x - (square_size/2 + square_x_offset)))
                vy = strength_factor * (10 * (y - (square_size/2 + square_y_offset)))
                sim.add_velocity((x, y), (vx, vy))

    elif velocity_field_code == VELOCITY_FIELD_CODE_SPIRAL:
        strength_factor = 0.05

        for x in range(int(square_x_offset/2), 2*square_size + square_x_offset):
            for y in range(int(square_y_offset/2), 2*square_size + square_y_offset):
                # modulating velocity by Y-component

                x_diff = x - (square_size//2 + square_x_offset)
                y_diff = y - (square_size//2 + square_y_offset)
                if x_diff > 0:
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

                vx *= strength_factor
                vy *= strength_factor

                sim.add_velocity((x, y), (vx, vy))

    elif velocity_field_code == VELOCITY_FIELD_CODE_UP or velocity_field_code == VELOCITY_FIELD_CODE_DOWN:
        strength_factor = 100.0

        for x in range(0, square_size):
            for y in range(0, square_size):
                vx = 0
                vy = -100

                vx *= strength_factor
                vy *= strength_factor

                if velocity_field_code == VELOCITY_FIELD_CODE_UP:
                    sim.add_velocity((x, y), (vx, vy))
                elif velocity_field_code == VELOCITY_FIELD_CODE_DOWN:
                    sim.add_velocity((x, y), (vx, -vy))

    elif velocity_field_code == VELOCITY_FIELD_CODE_NONE:
        # do nothing.
        pass

    else:
        print(f'Invalid velocity field code: {velocity_field_code}')
        raise NotImplementedError("Invalid velocity field selected in menu.")


def main():
    # configuring:
    pygame.font.init()
    # debug_font = pygame.font.SysFont("monospace", 15)
    debug_font = pygame.font.Font("./fonts/Nanum_Gothic_Coding/NanumGothicCoding-Regular.ttf", 18)
    draw_grid_lines = False
    grid_size = 24
    sim_size = 32
    window_size = sim_size * grid_size
    grid_color = (0xa0, 0xa0, 0xc0)
    active_v_field_menu_index = 0

    # setting up initial state for the simulation using config:
    sim = create_sim(sim_size)

    # these variables are used to display frame-rate statistics during the simulation:
    frame_index = 0
    last_frame_time = datetime.now()

    #
    # Defining App callbacks:
    # - what to do to 'init', 'de_init', 'render', 'update', or if the user opens the 'main_menu'
    #

    def init_cb(screen, listener_list):
        pass

    def render_cb(screen):
        nonlocal frame_index, last_frame_time

        # running K simulation steps:
        k = 1
        for i in range(k):
            sim.step()

        #
        # acquiring density and velocity arrays and ranges:
        #

        density_array = sim.dump_density_array()
        min_density = density_array.min()
        max_density = density_array.max()
        assert min_density < max_density

        vx_array = sim.dump_vx_array()
        vy_array = sim.dump_vy_array()

        #
        # presenting:
        #

        #
        # drawing densities:
        #

        for grid_x in range(sim.size):
            for grid_y in range(sim.size):
                # updating this cell's pixel rectangle:
                pixel_rect = (
                    grid_x * grid_size,
                    grid_y * grid_size,
                    (grid_x + 1) * grid_size,
                    (grid_y + 1) * grid_size
                )

                # acquiring a density and velocity readings:
                cell_index = sim.ix(grid_x, grid_y)
                density = density_array[cell_index]
                vx, vy = vx_array[cell_index], vy_array[cell_index]

                # normalizing density given min/max of aperture:
                density_normalized = (density - min_density) / max_density

                # density_byte = normal_float_to_byte(density_normalized)

                # ensuring non-zero density is represented by the faintest value possible:
                # if density > 0 and density_byte == 0:
                #     density_byte = 1

                # selecting 'white' color:
                # color = (density_byte, density_byte, density_byte)

                # shades of blue:
                blue_stop = (0x00, 0xbb, 0xff)
                white_stop = (0xff, 0xff, 0xff)
                color = blend_rgb_colors(blue_stop, white_stop, density_normalized)

                # setting the color:
                screen.fill(color, rect=pixel_rect)

                # screen.set_at((grid_x, grid_y), color)

        #
        # drawing grid:
        #

        if draw_grid_lines:
            for grid_x in range(sim.size):
                pixel_x = grid_size * grid_x
                pygame.draw.line(
                    screen, grid_color,
                    start_pos=(pixel_x, 0),
                    end_pos=(pixel_x, window_size)
                )

            for grid_y in range(sim.size):
                pixel_y = grid_size * grid_y
                pygame.draw.line(
                    screen, grid_color,
                    start_pos=(0, pixel_y),
                    end_pos=(window_size, pixel_y)
                )


        #
        # text drawing:
        #

        text_color = (0x00, 0x00, 0x00, 0xae)

        # drawing FPS, updating accounting statistics:
        this_frame_time = datetime.now()

        frame_time = (this_frame_time - last_frame_time).microseconds / 1e6
        frame_rate = 1.0 / frame_time
        frame_time_s = f"{frame_time:.3f}"
        frame_rate_s = f"{frame_rate:.3f}"
        density_s = f"ρ ∈ [{min_density:.3f}, {max_density:.3f}]"
        assert min_density < max_density
        report = f"[ix={frame_index} | dt={frame_time_s} | fps={frame_rate_s} | {density_s}]"
        stats_label = debug_font.render(report, True, text_color)
        screen.blit(stats_label, (window_size - 510, window_size - 25))

        frame_index += 1
        last_frame_time = this_frame_time

        # drawing instructions to press 'escape' or 'space' to open the main menu:
        text = f"Press [SPACE], [ESCAPE], or [RETURN] to open the menu."
        help_label = debug_font.render(text, True, text_color)
        screen.blit(help_label, (window_size - 510, window_size - 50))

        # debug: ensure we actually render
        # screen.fill((255, 0, 0))

    def run_main_menu_cb(screen):
        nonlocal sim, active_v_field_menu_index, draw_grid_lines

        # Writing callbacks:
        # - these functions are called by PyGame-Menu when the user clicks a button or enters text.
        # - these functions update shared variables so that menu state is 'sticky' when we reopen the menu.
        #   - exception is 'keep_app_running' which, once set to False, terminates flow.
        #   - exception is 'clear_sim_state', which is always 'False' by default.
        #   - `sim`, `active_v_field_menu_index`, `draw_grid_cells` are used to store such persistent properties.
        # - they must be written before the widgets they are bound to, so (SEE BELOW) for nonlocal vars.

        keep_running_app = True
        clear_sim_state = False
        active_v_field_code = DEFAULT_VELOCITY_FIELD_CODE

        def exit_main_menu_cb(*args):
            nonlocal menu_widget
            menu_widget.disable()

        def exit_main_menu_and_reset_cb(*args):
            nonlocal clear_sim_state
            clear_sim_state = True
            exit_main_menu_cb()

        def exit_game_cb(*args):
            nonlocal keep_running_app
            keep_running_app = False
            exit_main_menu_cb()

        def set_active_v_field_code(key, code):
            nonlocal active_v_field_code, active_v_field_menu_index
            _, active_v_field_menu_index = key
            active_v_field_code = code

        def help_get_float_prop_from_text_input_widget(text_input_widget):
            ok = True
            try:
                value = float(text_input_widget.get_value())
            except ValueError:
                ok = False
                value = None

            if ok:
                # todo: set widget background color to green
                alarming_pink_color = (255, 171, 171)
                text_input_widget.background_color = alarming_pink_color
            else:
                calming_white_color = (255, 255, 255)
                text_input_widget.background_color = calming_white_color
                # todo: set widget background color to red

            return value

        def set_viscosity_cb(*args):
            parsed_val = help_get_float_prop_from_text_input_widget(viscosity_input_widget)
            if parsed_val is not None:
                sim.viscosity = parsed_val

        def set_diffusion_cb(*args):
            parsed_val = help_get_float_prop_from_text_input_widget(diffusion_input_widget)
            if parsed_val is not None:
                sim.diffusion = parsed_val

        def set_time_rate_cb(*args):
            parsed_val = help_get_float_prop_from_text_input_widget(time_rate_input_widget)
            if parsed_val is not None:
                sim.time_rate = parsed_val

        def toggle_grid_line_cb(key, value):
            nonlocal draw_grid_lines
            draw_grid_lines = value

        #
        # Create the menu widgets:
        #

        # menu-widget contains all other widgets:
        menu_widget = pygame_menu.Menu(title='§ Interactive Fluids §', width=window_size, height=window_size,
                                       theme=pygame_menu.themes.THEME_BLUE)
        menu = menu_widget

        # the `play` button returns to the simulation.
        # - NOTE: this button should be first, for easy return.
        play_btn = menu.add.button("Continue...", exit_main_menu_cb)

        # the `reset` button returns to the simulation, but wipes clear all density and velocity state first:
        reset_btn = menu.add.button("Reset...", exit_main_menu_and_reset_cb)

        # these widgets help configure global sim properties:
        # - note these properties are not reset by `reset_sim`
        viscosity_input_widget = menu.add.text_input("Viscosity Input:", default=str(sim.viscosity),
                                                     onchange=set_viscosity_cb)
        diffusion_input_widget = menu.add.text_input("Diffusion Input:", default=str(sim.diffusion),
                                                     onchange=set_diffusion_cb)
        time_rate_input_widget = menu.add.text_input("Time Rate Input:", default=str(sim.time_rate),
                                                     onchange=set_time_rate_cb)

        # this widget allows the user to select the initial velocity field.
        # - we just add a little bump and then leave the simulation to its own devices
        # - re-opening the menu adds a new bump!
        velocity_fields = [
            ("None", VELOCITY_FIELD_CODE_NONE),
            ("Spiral", VELOCITY_FIELD_CODE_SPIRAL),
            ("Outflow", VELOCITY_FIELD_CODE_OUTFLOW),
            ("Upward", VELOCITY_FIELD_CODE_UP),
            ("Downward", VELOCITY_FIELD_CODE_DOWN)
        ]
        v_field_select_widget = menu.add.selector("Add Velocity Field:", velocity_fields,
                                                  onchange=set_active_v_field_code,
                                                  default=active_v_field_menu_index)

        # # this widget controls whether or not grid cells are drawn:
        grid_opts = [
            ("Off", False),
            ("On", True)
        ]
        default_ix = int(draw_grid_lines)       # 0 or 1? it indexes the right option.
        grid_widget = menu.add.selector("Grid Lines", grid_opts, onchange=toggle_grid_line_cb, default=default_ix)

        # thie widget allows the user to exit the whole app:
        quit_btn = menu.add.button("Quit", exit_game_cb)

        # Unfortunately, PyGame-Menu uses its own blocking render loop.
        # We call it here.
        # After this function, all above callbacks will have run to completion to finish configuring the `sim` instance
        # or other variables used to further change the sim.
        menu.mainloop(screen)

        # `reset_sim` places initial velocities and densities
        reset_sim(sim, velocity_field_code=active_v_field_code, clear_all=clear_sim_state)

        # Returning whether or not to keep the app running:
        return keep_running_app

    def de_init_cb():
        pass

    # running the app:
    app.run(
        window_size, window_size,
        "demo-4",
        init_cb=init_cb,
        render_cb=render_cb,
        run_menu_cb=run_main_menu_cb,
        de_init_cb=de_init_cb,
        desired_updates_per_sec=60
    )


def normal_float_to_byte(x, default=0):
    try:
        xi = abs(int(255.0 * x))
        return clamp(xi, 0, 255)
    except ValueError:
        return default


def blend_rgb_colors(color1, color2, x):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (
        lerp(x, r1, r2),
        lerp(x, g1, g2),
        lerp(x, b1, b2)
    )


def lerp(x, a, b):
    """
    linearly interpolate between two stops
    :param x: a value in [0,1] where 0 indicates all a, and 1 indicates all b
    :param a: the 'a' stop
    :param b: the 'b' stop
    :return: a value y in [a,b] such that (y-a)/(b-a) = 1-x
    """
    return a + (1-x)*(b-a)


def clamp(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x


if __name__ == "__main__":
    main()

