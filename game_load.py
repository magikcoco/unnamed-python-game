
## CONTAINS FUNCTIONS FOR LOADING THINGS FOR THE GAME  ##

import pygame, os
import game_values as value


def load_sprites():
    tile_w = 20 * value.TILE_SIZE_MULT  # base tile size times tile size multiplier, width
    tile_h = 24 * value.TILE_SIZE_MULT  # tile height

    default_tile = pygame.image.load(os.path.join('assets', 'tiles', 'default.png'))  # default tile sprite
    default_tile = pygame.transform.scale(default_tile, (tile_w, tile_h))  # scale the tile
    default_tile.set_colorkey(value.BLACK)  # needed for transparent background on sprite

    value.SPRITES['default tile'] = default_tile

    play_btn = pygame.image.load(os.path.join('assets', 'tiles', 'play_btn.png'))
    play_btn_hl = pygame.image.load(os.path.join('assets', 'tiles', 'play_btn_highlight.png'))

    value.SPRITES['play button'] = play_btn
    value.SPRITES['play button highlight'] = play_btn_hl


def load_map(game_map):
    #file operation
    # TODO: check for and handle errors in accessing this file
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    # read each row into a list of substrings, for each substring convert into a list of ints for each character
    value.MAP_DATA = [[int(c) for c in row] for row in f.read().split('\n')]  # 2D list
    f.close()  # close the file
