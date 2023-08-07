
## MAIN GAME FILE ##

import pygame, os
from pygame.locals import *

## Vague list of tasks to accomplish  ##
# TODO: simplify existing code
# TODO: switch to using image manipulation to build each frame in memory, cut down calls to GPU as much as possible
# TODO: logs, ability to save and export game state to file, ability to load game state from a file
# TODO: multithreading, thread for game logic, thread for rendering, thread for outputting (logs, saves, etc)
# TODO: settings menu with ability to change to fullscreen, support changing resolution
# TODO: add downtime, meetup, legwork, getaway states to the game properly
# TODO: make additional tile types
# TODO: increase complexity of map file
# TODO: update default map to use new tile types
# TODO: add movable character to map
# TODO: add vision to character
# TODO: change sprites out of vision to greyscale

# SETUP PYGAME
pygame.init()  # initialize pygame
pygame.mixer.init()  # mixer for sounds

# VARIABLES
fck_scope = {  # all the variables defined in a dictionary as key: variable name -> value: variable value
    'button size default': (160, 65),  # the default size of a button
    'buttons': [],  # a 1D list of all buttons currently active
    'colors': {  # dictionary of preset colors
        'black': (0, 0, 0),  # basic black
        'white': (255, 255, 255),  # basic white
        'dis_blue': (0, 134, 223)  # blue used for displays
    },
    'current map': None,  # the current map loaded in the game
    'current map data': [],  # a 2D list of the current map data
    'debug mode': False,  # flag for whether to display debug information
    'default font': None,  # the default font to use for text in the game
    'iso map loaded': False,  # flag for loading isometric map
    'main menu drawn': False,  # flag for drawing main menu
    'pause menu drawn': False,  # flag for drawing pause menu
    'sounds': {  # a dictionary of sounds used for the game, simple name -> sound file
        'default': None  # string key -> sound loaded from pygame
    },
    'sprites': {  # a dictionary of sprites used for the game
        'default': []  # sprites store frames individually in a list
    },
    'states': {  # dictionary of current game states, controls the game, only one should be true at a time
        'main menu': True,  # start at the main menu
        'downtime': False,
        'meetup': False,
        'legwork': False,
        'mission': False,
        'getaway': False,
        'pause menu': False
    },
    'tile anim len': 0,  # the number of frames in a tile animation
    'tile hl len': 0  # the number of frames in a tile highlight animation
}


# DEFINE FUNCTIONS
# loads all sounds into a dictionary
def load_sounds():
    # load sounds that the game uses for various things
    btn_hover = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'button-hover.ogg'))  # button hover sound

    # data structure for sounds
    fck_scope['sounds']['button hover'] = btn_hover


# loads all sprites into a dictionary
def load_sprites():  # TODO: one for loop to rule them all, unified load assets function
    length_assigned = False  # flag so we don't keep assigning length over and over
    # load tiles
    dir_path = os.path.join('assets', 'sprites', 'tiles')  # path of directory
    for item in os.listdir(dir_path):  # iterate over all items
        item_path = os.path.join(dir_path, item)  # path of *this* item
        if os.path.isdir(item_path):  # ignore unless it's a subdirectory
            files = os.listdir(item_path)  # list of all files in that subdirectory
            anim_seq = list()  # list of all frames
            for file in files:  # load each file in that directory as a frame
                frame = pygame.image.load(os.path.join(item_path, file))  # TODO: check file type first
                frame.set_colorkey(fck_scope['colors']['black'])  # set color key for invisible background
                anim_seq.append(frame)  # pygame Surface goes into the animation sequence list
            fck_scope['sprites'][item] = anim_seq  # save as subdirectory name: list(frames)
            if str(item) == 'highlight':  # tile highlight (appears on mouse hover)
                fck_scope['tile hl len'] = len(anim_seq) - 1  # save length of this animation
            elif not length_assigned:  # otherwise assign normal tile animation
                fck_scope['tile anim len'] = len(anim_seq) - 1  # save length
                length_assigned = True  # switch flag


# loads a given map into a 2d array
def load_map(game_map):
    #file operation
    # TODO: check for and handle errors in accessing this file
    f = open(os.path.join('assets', 'maps', game_map))  # open the map file
    # read each row into a list of substrings, for each substring convert into a list of ints for each character
    fck_scope['current map data'] = [[int(c) for c in row] for row in f.read().split('\n')]  # 2D list
    f.close()  # close the file


