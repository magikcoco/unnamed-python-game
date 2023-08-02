
## THIS FILE IS FOR VALUES THAT NEED TO ACCESSED ACROSS PYTHON SCRIPTS ##

BUTTON_SIZE = (160, 65)
MAP_DATA = list()  # the data that gets read to form maps
BUTTONS = list()  # the currently available buttons
SPRITES = {}
SOUNDS = {}
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'dis_blue': (0, 134, 223)
}
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
CUR_ISO_MAP = None
GAME_FONT = None
