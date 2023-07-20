# main file of the game
import pygame, os

# TODO: add a main menu with a start button
# TODO: add a pause button with a quit to main menu button

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
WIN_H = WIN_W // 16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W // 16 * 9  # 16:9 aspect ratio
FPS = 24  # default to 24 fps

TOP_LEFT = (0, 0)  # coordinates for top left of the display
TOP_RIGHT = (DIS_W, 0)  # coordinates for top right of the display

MDIS_SIZE = (DIS_W // 5 * 3, DIS_H)  # map display surface size
MDIS_OFFSET = (DIS_W // 2 - MDIS_SIZE[0] // 2, 0)  # middle third of screen

# VARIABLES
clock = pygame.time.Clock()  # used to lock fps in main game loop

running = True  # boolean for main game loop
debug = True  # boolean for toggling debug information
map_loaded = False  # boolean flag to determine if map has been loaded
context_mission = True  # boolean flag if we should display map information

dt = 0  # delta time is milliseconds since last frame
rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
map_vel = 10  # speed at which the map moves
map_off_x = MDIS_SIZE[0] / 2  # where to place iso map on the map display, x dimension
map_off_y = MDIS_SIZE[1] / 2  # where top place iso map on the map display, y dimension

map_data = [[]]  # global 2D list to hold map data
last_frame_keys = []  # global list to hold the status of keys from the previous frame

# SETUP DISPLAY
pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
display = pygame.Surface((DIS_W, DIS_H))  # display where things are rendered

# render surfaces
visible_map_dis = pygame.Surface(MDIS_SIZE)  # isometric map display


def load_map(game_map):
    # globals
    global map_data

    #file operation
    # TODO: check for and handle errors in accessing this file
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    # read each row into a list of substrings, for each substring convert into a list of ints for each character
    map_data = [[int(c) for c in row] for row in f.read().split('\n')]  # 2D list
    f.close()  # close the file


def render_visible_map():
    iso_x = 10 * TILE_SIZE_MULT  # x-axis offset
    iso_y = 5 * TILE_SIZE_MULT  # y-axis offset
    iso_z = 13 * TILE_SIZE_MULT  # z axis to move up or down a level
    for y, row in enumerate(map_data):  # data y axis
        for x, tile in enumerate(row):  # data x axis
            x_pos = map_off_x + x * iso_x - y * iso_x
            y_pos = map_off_y + x * iso_y + y * iso_y
            visible_map_dis.blit(DEFAULT_TILE, (x_pos, y_pos))  # render the floor
            if tile:
                visible_map_dis.blit(DEFAULT_TILE, (x_pos, y_pos - iso_z))  # translate on y-axis upward for z


def handle_map_movement(keys):
    # globals
    global map_off_y
    global map_off_x
    global map_data

    # lateral movement keys, should be continuous
    if keys[pygame.K_UP]:
        map_off_y -= map_vel
    if keys[pygame.K_DOWN]:
        map_off_y += map_vel
    if keys[pygame.K_LEFT]:
        map_off_x -= map_vel
    if keys[pygame.K_RIGHT]:
        map_off_x += map_vel

    # rotation keys, should not be continuous
    if keys[pygame.K_LCTRL] and not last_frame_keys[pygame.K_LCTRL]:
        map_data = list(zip(*map_data))[::-1]  # counterclockwise
    if keys[pygame.K_RCTRL] and not last_frame_keys[pygame.K_RCTRL]:
        map_data = list(zip(*map_data[::-1]))  # clockwise


def main():
    # declare globals
    global clock
    global running
    global debug
    global map_loaded
    global context_mission
    global dt
    global rt
    global map_vel
    global map_off_x
    global map_off_y
    global map_data
    global last_frame_keys

    # MAIN GAME LOOP
    while running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                running = False  # ends main game loop

        # CONTROLS
        # key events
        keys = pygame.key.get_pressed()  # the state of all keys in an array
        if context_mission:
            handle_map_movement(keys)
        last_frame_keys = keys  # keep these keys to track changes in next frame

        # RENDER GAME
        # fill screen to wipe away last frame
        display.fill(BLACK)  # fills screen with solid black
        if debug and context_mission:  # fill green when debug is on to see surface boundaries
            visible_map_dis.fill(GREEN)
        elif context_mission:  # fill same as main display when no debug info shown
            visible_map_dis.fill(BLACK)

        # display map
        if not map_loaded and context_mission:  # if we need to load a map, and it hasn't been loaded
            load_map('default.txt')  # load map
            map_loaded = True  # switch flag to avoid reloading every time
        if map_loaded and context_mission:  # if the map is loaded, and we need to display it
            render_visible_map()  # render the isometric map

        # debug overlay
        if debug:
            dt_text = DEFAULT_FONT.render('dt=' + str(dt) + 'ms', 1, WHITE)  # setup delta time text
            rt_text = DEFAULT_FONT.render('rt=' + str(rt) + 'ms', 1, WHITE)  # setup raw time text
            display.blit(dt_text, TOP_LEFT)  # add delta time tracker to upper left
            display.blit(rt_text, (0, 25))  # add delta time tracker to upper left

        # add surfaces
        if context_mission:
            display.blit(visible_map_dis, MDIS_OFFSET)  # map

        # put work on the screen
        screen.blit(pygame.transform.scale(display, screen.get_size()), TOP_LEFT)  # apply rendered display to window
        pygame.display.update()  # update display

        # lock fps
        rt = clock.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = clock.tick(FPS)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
