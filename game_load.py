
## CONTAINS FUNCTIONS FOR LOADING THINGS FOR THE GAME  ##

import pygame, os
import game_values as value

pygame.mixer.init()


def load_sounds():
    # load sounds that the game uses for various things
    btn_hover = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'button-hover.ogg'))  # button hover sound

    # data structure for sounds
    value.SOUNDS['button hover'] = btn_hover


def load_sprites():
    length_assigned = False
    # load tiles
    dir_path = os.path.join('assets', 'sprites', 'tiles')
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            files = os.listdir(item_path)
            anim_seq = list()
            for file in files:
                frame = pygame.image.load(os.path.join(item_path, file))
                frame.set_colorkey(value.COLORS['black'])
                anim_seq.append(frame)
            value.SPRITES[item] = anim_seq
            if str(item) == 'highlight':
                value.TILE_HL_ANIM_LEN = len(anim_seq) - 1
            elif not length_assigned:
                value.TILE_ANIM_LEN = len(anim_seq) - 1
                length_assigned = True


def load_map(game_map):
    #file operation
    # TODO: check for and handle errors in accessing this file
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    # read each row into a list of substrings, for each substring convert into a list of ints for each character
    value.MAP_DATA = [[int(c) for c in row] for row in f.read().split('\n')]  # 2D list
    f.close()  # close the file