def draw_menu(button_list, display):
    top_pad = 50
    x = display.get_width() // 2 - fck_scope['button size default'][0] // 2  # the x coordinate of these buttons
    btn_y = fck_scope['button size default'][1] + 20
    for i in range(len(button_list)):
        y = top_pad + btn_y * i
        btn = Button(button_list[i], fck_scope['button size default'], fck_scope['colors']['dis_blue'], fck_scope['colors']['white'], display, (x, y))
        fck_scope['buttons'].append(btn)  # add the button to the proper data structure

    fck_scope['main menu drawn'] = True


# checks if any active buttons have been clicked and performs an action if they have been
def check_button_collisions():
    # button actions
    # TODO: state dependent button names
    # TODO: function for changing state?
    for button in fck_scope['buttons']:  # TODO: functions for each button
        if button.check_mouse():  # what each button does
            if button.name == 'PLAY':  # main menu play button, starts the game without loading any save
                fck_scope['states']['main menu'] = False  # not on the main menu anymore
                fck_scope['states']['mission'] = True  # TODO: change the flag when new contexts are made
                fck_scope['main menu drawn'] = False  # main menu not drawn anymore
                fck_scope['buttons'].clear()  # clear the main menu buttons out
            elif button.name == 'MAIN MENU':  # pause menu main menu button, quits to main menu
                fck_scope['states']['main menu'] = True
                fck_scope['states']['downtime'] = False
                fck_scope['states']['meetup'] = False
                fck_scope['states']['legwork'] = False
                fck_scope['states']['mission'] = False
                fck_scope['states']['getaway'] = False
                fck_scope['states']['pause menu'] = False
                fck_scope['main menu drawn'] = False
                fck_scope['buttons'].clear()


# scale the isometric map in mission context within certain bounds
def handle_iso_zoom(m_wheel):  # m_wheel is the value given by pygame, negative or positive, based on direction/speed
    # TODO: smooth scrolling
    scalar = fck_scope['current map'].scale + m_wheel   # get the current scale of the map and add m_wheel
    if (scalar <= 9) and (scalar > 1):  # if the result is within correct bounds then change the scale
        fck_scope['current map'].scale_map(scalar)


# move the isometric map
def handle_iso_movement(keys, last_frame_keys):
    map_vel = 10  # speed at which the map moves

    # pause game, should not be continuous
    if keys[pygame.K_ESCAPE] and not last_frame_keys[pygame.K_ESCAPE]:
        fck_scope['states']['pause menu'] = not fck_scope['states']['pause menu']  # (un)pause the game (context change method?)
        if not fck_scope['states']['pause menu']:  # if we just unpaused the game
            fck_scope['buttons'].clear()  # clear buttons
            fck_scope['pause menu drawn'] = False  # switch flag

    if not fck_scope['states']['pause menu']:  # dont allow in pause context
        # lateral movement keys, should be continuous
        if keys[pygame.K_UP]:  # map up
            fck_scope['current map'].offset_y -= map_vel
        if keys[pygame.K_DOWN]:  # map down
            fck_scope['current map'].offset_y += map_vel
        if keys[pygame.K_LEFT]:  # map left
            fck_scope['current map'].offset_x -= map_vel
        if keys[pygame.K_RIGHT]:  # map right
            fck_scope['current map'].offset_x += map_vel

        # rotation keys, should not be continuous
        if keys[pygame.K_LCTRL] and not last_frame_keys[pygame.K_LCTRL]:
            fck_scope['current map'].turn_counterclockwise()  # TODO: Object or function job here?
        if keys[pygame.K_RCTRL] and not last_frame_keys[pygame.K_RCTRL]:
            fck_scope['current map'].turn_clockwise()


