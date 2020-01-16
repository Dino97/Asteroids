import math
import pygame
import random
import copy
import asteroidgame


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, player, speed_increase):
        super().__init__()
        self.original_img = pygame.image.load('images/asteroid.png')
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.asteroid_w, self.asteroid_h = self.original_img.get_size()
        self.player_x, self.player_y = player.rect.center
        self.speed = 250 + speed_increase
        self.acceleration = self.speed * 3
        self.velocity = pygame.Vector2()
        # zatrebace posle
        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5
        self.degrees = 0
        self.get_random_coordinates()
        self.get_angle_towards_player()

        self.mask = pygame.mask.from_surface(self.image)

    def copy(self, asteroid):
        copyobj = Asteroid(asteroid, 0)

        for name, attr in self.__dict__.items():
            if name == 'mask':
                continue
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)

        return copyobj

    def death(self, asteroid, asteroids):
        rads = asteroid.degrees
        asteroid_two = asteroid.copy(asteroid)
        if asteroid.points == 150:
            for x in range(2):
                asteroid.points = 100
                asteroid.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (32, 32))
                asteroid.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                asteroid.mask = pygame.mask.from_surface(asteroid.image)

                asteroid_two.points = 100
                asteroid_two.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (32, 32))
                asteroid_two.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                asteroid_two.mask = pygame.mask.from_surface(asteroid.image)
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
            asteroid_two = asteroid.copy(asteroid)
            for x in range(2):
                asteroid.points = 150
                asteroid.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (64, 64))
                asteroid.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                asteroid.mask = pygame.mask.from_surface(asteroid.image)

                asteroid_two.points = 150
                asteroid_two.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (64, 64))
                asteroid_two.rect = asteroid.image.get_rect(center=asteroid.rect.center)
                asteroid_two.mask = pygame.mask.from_surface(asteroid.image)
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
            self.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (96, 96))
            self.points = 200
        if choice == 2:
            self.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (64, 64))
            self.points = 150
        if choice == 3:
            self.image = pygame.transform.smoothscale(pygame.image.load('images/asteroid.png'), (32, 32))
            self.points = 100

        self.rect = self.image.get_rect()
        choice = random.choice([1, 2, 3, 4])

        if choice == 1:
            x = 0 + 5
            y = random.randint(0, self.screen_h)
            self.rect.right = x
            self.rect.bottom = y
            return x, y
        elif choice == 2:
            x = self.screen_w - 5
            y = random.randint(0, self.screen_h)
            self.rect.right = x
            self.rect.bottom = y
            return x, y
        elif choice == 3:
            x = random.randint(0, self.screen_w)
            y = 0 + 5
            self.rect.right = x
            self.rect.bottom = y
            return x, y
        elif choice == 4:
            x = random.randint(0, self.screen_w)
            y = self.screen_h - 5
            self.rect.right = x
            self.rect.bottom = y
            return x, y

    def get_angle_towards_player(self):
        x, y = self.rect.center
        dx = x - self.player_x
        dy = y - self.player_y
        rads = math.atan2(-dy, -dx)

        # see why
        rads %= 2*math.pi
        self.degrees = math.degrees(rads)
        self.velocity.x = self.speed * math.cos(rads)/100
        self.velocity.y = self.speed * math.sin(rads)/100

    def move(self):

        x, y = self.rect.center

        # bottom edge
        if y > self.screen_h + self.asteroid_h / 2:
            y = -self.asteroid_h / 2
            print("bottom")
        # top edge
        elif y < -self.asteroid_h / 2:
            y = self.screen_h + self.asteroid_h / 2
            print("top")
        # left edge
        if x < -self.asteroid_w / 2:
            x = self.screen_w + self.asteroid_w / 2
            print("left")
        # right edge
        elif x > self.screen_w + self.asteroid_w / 2:
            x = -self.asteroid_w / 2
            print("right")

        x += self.velocity.x
        y += self.velocity.y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        if asteroidgame.AsteroidGame.debug:
            pygame.draw.rect(pygame.display.get_surface(), (150, 0, 30), self.rect, 1)

            # my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 20)
            my_font = pygame.font.SysFont('Ariel', 20)

            text_surface = my_font.render("xVel: " + "{0:.2f}".format(self.velocity.x), False, (150, 0, 30))
            screen.blit(text_surface, self.rect.move(self.rect.w + 5, 0))
            text_surface = my_font.render("yVel: " + "{0:.2f}".format(self.velocity.y), False, (150, 0, 30))
            screen.blit(text_surface, self.rect.move(self.rect.w + 5, 15))

        screen.blit(self.image, self.rect)
