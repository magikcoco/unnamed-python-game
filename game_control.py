
## FUNCTIONS FOR CONTROLLING THE GAME ##

import pygame
import game_values as value


def check_button_collisions():
    for button in value.BUTTONS:
        if button.check_mouse():
            if button.name == 'play':
                value.CONTEXT_MAIN_MENU = False  # not on the main menu anymore
                value.CONTEXT_MISSION = True  # TODO: change the flag when new contexts are made
                value.MAIN_MENU_DRAWN = False  # main menu not drawn anymore
                value.BUTTONS.clear()  # clear the main menu buttons out
            elif button.name == 'quit':
                value.CONTEXT_MAIN_MENU = True
                value.CONTEXT_DOWNTIME = False
                value.CONTEXT_MEET = False
                value.CONTEXT_LEGWORK = False
                value.CONTEXT_MISSION = False
                value.CONTEXT_ESCAPE = False
                value.GAME_PAUSE = False
                value.PAUSE_MENU_DRAWN = False
                value.BUTTONS.clear()


def handle_iso_movement(keys, last_frame_keys):
    map_vel = 10  # speed at which the map moves

    # pause game
    if keys[pygame.K_ESCAPE] and not last_frame_keys[pygame.K_ESCAPE]:
        value.GAME_PAUSE = not value.GAME_PAUSE
        if not value.GAME_PAUSE:
            value.BUTTONS.clear()
            value.PAUSE_MENU_DRAWN = False

    if not value.GAME_PAUSE:
        # lateral movement keys, should be continuous
        if keys[pygame.K_UP]:
            value.ISO_OFFSET_Y -= map_vel
        if keys[pygame.K_DOWN]:
            value.ISO_OFFSET_Y += map_vel
        if keys[pygame.K_LEFT]:
            value.ISO_OFFSET_X -= map_vel
        if keys[pygame.K_RIGHT]:
            value.ISO_OFFSET_X += map_vel

        # rotation keys, should not be continuous
        if keys[pygame.K_LCTRL] and not last_frame_keys[pygame.K_LCTRL]:
            value.MAP_DATA = list(zip(*value.MAP_DATA))[::-1]  # counterclockwise
        if keys[pygame.K_RCTRL] and not last_frame_keys[pygame.K_RCTRL]:
            value.MAP_DATA = list(zip(*value.MAP_DATA[::-1]))  # clockwise
