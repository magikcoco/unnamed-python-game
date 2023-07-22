
## DEFINES CUSTOM OBJECTS FOR THE GAME ##

import pygame
import game_values as value


class Display:
    def __init__(self, name, s_size, location, border_color, fill_color, text_color, main_surface):
        print(self)
        self.my_surface = pygame.Surface(s_size)  # the surface within the display
        self.main_surface = main_surface  # the surface to draw the display onto
        self.location = location  # the location of the display relative to the main surface
        self.name = name  # the name of this display
        self.render_queue = list()  # the list of things to draw when this display is rendered
        self.text_color = text_color  # the color with which to draw text
        self.fill_color = fill_color  # the fill color for the background of this display
        self.border_color = border_color  # the border color of this display
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
        title = value.GAME_FONT.render(self.name, 1, self.text_color)
        text_width, text_height = value.GAME_FONT.size(self.name)
        self.my_surface.blit(title, (self.border_top.centerx - text_width // 2, 0))
        self.main_surface.blit(self.my_surface, self.location)

    def draw(self, thing, location):
        self.render_queue.append((thing, location))

    def move_to(self, x, y):
        self.location[0] = x
        self.location[1] = y

    def get_relative_mouse_pos(self):
        m_pos = pygame.mouse.get_pos()
        return m_pos[0] - self.location[0], m_pos[1] - self.location[1]

    def get_width(self):
        return self.my_surface.get_width()

    def get_height(self):
        return self.my_surface.get_height()


class Button:
    def __init__(self, name, display, location, image_tuple):
        print(display)
        self.image = image_tuple[0]
        self.image_hl = image_tuple[1]
        self.display = display
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.clicked = False
        self.highlight = False

    def draw(self):
        self.display.draw(self.image, self.rect.topleft)

    def check_mouse(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.highlight:
                temp = self.image
                self.image = self.image_hl
                self.image_hl = temp
                self.highlight = True
                #self.draw()
            if pygame.mouse.get_pressed()[0] and not self.clicked:  # left click
                action = True
                self.clicked = True
        elif self.highlight:
            temp = self.image
            self.image = self.image_hl
            self.image_hl = temp
            self.highlight = False
            self.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
