from engine.component import Component
from engine.input import Input
import pygame


class Sprite(Component):
    def __init__(self, draw_window, image_path, width, height, origin=(0, 0)):
        super().__init__()
        self.window = draw_window
        self.image = pygame.image.load(image_path)
        self.w = width
        self.h = height
        self.angle = 45

    def on_update(self, dt):
        if self.enabled:
            transform = self.gameobject.get_component("Transform")

            scaled = pygame.transform.scale(self.image, (self.w, self.h))
            rotated = pygame.transform.rotate(scaled, 45)
            self.window.blit(rotated, (transform.x, transform.y))
