from typing import TYPE_CHECKING

import pygame
import math

if TYPE_CHECKING:
    from engine.window import Window
    from engine.image import Surface

class Element(pygame.sprite.Sprite):
    def __init__(self, name:str, elements:"Elements", image:pygame.Surface, x:int=0, y:int=0, radius:int=0) -> None:
        super().__init__()
        if hasattr(image, 'get_surface'):
            self.ori_image = image.get_surface()
        else:
            self.ori_image = image

        self.name = name
        self.elements = elements

        self.image = self.ori_image.copy()

        self.degree = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = radius
        self.width = self.rect.width
        self.height = self.rect.height

        self.is_element_clicked = False

    def change_image(self, image:pygame.Surface):
        if hasattr(image, 'get_surface'):
            self.ori_image = image.get_surface()
        else:
            self.ori_image = image

        self.set_degree(self.degree)
        self.resize(self.width, self.height)

    def set_degree(self, degree:float):
        self.degree = degree
        self.image = pygame.transform.rotate(pygame.transform.scale(self.ori_image, (self.width, self.height)), degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def rotate(self, degree:float):
        self.set_degree((self.degree + degree) % 360)

    def look_at_cursor(self):
        mouse_x, mouse_y = self.get_mouse_position()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.set_degree(angle)

    def look_at(self, pos_x:int, pos_y:int):
        rel_x, rel_y = pos_x - self.rect.centerx, pos_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan(rel_y, rel_x)

        self.set_degree(angle)

    def resize(self, width:int, height:int):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def get_key_pressed(self):
        return pygame.key.get_pressed()

    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed()

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

    def is_mouse_pressed(self, mouse_btn:int):
        return self.get_mouse_pressed()[mouse_btn]

    def is_mouse_hover(self):
        return self.rect.collidepoint(self.get_mouse_position())
    
    def is_key_pressed(self, key):
        return self.get_key_pressed()[key]

    def is_clicked(self, mouse_btn:int):
        if self.is_mouse_hover():
            if self.is_mouse_pressed(mouse_btn):
                self.is_element_clicked = True
                return False
            else:
                if self.is_element_clicked:
                    self.is_element_clicked = False
                    return True
                else:
                    return False
        else:
            return False

    def delete(self):
        self.elements.remove_element(self.name)

class Elements:
    def __init__(self, window:"Window") -> None:
        self.elements = {}
        self.groups = {}
        self.window = window

    def create_group(self, name:str):
        self.groups[name] = pygame.sprite.Group()

    def get_group(self, name:str):
        return self.groups.get(name)

    def add_element(self, name:str, group:str, element:"Element"):
        self.elements[name] = element
        self.groups[group].add(element)

        self.window.elements_group.empty()
        for g in self.groups.values():
            for el in g.sprites():
                self.window.elements_group.add(el)
                self.window.elements_group

    def get_element(self, name:str):
        return self.elements.get(name)

    def remove_element(self, name:str):
        self.elements.get(name).kill()
        del self.elements[name]