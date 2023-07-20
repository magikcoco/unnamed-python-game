# main file of the game
import pygame, os

# TODO: add a pause button with a quit to main menu button
# TODO: add hover highlights to map
# TODO: add movable character to map
# TODO: add vision to character
# TODO: change tiles out of vision to greyscale

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

#tiles
DEFAULT_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'default.png'))  # default tile sprite
DEFAULT_TILE = pygame.transform.scale(DEFAULT_TILE, (TILE_W, TILE_H))  # scale the tile
DEFAULT_TILE.set_colorkey(BLACK)  # needed for transparent background on sprite
#buttons
START_BTN = pygame.image.load(os.path.join('assets', 'tiles', 'start_btn.png'))
START_BTN_HL = pygame.image.load(os.path.join('assets', 'tiles', 'start_btn_highlight.png'))

WIN_W = 1600  # width of the window
WIN_H = WIN_W // 16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W // 16 * 9  # 16:9 aspect ratio
FPS = 24  # default to 24 fps

TOP_LEFT = (0, 0)  # coordinates for top left of the display
TOP_RIGHT = (DIS_W, 0)  # coordinates for top right of the display
MENU_DIS_SIZE = (DIS_W // 5, DIS_H)  # menu surface size
MENU_DIS_OFFSET = (0, 0)  # from top left corner
MAP_DIS_SIZE = (DIS_W // 5 * 3, DIS_H)  # map display surface size
MAP_DIS_OFFSET = (DIS_W // 2 - MAP_DIS_SIZE[0] // 2, 0)  # middle third of screen

# VARIABLES
clock = pygame.time.Clock()  # used to lock fps in main game loop

running = True  # boolean for main game loop
debug = True  # boolean for toggling debug information
map_loaded = False  # boolean flag to determine if map has been loaded
main_menu_drawn = False  # flag to see if the main menu has been drawn
context_main_menu = True  # main menu flag
context_mission = False  # boolean flag if we should display map information

dt = 0  # delta time is milliseconds since last frame
rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
map_vel = 10  # speed at which the map moves
map_off_x = MAP_DIS_SIZE[0] / 2  # where to place iso map on the map display, x dimension
map_off_y = MAP_DIS_SIZE[1] / 2  # where top place iso map on the map display, y dimension

map_data = [[]]  # global 2D list to hold map data
last_frame_keys = []  # global list to hold the status of keys from the previous frame
main_menu_buttons = []  # list of main menu buttons from top to bottom

mouse_pos = (0, 0)  # position of the mouse

# SETUP DISPLAY
pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
display = pygame.Surface((DIS_W, DIS_H))  # display where things are rendered

# render surfaces
main_menu_dis = pygame.Surface(MENU_DIS_SIZE)  # main menu
visible_map_dis = pygame.Surface(MAP_DIS_SIZE)  # isometric map display
main_menu_dis.set_colorkey(BLACK)  # set a transparent color that isn't used by sprites
visible_map_dis.set_colorkey(BLACK)


class Button:
    def __init__(self, surface, x, y, image_tuple, button_id):
        self.display_image = image_tuple[0]
        self.other_image = image_tuple[1]
        self.surface = surface
        self.id = button_id
        self.rect = self.display_image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.highlight = False

    def draw(self):
        self.surface.blit(self.display_image, (self.rect.x, self.rect.y))

    def check_mouse(self):
        action = False
        if self.rect.collidepoint(mouse_pos):
            if not self.highlight:
                temp = self.display_image
                self.display_image = self.other_image
                self.other_image = temp
                self.highlight = True
                self.draw()
            if pygame.mouse.get_pressed()[0] and not self.clicked:  # left click
                action = True
                self.clicked = True
        elif self.highlight:
            temp = self.display_image
            self.display_image = self.other_image
            self.other_image = temp
            self.highlight = False
            self.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action


def draw_main_menu():
    global main_menu_drawn
    main_menu_dis.fill(BLACK)
    btn_scale = (main_menu_dis.get_width()//2, int(0.41 * main_menu_dis.get_width()//2))
    btn_x = main_menu_dis.get_width()//2
    btn_y = 20
    start_btn_graphic = (pygame.transform.scale(START_BTN, btn_scale), pygame.transform.scale(START_BTN_HL, btn_scale))
    start_btn = Button(main_menu_dis, btn_x, btn_y * 1, start_btn_graphic, 'start')
    start_btn.draw()
    main_menu_drawn = True
    return [start_btn]


def check_main_menu_collisions():
    global context_main_menu
    global context_mission
    global main_menu_drawn

    for button in main_menu_buttons:
        if button.check_mouse():
            if button.id == 'start':
                context_main_menu = False
                context_mission = True
                main_menu_drawn = False


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
    global main_menu_buttons
    global mouse_pos

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

        # mouse
        mouse_pos = pygame.mouse.get_pos()
        if context_main_menu:
            check_main_menu_collisions()

        # RENDER GAME
        # fill screen to wipe away last frame
        display.fill(BLACK)  # fills screen with solid black
        if debug:
            if context_mission:  # fill green when debug is on to see surface boundaries
                visible_map_dis.fill(GREEN)
        else:
            if context_mission:  # fill same as main display when no debug info shown
                visible_map_dis.fill(BLACK)

        # display main menu
        if context_main_menu and not main_menu_drawn:
            main_menu_buttons = draw_main_menu()

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
        if context_main_menu:
            display.blit(main_menu_dis, MENU_DIS_OFFSET)  # main menu
        if context_mission:
            display.blit(visible_map_dis, MAP_DIS_OFFSET)  # map

        # put work on the screen
        screen.blit(pygame.transform.scale(display, screen.get_size()), TOP_LEFT)  # apply rendered display to window
        pygame.display.update()  # update display

        # lock fps
        rt = clock.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = clock.tick(FPS)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
