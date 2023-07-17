# main file of the game
import pygame

# SETUP PYGAME
pygame.init()

# CONSTANTS
WIN_TITLE = 'untitled game'  # window title

DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)  # default font, use for info displays

WIN_W = 1600  # width of the window
WIN_H = WIN_W//16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W//16 * 9  # 16:9 aspect ratio

BLACK = (0, 0, 0)  # RGB for black
WHITE = (255, 255, 255)  # RGB for white

TOP_LEFT = (0, 0)  # coordinates for top left of a surface

# VARIABLES
clock = pygame.time.Clock()  # used to lock fps in main game loop

running = True  # boolean for main game loop

fps = 24  # default to 24 fps
dt = 0  # delta time is seconds since last frame

# SETUP DISPLAY
pygame.display.set_caption(WIN_TITLE)  # window title
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
display = pygame.Surface((DIS_W, DIS_H))  # display where things are rendered

# MAIN GAME LOOP
while running:
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # ends main game loop

    # fill screen to wipe away last frame
    display.fill(BLACK)  # fills screen with solid black

    # RENDER GAME HERE
    dt_text = DEFAULT_FONT.render('dt='+str(dt)+'ms', 1, WHITE)  # setup delta time text
    display.blit(dt_text, TOP_LEFT)  # add delta time tracker to upper left

    # put work on the screen
    screen.blit(pygame.transform.scale(display, screen.get_size()), TOP_LEFT)  # apply rendered display to window
    pygame.display.update()  # update display

    # lock fps
    dt = clock.tick(fps)  # keeps track of time since last frame in milliseconds

pygame.quit()  # quit pygame or otherwise game will continue after closing