# DEFINE OBJECTS
class Display:  # a display for components on the screen
    def __init__(self, name, s_size, location, border_color, fill_color, text_color, main_surface):  # TODO: fix shadow
        # passed values
        self.name = name.strip()  # the name of this display
        self.my_surface = pygame.Surface(s_size)  # the surface within the display
        self.location = location  # the location of the display relative to the main surface
        self.border_color = border_color  # the border color of this display
        self.fill_color = fill_color  # the fill color for the background of this display
        self.text_color = text_color  # the color with which to draw text
        self.main_surface = main_surface  # the surface to draw the display onto

        # initial / calculated values
        self.render_queue = list()  # the list of things to draw when this display is rendered
        if self.name == '':  # blank name gets no title bar
            self.border_top = pygame.Rect((0, 0), (s_size[0], 10))  # the borders of this display
        else:
            self.border_top = pygame.Rect((0, 0), (s_size[0], 30))  # the borders of this display
        self.border_left = pygame.Rect((0, 0), (10, s_size[1]))  # left part of the border
        self.border_right = pygame.Rect((s_size[0] - 10, 0), (10, s_size[1]))  # right border
        self.border_bottom = pygame.Rect((0, s_size[1] - 10), (s_size[0], 10))  # bottom border

    def render(self):
        # renders this display and everything contained within
        self.my_surface.fill(self.fill_color)  # wipe away previous frame
        for thing, location in self.render_queue:  # draw everything in queue
            self.my_surface.blit(thing, location)
        self.render_queue.clear()  # clear the queue
        # draw a border around the display, overlaps and covers anything rendered in the display
        pygame.draw.rect(self.my_surface, self.border_color, self.border_bottom)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_right)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_left)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_top)
        if not self.name == '':  # render a name if its not blank
            title = fck_scope['default font'].render(self.name, 1, self.text_color)
            text_width, text_height = fck_scope['default font'].size(self.name)
            self.my_surface.blit(title, (self.border_top.centerx - text_width // 2, 0))
        self.main_surface.blit(self.my_surface, self.location)  # blit the display onto the main surface

    def draw(self, thing, location):
        # add something to the render queue
        self.render_queue.append((thing, location))

    def move_to(self, x, y):
        # move this display to the new given coordinates
        self.location[0] = x
        self.location[1] = y

    def get_fill(self):
        # get the color used to fill this display
        return self.fill_color

    def get_relative_mouse_pos(self):
        # get the mouse position relative to this display, useful for mouse collisions
        m_pos = pygame.mouse.get_pos()
        return m_pos[0] - self.location[0], m_pos[1] - self.location[1]

    def get_width(self):
        # get the width of this display (includes borders)
        return self.my_surface.get_width()

    def get_height(self):
        # get the height of this display (includes borders)
        return self.my_surface.get_height()


class Button:  # button for pressing and making things happen
    def __init__(self, name, s_size, color, color_hl, display, location):
        # passed variables
        self.name = name  # the name of this button, used for executing code and display
        self.my_surface = pygame.Surface(s_size)  # the surface of this button
        self.color = color  # the color of this button
        self.color_hl = color_hl  # the color this button changes to when its highlighted
        self.display = display  # the display this button is inside of
        self.rect = self.my_surface.get_rect()  # the rectangle of this button, used for positioning
        self.rect.topleft = location  # the actual position within the display where this button is placed

        # initial / calculated values
        self.clicked = False  # flag for if this button has been clicked
        self.highlight = False  # flag for if this button is currently highlighted
        self.to = 0  # top offset for highlight line
        self.bo = self.rect.size[0]  # bottom offset for highlight line
        self.lo = self.rect.size[1]  # left offset for highlight line
        self.ro = 0  # right offset for highlight line
        self.top_go = True  # flag for if the highlight line should display on the top
        self.bot_go = True  # on the bottom
        self.left_go = False  # on the left
        self.right_go = False  # or on the right
        self.hover_sound = fck_scope['sounds']['button hover']  # the sound this button makes when hovered over

    def draw(self):
        # draws this button onto it's display
        s = self.my_surface  # abbreviation for self.my_surface, makes things look a little neater
        s.fill(self.display.get_fill())  # wipe away last frame
        x = self.rect.size[0]  # the maximum x value
        y = self.rect.size[1]  # the maximum y value
        off_x, off_y = fck_scope['default font'].size(self.name)  # the offsets for the text in the button
        hl_vel = 10  # how fast the line moves
        t = 2  # line thickness
        l = 40  # length of animated line on highlight
        if not self.highlight:  # if the button is not currently highlighted
            c = self.color  # abbreviation for self.color for neater expressions
            pygame.draw.line(s, c, (x - t, 0), (x - t, y), t)  # right
            pygame.draw.line(s, c, (0, 0), (0, y), t)  # left
            pygame.draw.line(s, c, (0, y - t), (x, y - t), t)  # bot
            pygame.draw.line(s, c, (0, 0), (x, 0), t)  # top
            btn_text = fck_scope['default font'].render(self.name, 1, self.color)  # render the button text
        else:  # if the button is currently highlighted
            c = self.color_hl  # abbr. for self.color
            # animate the border, two lines running along the border of the button
            # right line animates bottom to top
            if self.right_go:  # check flag for if this line should be rendered
                ry = y - self.ro + l  # the maximum y, less the offset, plus the length of the line
                rl = max(ry - l, 0)  # the max of ry less the length, or 0
                pygame.draw.line(s, c, (x - t, rl), (x - t, ry), t)  # draw the line on the right border
                if (y - self.ro) < (0 - l // 2):  # if line is halfway off the surface, tell top line to go
                    self.top_go = True
                if (y - self.ro) < (0 - l):  # if line is all the way off the surface, stop drawing
                    self.ro = 0  # reset the offset
                    self.right_go = False
                self.ro += hl_vel  # increment offset so the line moves from bottom to top
            # left line animates top to bottom
            if self.left_go:  # check flag
                ly = y - self.lo  # the difference between the max y coordinate and the offset
                ll = max(ly - l, 0)  # the largest of either 0 or ly less the length of the line
                pygame.draw.line(s, c, (0, ll), (0, ly), t)  # draw the line on the left border
                if (y - self.lo) > (self.rect.size[1] + l // 2):  # if the line is half off the surface, tell bot to go
                    self.bot_go = True
                if (y - self.lo) > (self.rect.size[1] + l):  # stop drawing once all the way off the surface
                    self.lo = self.rect.size[1]  # reset the offset
                    self.left_go = False
                self.lo -= hl_vel  # decrement the offset so the line moves from top to bottom
            # bottom line animates ----> left to right
            if self.bot_go:  # check flag
                bx = x - self.bo  # the difference of the maximum x coordinate and the offset
                bl = max(bx - l, 0)  # the largest of bx less the length of the line or 0
                pygame.draw.line(s, c, (bl, y - t), (bx, y - t), t)  # draw the line on the bottom border
                if (x - self.bo) > (self.rect.size[0] + l // 2):  # if the line is half of the surface tell right to go
                    self.right_go = True
                if (x - self.bo) > (self.rect.size[0] + l):  # stop drawing once off the surface
                    self.bo = self.rect.size[0]  # reset offset
                    self.bot_go = False
                self.bo -= hl_vel  # decrement offset to go from left to right
            # top line animates <---- right to left
            if self.top_go:  # check flag
                tx = x - self.to + l  # max x minus offset plus length of the line
                tl = max(tx - l, 0)  # the biggest of tx less the length of the line or 0
                pygame.draw.line(s, c, (tl, 0), (tx, 0), t)  # draw the line on the top border
                if (x - self.to) < (0 - l // 2):  # if halfway off the surface tell left to go
                    self.left_go = True
                if (x - self.to) < (0 - l):  # stop drawing once off the surface
                    self.to = 0  # reset offset
                    self.top_go = False
                self.to += hl_vel  # increment offset to go from right to left
            btn_text = fck_scope['default font'].render(self.name, 1, c)  # render the button text
        self.display.draw(self.my_surface, self.rect.topleft)  # draw this button on the display
        self.display.draw(btn_text, (self.rect.centerx - off_x // 2, self.rect.centery - off_y // 2))  # draw the text

    def check_mouse(self):  # TODO: move mouse logic to main game loop to prevent double clicking
        # checks where the mouse is, returns true if it should do something
        s = 1.2  # the factor by which to scale the button
        action = False  # return flag
        if self.rect.collidepoint(self.display.get_relative_mouse_pos()):
            # if the mouse is overlapping with the button, using relative coordinates in the display
            if not self.highlight:  # if the button is not being highlighted, highlight it
                self.highlight = True  # set flag for animation in draw()
                self.scale_btn(s)  # scale the button up
                self.reset_anim()  # reset the animation for new button size
                self.hover_sound.play()  # play the hover sound
            if pygame.mouse.get_pressed()[0] and not self.clicked:  # left click
                action = True  # switch flag to do something
                self.clicked = True  # set this flag so that there isn't continuous execution each frame
        elif self.highlight:  # if highlighted but not colliding with mouse, stop highlighting
            self.highlight = False  # flag
            self.scale_btn(1 / s)  # scale back to original size
            self.reset_anim()  # reset the animation again

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False  # if the mouse isn't pressed, the button isn't being clicked

        return action  # return the action flag

    def reset_anim(self):
        # reset all the animation values
        self.to = 0  # top offset for highlight line
        self.bo = self.rect.size[0]
        self.lo = self.rect.size[1]
        self.ro = 0
        self.top_go = True
        self.bot_go = True
        self.left_go = False
        self.right_go = False

    def scale_btn(self, z):
        # scale the button to a new size from the center
        new_size = (self.rect.size[0] * z, self.rect.size[1] * z)  # the size
        new_x = self.rect.centerx - (z * self.rect.size[0] // 2)  # new topleft x location
        new_y = self.rect.centery - (z * self.rect.size[1] // 2)  # new topleft y location
        new_loc = (new_x, new_y)  # new topleft tuple
        self.my_surface = pygame.Surface(new_size)  # make a new surface of the new size
        self.rect = self.my_surface.get_rect()  # get its rectangle
        self.rect.topleft = new_loc  # place that rectangle at the new position


class Isotile:
    # if this isn't static then every time the map changes the tiles the animation will reset
    # all tiles should be kept in sync
    frame = 0  # animation frame (all tiles are in sync)
    hl_frame = 0  # highlight frame (in sync across all tiles)

    def __init__(self, tile_sprite, scale, display, point, can_highlight=True):
        for i in range(len(tile_sprite)):  # scale all frames
            tile_sprite[i-1] = pygame.transform.scale(tile_sprite[i-1], (20 * scale, 24 * scale))
        self.surface = tile_sprite[Isotile.frame]  # get the current surface
        self.anim_seq = tile_sprite  # get the full animation sequence
        self.scale = scale  # get the current scale
        self.display = display  # get the display to draw on
        self.point = point  # get the location of this tile (topleft)
        highlight = pygame.transform.scale(fck_scope['sprites']['highlight'][0], (20 * self.scale, 11 * self.scale))
        self.hl_rect = highlight.get_rect(topleft=point)  # where to draw the highlight on this tile
        self.can_hl = can_highlight  # if this tile is highlightable

    def detect_mouse_hover(self):
        # find out if the mouse is hovering on a tile with raycasting
        hover = False
        # mouse location
        mx, my = self.display.get_relative_mouse_pos()
        # listed clockwise from left corner, vertices of collision area
        vertices = [  # TODO: expand to outer edge and deal with overlap in code
            (self.point[0] + (0 * self.scale), self.point[1] + (5 * self.scale)),  # left corner
            (self.point[0] + (8 * self.scale), self.point[1] + (0 * self.scale)),  # top corners
            (self.point[0] + (11 * self.scale), self.point[1] + (0 * self.scale)),
            (self.point[0] + (19 * self.scale), self.point[1] + (5 * self.scale)),  # right corner
            (self.point[0] + (11 * self.scale), self.point[1] + (9 * self.scale)),  # bottom corners
            (self.point[0] + (8 * self.scale), self.point[1] + (9 * self.scale))
        ]
        n = len(vertices)
        p1x, p1y = vertices[0]
        for i in range(n + 1):
            p2x, p2y = vertices[i % n]
            if my > min(p1y, p2y):
                if my <= max(p1y, p2y):
                    if mx <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (my - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or mx <= xinters:
                            hover = not hover
            p1x, p1y = p2x, p2y
        return hover

    def draw(self):
        # draw self on the display for this tile
        pygame.draw.rect(self.surface, (255, 0, 0), self.hl_rect)
        self.display.draw(self.surface, self.point)

    def draw_hl(self):
        # draw highlight on the display
        if self.can_hl:
            if self.detect_mouse_hover():
                highlight = pygame.transform.scale(fck_scope['sprites']['highlight'][Isotile.hl_frame], (20 * self.scale, 11 * self.scale))
                self.display.draw(highlight, self.point)
                return True
        return False


class Isomap:
    def __init__(self, mapdata, display):
        #passed
        self.mapdata = mapdata  # map data to render
        self.display = display  # display to draw on

        # changes
        self.scale = 2  # scale of this map
        self.offset_x = self.display.get_width() // 2  # offset (default to middle)
        self.offset_y = self.display.get_height() // 2

        #default, declare the first time
        self.tiles = dict()  # all tiles in this map
        # TODO: remove scale from this calculation, make static
        self.iso_x = 10 * self.scale  # isometric offsets for projecting into isometric view
        self.iso_y = 5 * self.scale
        self.iso_z = 14 * self.scale

    def convert_coordinates(self, x, y):  # TODO: make static, remove offset from equation
        # convert given 2d coordinates to isometric
        conv_x = self.offset_x + x * self.iso_x - y * self.iso_x
        conv_y = self.offset_y + x * self.iso_y + y * self.iso_y
        return conv_x, conv_y

    def z_shift(self, point, level):  # TODO: merge with convert_coordinates and commit to 3D isometric
        z_shift_y = point[1] - (self.iso_z * level)
        return point[0], z_shift_y

    def reset_values(self):
        # reset values
        self.tiles = dict()
        self.iso_x = 10 * self.scale
        self.iso_y = 5 * self.scale
        self.iso_z = 14 * self.scale

    def update_tiles(self):
        # TODO: tiles other than default
        self.reset_values()
        for y, row in enumerate(self.mapdata):  # data y axis
            for x, tile in enumerate(row):  # data x axis
                if tile:
                    iso_pnt = self.convert_coordinates(x, y)
                    self.tiles[iso_pnt] = Isotile(fck_scope['sprites']['default'], self.scale, self.display, iso_pnt, can_highlight=False)
                    iso_pnt = self.z_shift(iso_pnt, tile)
                    self.tiles[iso_pnt] = Isotile(fck_scope['sprites']['default'], self.scale, self.display, iso_pnt, can_highlight=False)
                else:
                    iso_pnt = self.convert_coordinates(x, y)
                    self.tiles[iso_pnt] = Isotile(fck_scope['sprites']['default'], self.scale, self.display, iso_pnt)

    def scale_map(self, scalar):  # TODO: find a way to do this that doesnt have a big impact on calculation time
        # scales the map
        self.scale = scalar  # TODO: smooth scroll, animate?
        self.update_tiles()

    # TODO: preload the possible map positions on turn?
    # TODO: animate the spin
    def turn_clockwise(self):
        self.mapdata = list(zip(*self.mapdata[::-1]))  # clockwise
        self.update_tiles()

    def turn_counterclockwise(self):
        self.mapdata = list(zip(*self.mapdata))[::-1]  # counterclockwise
        self.update_tiles()

    def draw(self):
        # draw all the tiles
        for tile in self.tiles.values():
            tile.draw()
        for tile in self.tiles.values():  # draw tile highlights
            if tile.draw_hl():
                break  # first tile to draw the highlight ends it so no duplicates

        # move through frames of animation, we call this method every frame
        if Isotile.frame < fck_scope['tile anim len']:
            Isotile.frame += 1
        else:
            Isotile.frame = 0
        if Isotile.hl_frame < fck_scope['tile hl len']:
            Isotile.hl_frame += 1
        else:
            Isotile.hl_frame = 0


# SETUP WINDOW
WIN_W = 1600  # width of the window
WIN_H = WIN_W // 16 * 9  # 16:9 aspect ratio
DIS_W = WIN_W  # default to same as window width for now
DIS_H = DIS_W // 16 * 9  # 16:9 aspect ratio
WIN_TITLE = 'untitled game'  # window title
pygame.display.set_caption(WIN_TITLE)  # window title set
screen = pygame.display.set_mode((WIN_W, WIN_H))  # application window
main_surface = pygame.Surface((DIS_W, DIS_H))  # main_surface where things are rendered
pygame.key.set_repeat(1, 50)  # set all keys to repeat when held down
clock = pygame.time.Clock()  # used to lock fps in main game loop


def main():
    # VARIABLES
    # TODO: move all this into fck_scope

    # game state variables
    # main menu
    main_menu_size = (DIS_W // 5, DIS_H - 20)  # size
    main_menu_loc = (10, 10)  # location on main_surface
    main_menu_display = Display('Main Menu', main_menu_size, main_menu_loc, fck_scope['colors']['dis_blue'], fck_scope['colors']['black'], fck_scope['colors']['black'], main_surface)
    # pause menu
    pause_menu_size = (DIS_W // 5 * 2, DIS_H // 3 * 2)  # size
    pause_menu_loc = (DIS_W // 2 - pause_menu_size[0] // 2, DIS_H // 2 - pause_menu_size[1] // 2)  # location
    pause_menu_display = Display('', pause_menu_size, pause_menu_loc, fck_scope['colors']['dis_blue'], fck_scope['colors']['black'], fck_scope['colors']['black'], main_surface)
    # mission map
    map_iso_size = (DIS_W // 5 * 3, DIS_H - 20)  # size
    map_iso_loc = (DIS_W // 2 - map_iso_size[0] // 2, 10)  # location
    mission_display = Display('Mission', map_iso_size, map_iso_loc, fck_scope['colors']['dis_blue'], fck_scope['colors']['black'], fck_scope['colors']['black'], main_surface)

    # metrics and controls
    dt = 0  # delta time is milliseconds since last frame
    rt = 0  # raw time is milliseconds since last frame excluding frame lock delay
    fps = 24  # frames per second the main game is locked to

    # flags
    game_running = True  # for the main game loop

    # set values
    fck_scope['default font'] = pygame.font.Font(os.path.join('assets', 'fonts', 'AtlantisInternational-jen0.ttf'), 30)
    last_frame_keys = pygame.key.get_pressed()
    load_sprites()
    load_sounds()

    # MAIN GAME LOOP
    while game_running:
        m_wheel = 0

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                game_running = False  # ends main game loop
            if event.type == pygame.KEYUP:
                if event.key == K_F1:  # TODO: move this into key controls function where it belongs
                    fck_scope['debug mode'] = not fck_scope['debug mode']  # toggle debug mode
            if event.type == pygame.MOUSEWHEEL:
                m_wheel = event.y

        # CONTROLS
        # keyboard input
        keys = pygame.key.get_pressed()  # the state of all keys in an array
        if fck_scope['states']['mission']:
            handle_iso_movement(keys, last_frame_keys)  # TODO: one function for key controls
        last_frame_keys = keys  # keep these keys to track changes in next frame

        # mouse input
        # TODO: one function for mouse clicks, buttons, another for all mouse wheel stuff
        if fck_scope['states']['main menu']:
            check_button_collisions()
        elif fck_scope['states']['pause menu']:
            check_button_collisions()
        elif fck_scope['states']['mission']:
            handle_iso_zoom(m_wheel)

        # GAME LOGIC
        # none yet

        # RENDER GAME
        # fill screen to wipe away last frame
        main_surface.fill(fck_scope['colors']['black'])  # fills screen with solid black

        # state-dependent
        # main menu
        main_buttons = ['PLAY', 'TEST']  # TODO: move these to fck_scope
        pause_buttons = ['MAIN MENU', 'TEST']
        if fck_scope['states']['main menu']:
            if not fck_scope['main menu drawn']:  # TODO: change the name of this variable
                draw_menu(main_buttons, main_menu_display)
            for button in fck_scope['buttons']:
                button.draw()
            main_menu_display.render()
        # game pause
        elif fck_scope['states']['pause menu']:  # pause menu should draw instead of anything else
            if not fck_scope['main menu drawn']:
                draw_menu(pause_buttons, main_menu_display)
            for button in fck_scope['buttons']:
                button.draw()
            main_menu_display.render()
        elif fck_scope['states']['mission']:
            if not fck_scope['iso map loaded']:
                load_map('default.txt')
                fck_scope['current map'] = Isomap(fck_scope['current map data'], mission_display)
                fck_scope['iso map loaded'] = True  # switch flag
            if fck_scope['iso map loaded']:
                fck_scope['current map'].draw()
            mission_display.render()

        # debug_mode overlay
        if fck_scope['debug mode']:  # debug stuff draws on top of anything else being rendered
            dt_text = fck_scope['default font'].render('dt=' + str(dt) + 'ms', 1, fck_scope['colors']['white'])  # setup delta time text
            rt_text = fck_scope['default font'].render('rt=' + str(rt) + 'ms', 1, fck_scope['colors']['white'])  # setup raw time text
            mouse_text = fck_scope['default font'].render('mp=' + str(pygame.mouse.get_pos()), 1, fck_scope['colors']['white'])  # mouse position
            main_surface.blit(dt_text, (0, 0))  # add delta time tracker to upper left
            main_surface.blit(rt_text, (0, 25))  # add delta time tracker to upper left
            main_surface.blit(mouse_text, (0, 25 * 2))  # add mouse text

        # put work on the screen
        screen.blit(pygame.transform.scale(main_surface, screen.get_size()), (0, 0))  # put the display onto the screen
        pygame.display.update()  # update main_surface

        # FRAME LOCK / METRICS
        rt = clock.get_rawtime()  # keeps track of time since last frame without including waiting for frame lock
        dt = clock.tick(fps)  # measures the time since last frame

    pygame.quit()  # quit pygame or otherwise game will continue after closing


if __name__ == "__main__":
    main()
