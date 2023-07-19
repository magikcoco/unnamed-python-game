# main file of the game
import pygame, os
from functools import reduce

# SETUP PYGAME
pygame.init()

# CONSTANTS
BLACK = (0, 0, 0)  # RGB for black
WHITE = (255, 255, 255)  # RGB for white

WIN_TITLE = 'untitled game'  # window title

DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)  # default font, use for info displays

TILE_SIZE_MULT = 3
TILE_W = 20 * TILE_SIZE_MULT
TILE_H = 24 * TILE_SIZE_MULT

DEFAULT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'default.png'))
DEFAULT_TILE = pygame.transform.scale(DEFAULT_TILE, (TILE_W, TILE_H))
DEFAULT_TILE.set_colorkey(BLACK)

WIN_W = 1600  # width of the window
WIN_H = WIN_W//16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W//16 * 9  # 16:9 aspect ratio
FPS = 24  # default to 24 fps

TOP_LEFT = (0, 0)  # coordinates for top left of the display
TOP_RIGHT = (DIS_W, 0)  # coordinates for top right of the display

# VARIABLES
clock = pygame.time.Clock()  # used to lock fps in main game loop

running = True  # boolean for main game loop

dt = 0  # delta time is seconds since last frame

# SETUP DISPLAY
pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
display = pygame.Surface((DIS_W, DIS_H))  # display where things are rendered


def load_map(game_map):
    # we want to load the game_map as a 2D array of integers from the top left to the bottom right
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    #TODO: check for and handle errors in accessing this file
    #
    # read each row into a a list of substrings, for each substring convert into a list of ints for each character
    map_data = [[int(c) for c in row] for row in f.read().split('\n')]
    f.close()  # close the file
    return map_data  # return the 2D list


def render_minimap(map_data):
    max_x = reduce(lambda x, y: max(x, len(y)), map_data, 0)  # performance friendly way to get largest x
    offset_x = DIS_W - max_x * 50  # X dimension offset from far left of display
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile:
                pygame.draw.rect(display, WHITE, pygame.Rect(offset_x + x * 50, y * 50, 50, 50))
            else:
                pygame.draw.rect(display, WHITE, pygame.Rect(offset_x + x * 50, y * 50, 50, 50), 1)


def render_isometric(map_data):
    iso_x = 10 * TILE_SIZE_MULT
    iso_y = 5 * TILE_SIZE_MULT
    iso_z = 13 * TILE_SIZE_MULT
    max_x = reduce(lambda x, y: max(x, len(y)), map_data, 0)  # performance friendly way to get largest x
    offset_x = DIS_W/2 - max_x * 10  # X dimension offset from far left of display
    max_y = len(map_data)
    offset_y = DIS_H/2 - max_y * 10
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            display.blit(DEFAULT_TILE, (offset_x + x * iso_x - y * iso_x, offset_y + x * iso_y + y * iso_y))  # render floor
            if tile:
                display.blit(DEFAULT_TILE, (offset_x + x * iso_x - y * iso_x, offset_y + x * iso_y + y * iso_y - iso_z))  # render 2nd level


def main():
    # declare globals
    global clock
    global running
    global dt

    # MAIN GAME LOOP
    while running:
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # ends main game loop

        # fill screen to wipe away last frame
        display.fill(BLACK)  # fills screen with solid black

        # RENDER GAME HERE
        # display map
        map_data = load_map('default.txt')
        render_minimap(map_data)
        render_isometric(map_data)

        # debug overlay
        dt_text = DEFAULT_FONT.render('dt='+str(dt)+'ms', 1, WHITE)  # setup delta time text
        display.blit(dt_text, TOP_LEFT)  # add delta time tracker to upper left

        # put work on the screen
        screen.blit(pygame.transform.scale(display, screen.get_size()), TOP_LEFT)  # apply rendered display to window
        pygame.display.update()  # update display

        # lock fps
        dt = clock.tick(FPS)  # keeps track of time since last frame in milliseconds

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
