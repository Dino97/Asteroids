import math
import pygame
import random


class Laser(pygame.sprite.Sprite):
    def __init__(self, playerX, playerY, angle):
        super().__init__()
        self.original_img = pygame.transform.smoothscale(pygame.image.load('laser_red.png'), (8, 24))
        self.image = self.original_img
        self.rect = self.image.get_rect()
        self.rect.center = (playerX, playerY)
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.laser_w, self.laser_h = self.image.get_size()

        self.player_x = playerX
        self.player_y = playerY

        self.speed = 700
        self.acceleration = self.speed * 3

        self.velocity = pygame.Vector2()
        self.velocity.x = 0.00
        self.velocity.y = 0.00

        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5

        self.position(angle)

    def position(self, angle):
        self.image = pygame.transform.rotate(self.original_img, angle)
        rads = math.radians(angle + 270)

        self.velocity.x = self.speed * math.cos(rads)/100
        self.velocity.y = self.speed * math.sin(rads)/100

    def draw(self, screen):
        x, y = self.rect.center
        x -= self.velocity.x
        y += self.velocity.y
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect.center)