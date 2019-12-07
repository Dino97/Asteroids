from engine.scene import Scene
from engine.input import Input
from engine.components.sprite import Sprite
from engine.gameobject import GameObject
from engine.component import Component
import pygame

pygame.init()

FPS = 60
clock = pygame.time.Clock()


class Game:
    loadedscene: Scene

    def __init__(self, name, resolution):
        self.window = pygame.display.set_mode(resolution)
        pygame.display.set_caption(name)
        self.clear_color = (20, 22, 25)
        self.running = False
        self.loadedscene = Scene()

    def start(self):
        # main update loop
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    Input.keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    Input.keys[event.key] = False

            self.window.fill(self.clear_color)

            pygame.draw.rect(self.window, (150, 0, 30), [10, 10, 300, 300], 0)

            for gameobject in self.loadedscene.gameobjects:
                for component in gameobject.components.values():
                    component.on_update(1/FPS)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    def load_scene(self, scene):
        self.loadedscene = scene

