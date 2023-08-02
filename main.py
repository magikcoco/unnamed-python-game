
## MAIN GAME FILE ##

import pygame, os
from pygame.locals import *
import game_objects as objects
import game_load as load
import game_render as render
import game_control as control
import game_values as value

# TODO: add highlights to tops of tiles on hover
# TODO: expand default map in size
# TODO: decide what numbers that aren't 0 or 1 mean in a map file
# TODO: make some actual tiles
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
    # location variables
    # main menu
    main_menu_size = (DIS_W // 5, DIS_H - 20)  # size
    main_menu_loc = (10, 10)  # location on main_surface
    # pause menu
    pause_menu_size = (DIS_W // 5 * 2, DIS_H // 3 * 2)  # size
    pause_menu_loc = (DIS_W // 2 - pause_menu_size[0] // 2, DIS_H // 2 - pause_menu_size[1] // 2)  # location
    # mission map
    map_iso_size = (DIS_W // 5 * 3, DIS_H - 20)  # size
    map_iso_loc = (DIS_W // 2 - map_iso_size[0] // 2, 10)  # location

    # integer values
    dt = 0  # delta time is milliseconds since last frame
    rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
    fps = 24  # frames per second the main game is locked to

    # local flags
    game_running = True  # for the main game loop

    # set displays
    main_menu_display = objects.Display('Main Menu', main_menu_size, main_menu_loc, value.COLORS['dis_blue'], value.COLORS['black'], value.COLORS['black'], main_surface)
    pause_menu_display = objects.Display('', pause_menu_size, pause_menu_loc, value.COLORS['dis_blue'], value.COLORS['black'], value.COLORS['black'], main_surface)
    mission_display = objects.Display('Mission', map_iso_size, map_iso_loc, value.COLORS['dis_blue'], value.COLORS['black'], value.COLORS['black'], main_surface)

    # load initial values
    value.GAME_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'AtlantisInternational-jen0.ttf'), 30)
    load.load_sprites()
    load.load_sounds()
    last_frame_keys = pygame.key.get_pressed()

    # MAIN GAME LOOP
    while game_running:
        m_wheel = 0

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                game_running = False  # ends main game loop
            if event.type == pygame.KEYUP:
                if event.key == K_F1:
                    value.DEBUG_MODE = not value.DEBUG_MODE  # toggle debug mode
            if event.type == pygame.MOUSEWHEEL:
                m_wheel = event.y

        # CONTROLS
        # key events
        keys = pygame.key.get_pressed()  # the state of all keys in an array
        if value.CONTEXT_MISSION:
            control.handle_iso_movement(keys, last_frame_keys)
        last_frame_keys = keys  # keep these keys to track changes in next frame

        # mouse
        if value.CONTEXT_MAIN_MENU:
            control.check_button_collisions()
        elif value.GAME_PAUSE:
            control.check_button_collisions()
        elif value.CONTEXT_MISSION:
            control.handle_iso_zoom(m_wheel)

        # GAME LOGIC

        # RENDER GAME
        # fill screen to wipe away last frame
        main_surface.fill(value.COLORS['black'])  # fills screen with solid black

        # conditionals
        # main menu
        if value.CONTEXT_MAIN_MENU:
            if not value.MAIN_MENU_DRAWN:
                render.draw_main_menu(main_menu_display)
            for button in value.BUTTONS:
                button.draw()
            main_menu_display.render()
        # game pause
        elif value.GAME_PAUSE:  # pause menu should draw instead of anything else
            if not value.PAUSE_MENU_DRAWN:
                render.draw_pause_menu(pause_menu_display)
            for button in value.BUTTONS:
                button.draw()
            pause_menu_display.render()
        elif value.CONTEXT_MISSION:
            if not value.ISO_MAP_LOADED:
                load.load_map('default.txt')
                value.CUR_ISO_MAP = objects.Isomap(value.MAP_DATA, mission_display)
                value.ISO_MAP_LOADED = True  # switch flag
            if value.ISO_MAP_LOADED:
                value.CUR_ISO_MAP.update_tiles()
                value.CUR_ISO_MAP.draw()
            mission_display.render()

        # debug_mode overlay
        if value.DEBUG_MODE:  # debug stuff draws on top of anything else being rendered
            dt_text = value.GAME_FONT.render('dt=' + str(dt) + 'ms', 1, value.COLORS['white'])  # setup delta time text
            rt_text = value.GAME_FONT.render('rt=' + str(rt) + 'ms', 1, value.COLORS['white'])  # setup raw time text
            mouse_text = value.GAME_FONT.render('mp=' + str(pygame.mouse.get_pos()), 1, value.COLORS['white'])  # mouse position
            main_surface.blit(dt_text, (0, 0))  # add delta time tracker to upper left
            main_surface.blit(rt_text, (0, 25))  # add delta time tracker to upper left
            main_surface.blit(mouse_text, (0, 25 * 2))  # add mouse text

        # put work on the screen
        screen.blit(pygame.transform.scale(main_surface, screen.get_size()), (0, 0))  # put the display onto the screen
        pygame.display.update()  # update main_surface

        # FRAME LOCK / METRICS
        rt = CLOCK.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = CLOCK.tick(fps)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
