from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from engine.element import Element
    from engine.window import Window

MOUSE_BTN_LEFT = 0
MOUSE_BTN_MIDDLE = 1
MOUSE_BTN_RIGHT = 2

class Event:
    def __init__(self):
        self.events = None

    def collide_group_rect(self, group1:pygame.sprite.Group, group2:pygame.sprite.Group):
        return list(pygame.sprite.groupcollide(group1, group2, False, False).items())

    def collide_group_circle(self, group1:pygame.sprite.Group, group2:pygame.sprite.Group):
        return list(pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_circle).items())

    def collide_rect(self, element1:"Element", element2:"Element"):
        return pygame.sprite.collide_rect(element1, element2)
    
    def collide_circle(self, element1:"Element", element2:"Element"):
        return pygame.sprite.collide_circle(element1, element2)

    def get_key_pressed(self):
        return pygame.key.get_pressed()

    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed()

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

    def is_mouse_pressed(self, mouse_btn:int):
        return self.get_mouse_pressed()[mouse_btn]

    def is_mouse_hover(self, element:"Element"):
        return element.is_mouse_hover()
    
    def is_key_pressed(self, key):
        return self.get_key_pressed()[key]

    def is_clicked(self, element:"Element", mouse_btn:int):
        return element.is_clicked(mouse_btn)

    def update(self, window:"Window"):
        pass

    def draw(self, window:"Window"):
        pass