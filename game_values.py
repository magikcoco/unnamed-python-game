
## THIS FILE IS FOR VALUES THAT NEED TO ACCESSED ACROSS PYTHON SCRIPTS ##

GAME_FONT = None
ISO_OFFSET_X = 0  # offset for the isometric map, used to move it around
ISO_OFFSET_Y = 0
TILE_SIZE_MULT = 3  # tile size multiplier to increase how large the sprites are
MAP_DATA = list()  # the data that gets read to form maps
BUTTONS = list()  # the currently available buttons
SPRITES = {}
SOUNDS = {}
CONTEXT_MAIN_MENU = True  # context flags change the state of the game
CONTEXT_DOWNTIME = False
CONTEXT_MEET = False
CONTEXT_LEGWORK = False
CONTEXT_MISSION = False
CONTEXT_ESCAPE = False
GAME_PAUSE = False
DEBUG_MODE = False  # toggles debug mode
ISO_MAP_LOADED = False  # flag if any isometric map is currently loaded
MAIN_MENU_DRAWN = False  # flag if the main menu has been drawn
PAUSE_MENU_DRAWN = False
BUTTON_SIZE = (160, 65)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
