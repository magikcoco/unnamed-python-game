
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
        btn = objects.Button(buttons[i], value.BUTTON_SIZE, value.COLORS['dis_blue'], value.COLORS['white'], display, (x, y))
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
        btn = objects.Button(buttons[i], value.BUTTON_SIZE, value.COLORS['dis_blue'], value.COLORS['white'], display, (x, y))
        btn.draw()
        value.BUTTONS.append(btn)

    # set flags
    value.PAUSE_MENU_DRAWN = True
