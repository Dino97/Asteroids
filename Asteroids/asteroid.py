import math
import pygame
import random
import copy


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.original_img = pygame.image.load('asteroid.png')
        self.image = pygame.image.load('asteroid.png')
        self.rect = self.original_img.get_rect()
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.rect.center = self.get_random_coordinates()
        self.asteroid_w, self.asteroid_h = self.original_img.get_size()
        x, y = player.rect.center
        self.player_x = x
        self.player_y = y
        # vidi sta ti treba
        self.speed = 700
        self.acceleration = self.speed * 3
        self.velocity = pygame.Vector2()
        # zatrebace posle
        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5
        self.degrees = 0
        self.get_angle_towards_player()

    def copy(self):
        copyobj = Asteroid(1, 1)
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj

    def death(self, asteroid, asteroids):
        rads = asteroid.degrees
        asteroid_two = asteroid.copy()
        if asteroid.points == 150:
            for x in range(2):
                asteroid.points = 100
                asteroid.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (16, 16))
                asteroid.rect = asteroid.image.get_rect(center=asteroid.rect.center)

                asteroid_two.points = 100
                asteroid_two.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (16, 16))
                asteroid_two.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                if x == 0:
                    asteroid.velocity.x = self.speed * math.cos(math.radians(rads + 5)) / 100
                    asteroid.velocity.y = self.speed * math.sin(math.radians(rads + 5)) / 100
                if x == 1:
                    asteroid_two.velocity.x = self.speed * math.cos(math.radians(rads - 5)) / 100
                    asteroid_two.velocity.y = self.speed * math.sin(math.radians(rads - 5)) / 100
                asteroids.add(asteroid)
                asteroids.add(asteroid_two)
        if asteroid.points == 200:
            rads = asteroid.degrees
            asteroid_two = asteroid.copy()
            for x in range(2):
                asteroid.points = 150
                asteroid.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (32, 32))
                asteroid.rect = asteroid.image.get_rect(center=asteroid.rect.center)

                asteroid_two.points = 150
                asteroid_two.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (32, 32))
                asteroid_two.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                if x == 0:
                    asteroid.velocity.x = self.speed * math.cos(math.radians(rads + 5)) / 100
                    asteroid.velocity.y = self.speed * math.sin(math.radians(rads + 5)) / 100
                if x == 1:
                    asteroid_two.velocity.x = self.speed * math.cos(math.radians(rads - 5)) / 100
                    asteroid_two.velocity.y = self.speed * math.sin(math.radians(rads - 5)) / 100
                asteroids.add(asteroid)
                asteroids.add(asteroid_two)

    def get_random_coordinates(self):
        choice = random.choice([1, 2, 3])

        if choice == 1:
            self.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (48, 48))
            self.points = 200
        if choice == 2:
            self.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (32, 32))
            self.points = 150
        if choice == 3:
            self.image = pygame.transform.smoothscale(pygame.image.load('asteroid.png'), (16, 16))
            self.points = 100

        self.rect = self.image.get_rect()

        choice = random.choice([1, 2, 3, 4])

        if choice == 1:
            return 0, random.randint(0, self.screen_h)
        elif choice == 2:
            return self.screen_w, random.randint(0, self.screen_h)
        elif choice == 3:
            return random.randint(0, self.screen_w), 0
        elif choice == 4:
            return random.randint(0, self.screen_w), self.screen_h

    def get_angle_towards_player(self, again = None):
        x, y = self.rect.center
        dx = x - self.player_x
        dy = y - self.player_y
        rads = math.atan2(-dy, -dx)

        # see why
        rads %= 2*math.pi
        self.degrees = math.degrees(rads)
        self.velocity.x = self.speed * math.cos(rads)/100
        self.velocity.y = self.speed * math.sin(rads)/100

    def draw(self, screen):
        x, y = self.rect.center
        x += self.velocity.x
        y += self.velocity.y
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect.center)

