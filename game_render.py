
## CONTAINS FUNCTIONS FOR RENDERING THINGS IN GAME ##

import game_objects as objects
import game_values as value


def draw_main_menu(display):
    top_pad = 30

    # play button
    btn_x = display.get_width() // 2 - value.BUTTON_SIZE[0] // 2
    btn_y = 20
    play_btn = objects.Button('play', value.BUTTON_SIZE, value.RED, value.WHITE, display, (btn_x, top_pad + btn_y * 1))
    play_btn.draw()

    # append all buttons to list
    value.BUTTONS.append(play_btn)

    # set flags
    value.MAIN_MENU_DRAWN = True


def draw_pause_menu(display):
    top_pad = 10

    # quit button
    btn_x = display.get_width() // 2 - value.BUTTON_SIZE[0] // 2
    btn_y = 20
    pause_btn = objects.Button('quit', value.BUTTON_SIZE, value.RED, value.WHITE, display, (btn_x, top_pad + btn_y * 1))
    pause_btn.draw()

    # append all buttons to list
    value.BUTTONS.append(pause_btn)

    # set flags
    value.PAUSE_MENU_DRAWN = True


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
