
## CONTAINS FUNCTIONS FOR RENDERING THINGS IN GAME ##

import pygame
import game_objects as objects
import game_values as value


def draw_main_menu(display):
    # button scale
    btn_scale = (display.get_width()//2, int(0.41 * display.get_width()//2))
    #play button
    play_btn_sprite = pygame.transform.scale(value.SPRITES['play button'], btn_scale)
    play_btn_sprite_hl = pygame.transform.scale(value.SPRITES['play button highlight'], btn_scale)
    play_btn_group = (play_btn_sprite, play_btn_sprite_hl)
    btn_x = display.get_width() // 2 - play_btn_sprite.get_width() // 2
    btn_y = 50
    play_btn = objects.Button('play', display, (btn_x, btn_y + 20 * 0), play_btn_group)
    play_btn.draw()

    # append all buttons to play
    value.BUTTONS.append(play_btn)

    # set flags
    value.MAIN_MENU_DRAWN = True


def render_visible_map(display):
    iso_x = 10 * value.TILE_SIZE_MULT  # x-axis offset
    iso_y = 5 * value.TILE_SIZE_MULT  # y-axis offset
    iso_z = 13 * value.TILE_SIZE_MULT  # z axis to move up or down a level
    for y, row in enumerate(value.MAP_DATA):  # data y axis
        for x, tile in enumerate(row):  # data x axis
            # TODO: determine what sprites to load where
            x_pos = value.ISO_OFFSET_X + x * iso_x - y * iso_x
            y_pos = value.ISO_OFFSET_Y + x * iso_y + y * iso_y
            display.draw(value.SPRITES['default tile'], (x_pos, y_pos))  # render the floor
            if tile:
                display.draw(value.SPRITES['default tile'], (x_pos, y_pos - iso_z))  # translate on y-axis upward for z
