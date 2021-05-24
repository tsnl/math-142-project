import pygame

initial_fill_color = (255, 0, 255, 0xff)


def run(width, height, caption, render_cb=None, init_cb=None, desired_updates_per_sec=60):
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

    #
    # Running the app:
    #

    pygame.init()
    pygame.display.set_caption(caption)

    debug_font = pygame.font.SysFont("monospace", 20)

    pygame_widgets_event_listener_list = []

    clock = pygame.time.Clock()

    screen: pygame.Surface = pygame.display.set_mode((width, height))

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
                is_running = False

            # TODO: check for mouse input events

        # Managing Pygame Widgets events:
        for listener in pygame_widgets_event_listener_list:
            listener.listen(events)

        #
        # Rendering:
        #

        screen.fill(initial_fill_color)
        render_cb(screen)
        pygame.display.flip()

        # Sleeping:
        clock.tick(desired_updates_per_sec)

    pygame.quit()
