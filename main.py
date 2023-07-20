# main file of the game
import pygame, os
from functools import reduce

#TODO: add a main menu with a start button
#TODO: add a pause button with a quit to main menu button

# SETUP PYGAME
pygame.init()  # initialize pygame
pygame.key.set_repeat(1, 50)  # set all keys to repeat when held down

# CONSTANTS
BLACK = (0, 0, 0)  # RGB for black
WHITE = (255, 255, 255)  # RGB for white
GREEN = (34, 139, 34)  # forest green

WIN_TITLE = 'untitled game'  # window title

DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)  # default font, use for info displays

TILE_SIZE_MULT = 3  # tile size multiplier to increase how large the tiles are
TILE_W = 20 * TILE_SIZE_MULT  # base tile size times tile size multiplier, width
TILE_H = 24 * TILE_SIZE_MULT  # tile height

DEFAULT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'default.png'))  # default tile sprite
DEFAULT_TILE = pygame.transform.scale(DEFAULT_TILE, (TILE_W, TILE_H))  # scale the tile
DEFAULT_TILE.set_colorkey(BLACK)  # needed for transparent background on sprite

WIN_W = 1600  # width of the window
WIN_H = WIN_W//16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W//16 * 9  # 16:9 aspect ratio
FPS = 24  # default to 24 fps

TOP_LEFT = (0, 0)  # coordinates for top left of the display
TOP_RIGHT = (DIS_W, 0)  # coordinates for top right of the display

