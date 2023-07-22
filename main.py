
## MAIN GAME FILE ##

import pygame
import game_objects as objects
import game_load as load
import game_render as render
import game_control as control
import game_values as value

# TODO: load and display a map when in mission context
# TODO: add hover highlights to map
# TODO: add movable character to map
# TODO: add vision to character
# TODO: change sprites out of vision to greyscale

# SETUP PYGAME
pygame.init()  # initialize pygame
pygame.key.set_repeat(1, 50)  # set all keys to repeat when held down
CLOCK = pygame.time.Clock()  # used to lock fps in main game loop

# SETUP DISPLAY
WIN_W = 1600  # width of the window
WIN_H = WIN_W // 16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W // 16 * 9  # 16:9 aspect ratio
WIN_TITLE = 'untitled game'  # window title

pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
main_surface = pygame.Surface((DIS_W, DIS_H))  # main_surface where things are rendered


def main():
    # VARIABLES
    # fonts
    value.GAME_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)  # default font, use for info displays

    # location variables
    top_left = (0, 0)  # coordinates for top left of main_surface
    main_menu_size = (DIS_W // 5, DIS_H - 20)  # menu my_surface size
    main_menu_loc = (10, 10)  # from top left corner
    pause_menu_size = (DIS_W // 5 * 2, DIS_H // 3 * 2)
    pause_menu_loc = (DIS_W // 2 - pause_menu_size[0] // 2, DIS_H // 2 - pause_menu_size[1] // 2)
    map_iso_size = (DIS_W // 5 * 3, DIS_H)  # map main_surface my_surface size
    map_iso_loc = (DIS_W // 2 - map_iso_size[0] // 2, 0)  # middle third of screen

    # integer values
    dt = 0  # delta time is milliseconds since last frame
    rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
    fps = 24  # default to 24 fps

    # data structures
    last_frame_keys = pygame.key.get_pressed()
    mouse_pos = (0, 0)  # position of the mouse

    # local flags
    game_running = True

    # set defaults
    value.ISO_OFFSET_X = map_iso_size[0] / 2  # default location
    value.ISO_OFFSET_Y = map_iso_size[1] / 2  # where top place iso map on the map main_surface, y dimension
    value.DEBUG_MODE = True

    # set displays
    main_menu_display = objects.Display('main menu', main_menu_size, main_menu_loc, value.RED, value.BLACK, value.BLACK, main_surface)
    pause_menu_display = objects.Display('', pause_menu_size, pause_menu_loc, value.RED, value.BLACK, value.BLACK, main_surface)

    #load initial values
    load.load_sprites()

    # MAIN GAME LOOP
    while game_running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                game_running = False  # ends main game loop

        # CONTROLS
        # key events
        keys = pygame.key.get_pressed()  # the state of all keys in an array
        if value.CONTEXT_MISSION:
            control.handle_iso_movement(keys, last_frame_keys)
        last_frame_keys = keys  # keep these keys to track changes in next frame

        # mouse
        mouse_pos = pygame.mouse.get_pos()
        if value.CONTEXT_MAIN_MENU:
            control.check_button_collisions()
        elif value.GAME_PAUSE:
            control.check_button_collisions()

        # GAME LOGIC
        # load map if not already

        # RENDER GAME
        # fill screen to wipe away last frame
        main_surface.fill(value.BLACK)  # fills screen with solid black

        # conditionals
        # main menu
        if value.CONTEXT_MAIN_MENU:
            if not value.MAIN_MENU_DRAWN:
                render.draw_main_menu(main_menu_display)
            for button in value.BUTTONS:
                button.draw()
            main_menu_display.render()
        elif value.GAME_PAUSE:
            if not value.PAUSE_MENU_DRAWN:
                render.draw_pause_menu(pause_menu_display)
            for button in value.BUTTONS:
                button.draw()
            pause_menu_display.render()

        # debug_mode overlay
        if value.DEBUG_MODE:
            dt_text = value.GAME_FONT.render('dt=' + str(dt) + 'ms', 1, value.WHITE)  # setup delta time text
            rt_text = value.GAME_FONT.render('rt=' + str(rt) + 'ms', 1, value.WHITE)  # setup raw time text
            mouse_text = value.GAME_FONT.render('mp=' + str(mouse_pos), 1, value.WHITE)  # mouse position
            main_surface.blit(dt_text, top_left)  # add delta time tracker to upper left
            main_surface.blit(rt_text, (0, 25))  # add delta time tracker to upper left
            main_surface.blit(mouse_text, (0, 25 * 2))  # add mouse text

        # put work on the screen
        screen.blit(pygame.transform.scale(main_surface, screen.get_size()), top_left)
        pygame.display.update()  # update main_surface

        # FRAME LOCK / METRICS
        rt = CLOCK.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = CLOCK.tick(fps)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
