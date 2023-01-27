import pygame

class Surface:
    def __init__(self, surface:pygame.Surface) -> None:
        self.surface = surface
    
    def get_surface(self):
        return self.surface

class Image(Surface):
    def __init__(self, path:str):
        surface = pygame.image.load(path)
        super().__init__(surface)

    def resize(self, width:int, height:int):
        self.surface = pygame.transform.scale(self.surface, (width, height))
        return self.surface

class Text(Surface):
    def __init__(self, text:str, font:str="arial", color=(0, 0, 0), size:int=32, bold:bool=False, italic:bool=False) -> None:
        surface = pygame.font.SysFont(font, size, bold, italic).render(text, True, color)
        super().__init__(surface)

class Rectangle(Surface):
    def __init__(self, geometry:tuple=(50, 50), color:tuple=(0, 0, 0)) -> None:
        surface = pygame.Surface(geometry, pygame.SRCALPHA)
        surface.fill(color)
        super().__init__(surface)