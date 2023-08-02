
## DEFINES CUSTOM OBJECTS FOR THE GAME ##

import pygame
import game_values as value


class Display:  # a display for components on the screen
    def __init__(self, name, s_size, location, border_color, fill_color, text_color, main_surface):
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
            title = value.GAME_FONT.render(self.name, 1, self.text_color)
            text_width, text_height = value.GAME_FONT.size(self.name)
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
        self.hover_sound = value.SOUNDS['button hover']  # the sound this button makes when hovered over

    def draw(self):
        # draws this button onto it's display
        s = self.my_surface  # abbreviation for self.my_surface, makes things look a little neater
        s.fill(self.display.get_fill())  # wipe away last frame
        x = self.rect.size[0]  # the maximum x value
        y = self.rect.size[1]  # the maximum y value
        off_x, off_y = value.GAME_FONT.size(self.name)  # the offsets for the text in the button
        hl_vel = 10  # how fast the line moves
        t = 2  # line thickness
        l = 40  # length of animated line on highlight
        if not self.highlight:  # if the button is not currently highlighted
            c = self.color  # abbreviation for self.color for neater expressions
            pygame.draw.line(s, c, (x - t, 0), (x - t, y), t)  # right
            pygame.draw.line(s, c, (0, 0), (0, y), t)  # left
            pygame.draw.line(s, c, (0, y - t), (x, y - t), t)  # bot
            pygame.draw.line(s, c, (0, 0), (x, 0), t)  # top
            btn_text = value.GAME_FONT.render(self.name, 1, self.color)  # render the button text
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
            btn_text = value.GAME_FONT.render(self.name, 1, c)  # render the button text
        self.display.draw(self.my_surface, self.rect.topleft)  # draw this button on the display
        self.display.draw(btn_text, (self.rect.centerx - off_x // 2, self.rect.centery - off_y // 2))  # draw the text

    def check_mouse(self):
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
    frame = 0
    hl_frame = 0

    def __init__(self, tile_sprite, scale, display, point, can_highlight=True):
        for i in range(len(tile_sprite)):
            tile_sprite[i-1] = pygame.transform.scale(tile_sprite[i-1], (20 * scale, 24 * scale))
        self.surface = tile_sprite[Isotile.frame]
        self.anim_seq = tile_sprite
        self.scale = scale
        self.display = display
        self.point = point
        highlight = pygame.transform.scale(value.SPRITES['highlight'][0], (20 * self.scale, 11 * self.scale))
        self.hl_rect = highlight.get_rect(topleft=point)
        self.can_hl = can_highlight
        self.made_sound = False

    def detect_mouse_hover(self):
        hover = False
        # mouse location
        mx, my = self.display.get_relative_mouse_pos()
        # listed clockwise from left corner, vertices of collision area
        vertices = [
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
        pygame.draw.rect(self.surface, (255, 0, 0), self.hl_rect)
        self.display.draw(self.surface, self.point)

    def draw_hl(self):
        if self.can_hl:
            if self.detect_mouse_hover():
                highlight = pygame.transform.scale(value.SPRITES['highlight'][Isotile.hl_frame], (20 * self.scale, 11 * self.scale))
                self.display.draw(highlight, self.point)
                return True
        return False


class Isomap:
    def __init__(self, mapdata, display):
        #passed
        self.mapdata = mapdata
        self.display = display

        # changes
        self.scale = 2
        self.offset_x = self.display.get_width() // 2
        self.offset_y = self.display.get_height() // 2

        #default, declare the first time
        self.tiles = dict()
        self.iso_x = 10 * self.scale
        self.iso_y = 5 * self.scale
        self.iso_z = 14 * self.scale

    def convert_coordinates(self, x, y):
        conv_x = self.offset_x + x * self.iso_x - y * self.iso_x
        conv_y = self.offset_y + x * self.iso_y + y * self.iso_y
        return conv_x, conv_y

    def z_shift(self, point, level):
        z_shift_y = point[1] - (self.iso_z * level)
        return point[0], z_shift_y

    def reset_values(self):
        self.tiles = dict()
        self.iso_x = 10 * self.scale
        self.iso_y = 5 * self.scale
        self.iso_z = 14 * self.scale

    def update_tiles(self):  # TODO: tiles other than default
        self.reset_values()
        for y, row in enumerate(self.mapdata):  # data y axis
            for x, tile in enumerate(row):  # data x axis
                if tile:
                    iso_pnt = self.convert_coordinates(x, y)
                    self.tiles[iso_pnt] = Isotile(value.SPRITES['default'], self.scale, self.display, iso_pnt, can_highlight=False)
                    iso_pnt = self.z_shift(iso_pnt, tile)
                    self.tiles[iso_pnt] = Isotile(value.SPRITES['default'], self.scale, self.display, iso_pnt, can_highlight=False)
                else:
                    iso_pnt = self.convert_coordinates(x, y)
                    self.tiles[iso_pnt] = Isotile(value.SPRITES['default'], self.scale, self.display, iso_pnt)

    def scale_map(self, scalar):  # TODO: find a way to do this that doesnt have a big impact on calculation time
        self.scale = scalar
        self.update_tiles()

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
        for tile in self.tiles.values():
            if tile.draw_hl():
                break

        # move through frames of animation, we call this method every frame
        if Isotile.frame < value.TILE_ANIM_LEN:
            Isotile.frame += 1
        else:
            Isotile.frame = 0
        if Isotile.hl_frame < value.TILE_HL_ANIM_LEN:
            Isotile.hl_frame += 1
        else:
            Isotile.hl_frame = 0
