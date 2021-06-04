import pygame

initial_fill_color = (255, 0, 255, 0xff)


def run(width, height, caption,
        run_menu_cb=None, render_cb=None, init_cb=None, de_init_cb=None, should_yield_to_menu_cb=None,
        desired_updates_per_sec=60):
    #
    # Validating params:
    #

    if render_cb is None:
        # re-defining render_cb to overwrite previous,
        # un-callable definition.
        # - this way, we do not branch each loop iteration.
        def render_cb(screen):
            report = "Oops! Did you forget to pass a `render_cb` callback to `app.run`?"
            label = debug_font.render(report, True, (0x00, 0x00, 0x00, 0xff))
            screen.blit(label, (10, 10))

    if run_menu_cb is None:
        def run_menu_cb(screen):
            print("WARNING: no `run_menu_cb` was passed to the app. This will result in an infinite simulation loop.")
            return True

    if init_cb is None:
        def init_cb(screen, pygame_widgets_event_listener_list):
            pass

    if de_init_cb is None:
        def de_init_cb():
            pass

    if should_yield_to_menu_cb is None:
        def should_yield_to_menu_cb():
            return False

    #
    # Running the app:
    # - a simple infinite loop between two states: running a menu, then a simulation.
    # - INFURIATINGLY, pygame_menu requires `pygame.init` instead of a subsystem init, which would speed up startup
    #   by a lot.
    #

    pygame.init()
    # pygame.display.init()

    pygame.display.set_caption(caption)

    debug_font = pygame.font.SysFont("monospace", 20)

    pygame_widgets_event_listener_list = []

    clock = pygame.time.Clock()

    screen: pygame.Surface = pygame.display.set_mode((width, height))

    while True:
        keep_running = run_menu_cb(screen)
        if not keep_running:
            break

        keep_running = run_simulation(
            screen, init_cb, de_init_cb, render_cb, should_yield_to_menu_cb, pygame_widgets_event_listener_list, clock,
            desired_updates_per_sec
        )
        if not keep_running:
            break

    pygame.quit()


def run_simulation(
        screen, init_cb, de_init_cb, render_cb, should_yield_to_menu_cb,
        pygame_widgets_event_listener_list, clock, desired_updates_per_sec
):
    # by default, when the simulation ends, the app loops back to the main menu.
    # this attribute can be set to 'False' before returning to change this.
    keep_running = True

    # allowing client to initialize using the screen instance:
    if init_cb is not None:
        init_cb(screen, pygame_widgets_event_listener_list)

    # Clearing the screen initially:
    # DEBUG: filling screen with magenta/fuchsia
    screen.fill(initial_fill_color)

    is_running = True
    while is_running:
        #
        # Polling for user input:
        #

        # storing events as a list for later (in case it is an iterator)
        events = list(pygame.event.get())

        # Managing our inputs:
        for event in events:
            # checking for 'quit' events:
            if event.type == pygame.QUIT:
                # request exiting the application (main-menu and simulator)
                is_running = False
                keep_running = False

            # checking for keyboard events to open the main menu:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # request return to main-menu:
                    is_running = False
                    keep_running = True

        # Managing Pygame Widgets events:
        for listener in pygame_widgets_event_listener_list:
            listener.listen(events)

        # Managing `should_quit_cb`:
        if should_yield_to_menu_cb is not None:
            if should_yield_to_menu_cb():
                keep_running = True
                break

        #
        # Rendering:
        #

        screen.fill(initial_fill_color)
        render_cb(screen)
        pygame.display.flip()

        # Sleeping:
        clock.tick(desired_updates_per_sec)

    if de_init_cb is not None:
        de_init_cb()

    return keep_running
