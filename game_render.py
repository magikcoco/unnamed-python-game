
## CONTAINS FUNCTIONS FOR RENDERING THINGS IN GAME ##

import pygame
import game_objects as objects
import game_values as value


def draw_main_menu(display):
    top_pad = 50  # the pad from the top of the display, for its border
    buttons = ['PLAY', 'TEST']  # the buttons to put on this menu
    x = display.get_width() // 2 - value.BUTTON_SIZE[0] // 2  # the x coordinate of these buttons
    btn_y = value.BUTTON_SIZE[1] + 20  # the amount of space between buttons
    for i in range(len(buttons)):  # draw the buttons
        y = top_pad + btn_y * i  # incrementing the y
        btn = objects.Button(buttons[i], value.BUTTON_SIZE, value.RED, value.WHITE, display, (x, y))
        btn.draw()
        value.BUTTONS.append(btn)  # add the button to the proper data structure

    # set flags
    value.MAIN_MENU_DRAWN = True


def draw_pause_menu(display):
    top_pad = 30
    buttons = ['MAIN MENU', 'TEST']
    x = display.get_width() // 2 - value.BUTTON_SIZE[0] // 2
    btn_y = value.BUTTON_SIZE[1] + 20
    for i in range(len(buttons)):
        y = top_pad + btn_y * i
        btn = objects.Button(buttons[i], value.BUTTON_SIZE, value.RED, value.WHITE, display, (x, y))
        btn.draw()
        value.BUTTONS.append(btn)

    # set flags
    value.PAUSE_MENU_DRAWN = True


def render_visible_map(display):
    # TODO: determine what sprites to load where
    tile_w = 20 * value.TILE_SIZE_MULT  # base tile size times tile size multiplier, width
    tile_h = 24 * value.TILE_SIZE_MULT  # tile height
    value.SPRITES['default tile'] = pygame.transform.scale(value.SPRITES['default tile'], (tile_w, tile_h))
    iso_x = 10 * value.TILE_SIZE_MULT  # x-axis offset
    iso_y = 5 * value.TILE_SIZE_MULT  # y-axis offset
    iso_z = 13 * value.TILE_SIZE_MULT # z axis to move up or down a level
    for y, row in enumerate(value.MAP_DATA):  # data y axis
        for x, tile in enumerate(row):  # data x axis
            x_pos = value.ISO_OFFSET_X + x * iso_x - y * iso_x
            y_pos = value.ISO_OFFSET_Y + x * iso_y + y * iso_y
            display.draw(value.SPRITES['default tile'], (x_pos, y_pos))  # render the floor
            if tile:
                display.draw(value.SPRITES['default tile'], (x_pos, y_pos - iso_z))  # translate on y-axis upward for z
