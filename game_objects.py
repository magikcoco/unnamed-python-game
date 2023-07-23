import math

## DEFINES CUSTOM OBJECTS FOR THE GAME ##

import pygame
import game_values as value


class Point:
    def __init__(self, point=(0, 0)):
        self.x = int(point[0])
        self.y = int(point[1])

    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))

    def __floordiv__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    def get(self):
        return (self.x, self.y)


def _draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement//length
    for i in range(0, length//dash_length, 2):
        start = origin + (slope * i * dash_length)
        end = origin + (slope * (i + 1) * dash_length)
        pygame.draw.line(surface, color, start.get(), end.get(), width)


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
        self.hl_flag = True
        self.hl_tick = 10
        self.hl_tick_c = self.hl_tick

    def draw(self):
        self.my_surface.fill(self.display.get_fill())
        x = self.rect.size[0]
        y = self.rect.size[1]
        off_x, off_y = value.GAME_FONT.size(self.name)
        lt = 2  # line thickness
        dt = 40
        s = self.my_surface
        if not self.highlight:
            c = self.color
            pygame.draw.line(s, c, (x - lt, 0), (x - lt, y), lt)  # right
            pygame.draw.line(s, c, (0, 0), (0, y), lt)  # left
            pygame.draw.line(s, c, (0, y - lt), (x, y - lt), lt)  # bot
            pygame.draw.line(s, c, (0, 0), (x, 0), lt)  # top
            btn_text = value.GAME_FONT.render(self.name, 1, self.color)
        else:
            c = self.color_hl
            if not self.hl_tick_c:
                self.hl_tick_c = self.hl_tick
                self.hl_flag = not self.hl_flag
            else:
                self.hl_tick_c -= 1
            if self.hl_flag:
                _draw_dashed_line(s, c, (x - lt, y), (x - lt, 0), lt, dt)  # right
                _draw_dashed_line(s, c, (0, 0), (0, y), lt, dt)  # left
                _draw_dashed_line(s, c, (x, y - lt), (0, y - lt), lt, dt)  # bot
                _draw_dashed_line(s, c, (0, 0), (x, 0), lt, dt)  # top
            else:
                _draw_dashed_line(s, c, (x - lt, 0), (x - lt, y), lt, dt)  # right
                _draw_dashed_line(s, c, (0, y), (0, 0), lt, dt)  # left
                _draw_dashed_line(s, c, (0, y - lt), (x, y - lt), lt, dt)  # bot
                _draw_dashed_line(s, c, (x, 0), (0, 0), lt, dt)  # top
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

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
