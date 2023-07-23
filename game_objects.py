
## DEFINES CUSTOM OBJECTS FOR THE GAME ##

import pygame
import game_values as value


class Display:
    def __init__(self, name, s_size, location, border_color, fill_color, text_color, main_surface):
        self.my_surface = pygame.Surface(s_size)  # the surface within the display
        self.main_surface = main_surface  # the surface to draw the display onto
        self.location = location  # the location of the display relative to the main surface
        self.name = name.strip()  # the name of this display
        self.render_queue = list()  # the list of things to draw when this display is rendered
        self.text_color = text_color  # the color with which to draw text
        self.fill_color = fill_color  # the fill color for the background of this display
        self.border_color = border_color  # the border color of this display
        if self.name == '':
            self.border_top = pygame.Rect((0, 0), (s_size[0], 10))  # the borders of this display
        else:
            self.border_top = pygame.Rect((0, 0), (s_size[0], 30))  # the borders of this display
        self.border_left = pygame.Rect((0, 0), (10, s_size[1]))
        self.border_right = pygame.Rect((s_size[0] - 10, 0), (10, s_size[1]))
        self.border_bottom = pygame.Rect((0, s_size[1] - 10), (s_size[0], 10))

    def render(self):
        self.my_surface.fill(self.fill_color)
        for thing, location in self.render_queue:
            self.my_surface.blit(thing, location)
        self.render_queue.clear()
        pygame.draw.rect(self.my_surface, self.border_color, self.border_bottom)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_right)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_left)
        pygame.draw.rect(self.my_surface, self.border_color, self.border_top)
        if not self.name == '':
            title = value.GAME_FONT.render(self.name, 1, self.text_color)
            text_width, text_height = value.GAME_FONT.size(self.name)
            self.my_surface.blit(title, (self.border_top.centerx - text_width // 2, 0))
        self.main_surface.blit(self.my_surface, self.location)

    def draw(self, thing, location):
        self.render_queue.append((thing, location))

    def move_to(self, x, y):
        self.location[0] = x
        self.location[1] = y

    def get_fill(self):
        return self.fill_color

    def get_relative_mouse_pos(self):
        m_pos = pygame.mouse.get_pos()
        return m_pos[0] - self.location[0], m_pos[1] - self.location[1]

    def get_width(self):
        return self.my_surface.get_width()

    def get_height(self):
        return self.my_surface.get_height()


class Button:
    def __init__(self, name, s_size, color, color_hl, display, location):
        self.my_surface = pygame.Surface(s_size)
        self.display = display
        self.name = name
        self.rect = self.my_surface.get_rect()
        self.rect.topleft = location
        self.clicked = False
        self.highlight = False
        self.color = color
        self.color_hl = color_hl
        self.to = 0  # top offset for highlight line
        self.bo = self.rect.size[0]
        self.lo = self.rect.size[1]
        self.ro = 0
        self.top_go = True
        self.bot_go = True
        self.left_go = False
        self.right_go = False

    def draw(self):
        self.my_surface.fill(self.display.get_fill())
        x = self.rect.size[0]
        y = self.rect.size[1]
        off_x, off_y = value.GAME_FONT.size(self.name)
        hl_vel = 10  # how fast the line moves
        t = 2  # line thickness
        l = 40  # length of animated line on highlight
        s = self.my_surface
        if not self.highlight:
            c = self.color
            pygame.draw.line(s, c, (x - t, 0), (x - t, y), t)  # right
            pygame.draw.line(s, c, (0, 0), (0, y), t)  # left
            pygame.draw.line(s, c, (0, y - t), (x, y - t), t)  # bot
            pygame.draw.line(s, c, (0, 0), (x, 0), t)  # top
            btn_text = value.GAME_FONT.render(self.name, 1, self.color)
        else:
            c = self.color_hl
            # right line animates bottom to top
            if self.right_go:
                ry = y - self.ro + l
                rl = max(ry - l, 0)
                pygame.draw.line(s, c, (x - t, rl), (x - t, ry), t)
                if (y - self.ro) < (0 - l // 2):
                    self.top_go = True
                if (y - self.ro) < (0 - l):
                    self.ro = 0
                    self.right_go = False
                self.ro += hl_vel
            # left line animates top to bottom
            if self.left_go:
                ly = y - self.lo
                ll = max(ly - l, 0)
                pygame.draw.line(s, c, (0, ll), (0, ly), t)
                if (y - self.lo) > (self.rect.size[1] + l // 2):
                    self.bot_go = True
                if (y - self.lo) > (self.rect.size[1] + l):
                    self.lo = self.rect.size[1]
                    self.left_go = False
                self.lo -= hl_vel
            # bottom line animates ----> left to right
            if self.bot_go:
                bx = x - self.bo
                bl = max(bx - l, 0)
                pygame.draw.line(s, c, (bl, y - t), (bx, y - t), t)
                if (x - self.bo) > (self.rect.size[0] + l // 2):
                    self.right_go = True
                if (x - self.bo) > (self.rect.size[0] + l):
                    self.bo = self.rect.size[0]
                    self.bot_go = False
                self.bo -= hl_vel
            # top line animates <---- right to left
            if self.top_go:
                if (x - self.to) < (0 - l // 2):
                    self.left_go = True
                if (x - self.to) < (0 - l):
                    self.to = 0
                    self.top_go = False
                tx = x - self.to + l
                tl = max(tx - l, 0)
                self.to += hl_vel
                pygame.draw.line(s, c, (tl, 0), (tx, 0), t)
            # text for button
            btn_text = value.GAME_FONT.render(self.name, 1, c)
        self.display.draw(self.my_surface, self.rect.topleft)
        self.display.draw(btn_text, (self.rect.centerx - off_x // 2, self.rect.centery - off_y // 2))

    def check_mouse(self):
        action = False
        if self.rect.collidepoint(self.display.get_relative_mouse_pos()):
            if not self.highlight:
                self.highlight = True
            if pygame.mouse.get_pressed()[0] and not self.clicked:  # left click
                action = True
                self.clicked = True
        elif self.highlight:
            self.highlight = False
            self.reset_anim()

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action

    def reset_anim(self):
        self.to = 0  # top offset for highlight line
        self.bo = self.rect.size[0]
        self.lo = self.rect.size[1]
        self.ro = 0
        self.top_go = True
        self.bot_go = True
        self.left_go = False
        self.right_go = False
