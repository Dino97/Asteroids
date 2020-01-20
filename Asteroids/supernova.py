import pygame
import math


class Supernova(pygame.sprite.Sprite):
    RADIUS = 100
    SPEED = 5
    PULSE_DURATION = 5000

    def __init__(self, position):
        super().__init__()

        self.spawn_time = pygame.time.get_ticks()
        self.position = position
        self.rect = None

    def update(self, *args):
        radius = math.fabs(math.sin(pygame.time.get_ticks() / 1000 * Supernova.SPEED)) * Supernova.RADIUS
        radius = max(radius, Supernova.RADIUS * 0.7)

        # draw outline
        self.rect = pygame.draw.circle(args[0], (255, 255, 255), self.position, math.ceil(radius), 1)