MMDIS_SIZE = (300, 300)  # minimap surface size
MMDIS_OFFSET = (DIS_W - MMDIS_SIZE[0] - 10, DIS_H - MMDIS_SIZE[1] - 10)  # top right with 10 pixels padding from sides
MDIS_SIZE = (DIS_W//5 * 3, DIS_H)  # map display surface size
MDIS_OFFSET = (DIS_W//2 - MDIS_SIZE[0]//2, 0)  # middle third of screen

# VARIABLES
clock = pygame.time.Clock()  # used to lock fps in main game loop

running = True  # boolean for main game loop
debug = True  # boolean for toggling debug information
cmap_loaded = False  # boolean flag to determine if map has been loaded
context_map = True  # boolean flag if we should display map information

dt = 0  # delta time is milliseconds since last frame
rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
map_vel = 10  # speed at which the map moves
map_max_x = 1  # maximum x dimension of loaded map, not 0 to avoid possible division error
map_max_y = 1  # maximum y dimension of loaded map, not 0 to avoid possible division error
iso_offset_x = MDIS_SIZE[0]/2 - map_max_x  # where to place iso map on the map display, x dimension
iso_offset_y = MDIS_SIZE[1]/2 - map_max_y  # where top place iso map on the map display, y dimension

map_data = [[]]  # global 2D list to hold map data
last_frame_keys = []  # global list to hold the status of keys from the previous frame

# SETUP DISPLAY
pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
display = pygame.Surface((DIS_W, DIS_H))  # display where things are rendered
minimap_display = pygame.Surface(MMDIS_SIZE)  # minimap display
map_display = pygame.Surface(MDIS_SIZE)  # isometric map display


def load_map(game_map):
    global map_max_x
    global map_max_y
    global map_data
    # we want to load the game_map as a 2D array of integers from the top left to the bottom right
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    #TODO: check for and handle errors in accessing this file
    #
    # read each row into a a list of substrings, for each substring convert into a list of ints for each character
    map_data = [[int(c) for c in row] for row in f.read().split('\n')]
    f.close()  # close the file
    map_max_x = reduce(lambda x, y: max(x, len(y)), map_data, 0)  # performance friendly way to get largest x
    map_max_y = len(map_data)


def render_minimap():
    s_mult = min(MMDIS_SIZE)/map_max_x  # dynamically size the minimap
    for y, row in enumerate(map_data):  # y dimension
        for x, tile in enumerate(row):  # x dimension
            if tile:  # draw a solid rectangle
                pygame.draw.rect(minimap_display, WHITE, pygame.Rect(x * s_mult, y * s_mult, s_mult, s_mult))  # wall tile
            else:  # draw a hollow rectangle
                pygame.draw.rect(minimap_display, WHITE, pygame.Rect(x * s_mult, y * s_mult, s_mult, s_mult), 1)  # floor tile


def render_isometric():
    iso_x = 10 * TILE_SIZE_MULT  # x axis offset
    iso_y = 5 * TILE_SIZE_MULT  # y axis offset
    iso_z = 13 * TILE_SIZE_MULT  # z axis to move up or down a level
    for y, row in enumerate(map_data):  # data y axis
        for x, tile in enumerate(row):  # data x axis
            map_display.blit(DEFAULT_TILE,  # render image
                             (iso_offset_x + x * iso_x - y * iso_x,  # x axis
                              iso_offset_y + x * iso_y + y * iso_y))  # y axis
            if tile:
                map_display.blit(DEFAULT_TILE,  # render image
                                 (iso_offset_x + x * iso_x - y * iso_x,  # x axis
                                  iso_offset_y + x * iso_y + y * iso_y - iso_z))  # y axis raised for fake z


def handle_iso_movement(keys):
    global iso_offset_y
    global iso_offset_x
    global map_data

    if keys[pygame.K_UP]:
        iso_offset_y -= map_vel
    if keys[pygame.K_DOWN]:
        iso_offset_y += map_vel
    if keys[pygame.K_LEFT]:
        iso_offset_x -= map_vel
    if keys[pygame.K_RIGHT]:
        iso_offset_x += map_vel

    if keys[pygame.K_LCTRL] and not last_frame_keys[pygame.K_LCTRL]:
        map_data = list(zip(*map_data))[::-1]
    if keys[pygame.K_RCTRL] and not last_frame_keys[pygame.K_RCTRL]:
        map_data = list(zip(*map_data[::-1]))


def main():
    # declare globals
    global clock
    global running
    global debug
    global cmap_loaded
    global context_map
    global dt
    global rt
    global map_vel
    global iso_offset_x
    global iso_offset_y
    global map_data
    global last_frame_keys

    # MAIN GAME LOOP
    while running:
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                running = False  # ends main game loop

        # key events
        keys = pygame.key.get_pressed()  # the state of all keys in an array
        if context_map:  # controls based on context
            handle_iso_movement(keys)
        last_frame_keys = keys  # keep these keys to track changes in next frame

        # fill screen to wipe away last frame
        display.fill(BLACK)  # fills screen with solid black
        if debug and context_map:  # fill green when debug is on to see surface boundaries
            minimap_display.fill(GREEN)
            map_display.fill(GREEN)
        elif context_map:  # fill same as main display when no debug info shown
            minimap_display.fill(BLACK)
            map_display.fill(BLACK)

        # RENDER GAME HERE
        # display map
        if not cmap_loaded and context_map:  # if we need to load a map and it hasnt been loaded
            load_map('default.txt')  # load map
            cmap_loaded = True  # switch flag to avoid reloading every time
        if cmap_loaded and context_map:  # if the map is loaded and we need to display it
            render_minimap()  # render the minimap
            render_isometric()  # render the isometric map

        # debug overlay
        if debug:
            dt_text = DEFAULT_FONT.render('dt='+str(dt)+'ms', 1, WHITE)  # setup delta time text
            rt_text = DEFAULT_FONT.render('rt='+str(rt)+'ms', 1, WHITE)  # setup raw time text
            display.blit(dt_text, TOP_LEFT)  # add delta time tracker to upper left
            display.blit(rt_text, (0, 25))  # add delta time tracker to upper left

        # add surfaces
        if context_map:
            display.blit(map_display, MDIS_OFFSET)  # map
            display.blit(minimap_display, MMDIS_OFFSET)  # minimap

        # put work on the screen
        screen.blit(pygame.transform.scale(display, screen.get_size()), TOP_LEFT)  # apply rendered display to window
        pygame.display.update()  # update display

        # lock fps
        rt = clock.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = clock.tick(FPS)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
