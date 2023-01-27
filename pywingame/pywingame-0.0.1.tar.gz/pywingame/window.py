import pygame
from engine.event import Event

pygame.init()
pygame.font.init()

class Window:
    def __init__(self, geometry:tuple[int, int]=(500, 500), title:str="pygame window", fullscreen:bool=False, FPS:int=60, event_obj:Event=Event()):
        pygame.display.set_caption(title)
        if fullscreen:
            self.window = pygame.display.set_mode(geometry, pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(geometry)
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.elements_group = pygame.sprite.Group()
        self.event_obj = event_obj

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)

            # 取得輸入
            self.event_obj.events = pygame.event.get()
            for event in self.event_obj.events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # 更新游戲
            self.elements_group.update(self)
            self.event_obj.update(self)

            # 畫面顯示
            self.window.fill((255, 255, 255))
            self.elements_group.draw(self.window)
            self.event_obj.draw(self)
            pygame.display.update()

        pygame.quit()