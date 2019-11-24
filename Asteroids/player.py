import math
import pygame
from laser import Laser
from asteroid import Asteroid


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_img = pygame.image.load('flying-rocket64_expertly_edited.png')
        self.image = pygame.image.load('flying-rocket64_expertly_edited.png')
        self.rect = self.original_img.get_rect()

        # position variables
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.player_w, self.player_h = self.image.get_size()

        # movement variables
        self.speed = 700
        self.acceleration = self.speed*3
        self.velocity = [0.0, 0.0]
        self.top_speed = self.speed
        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5

        # valjda je ovako
        self.player_x = self.screen_w/2 - self.player_w
        self.player_y = self.screen_h/2 - self.player_h
        self.rect = self.original_img.get_rect(center=(self.player_x, self.player_y))

        # keys pressed
        self.up_bool = False
        self.right_bool = False
        self.left_bool = False

        # hm
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.asteroid_spawn = pygame.USEREVENT + 1
        self.is_dead = False
        self.points = 0

    def move(self, screen):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == self.asteroid_spawn:
                self.create_asteroid()
            self.do_key_stuff(event)

        self.draw_lasers(screen)
        self.draw_asteroids(screen)
        # Limit player from exiting the screen
        self.limit_exiting()
        self.draw(screen)
        return True

    def draw_asteroids(self, screen):
        for asteroid in self.asteroids.sprites():
            x, y = asteroid.rect.center
            if x < 0 or x > self.screen_w or y < 0 or y > self.screen_h:
                asteroid.kill()
            asteroid.draw(screen)

    def draw_lasers(self, screen):
        for laser in self.lasers.sprites():
            x, y = laser.rect.center
            if x < 0 or x > self.screen_w or y < 0 or y > self.screen_h:
                laser.kill()
            laser.draw(screen)

    def limit_exiting(self):
        x, y = self.rect.center
        if x <= 0:
            x = 0 + 5

        elif x >= self.screen_w - self.player_w:
            x = self.screen_w - self.player_w

        if y <= 0:
            y = 0 + 5

        elif y >= self.screen_h - self.player_h:
            y = self.screen_h - self.player_h

        self.rect.center = (x, y)

    def rotate(self):

        self.rotate_degrees_total += self.rotate_degrees
        self.rotate_degrees_total %= 360
        self.image = pygame.transform.rotate(self.original_img, self.rotate_degrees_total)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        # also dont know why 270
        rads = math.radians(self.rotate_degrees_total + 270)
        #

        if self.up_bool:
            self.velocity[0] += self.acceleration*math.cos(rads)/10000
            self.velocity[1] += self.acceleration*math.sin(rads)/10000
        else:
            if self.velocity[0] > 0:
                self.velocity[0] -= self.acceleration/20000
            else:
                self.velocity[0] += self.acceleration / 20000
            if self.velocity[1] > 0:
                self.velocity[1] -= self.acceleration/20000
            else:
                self.velocity[1] += self.acceleration/20000
            if abs(self.acceleration/20000) >= abs(self.velocity[0]):
                self.velocity[0] = 0.00
            if abs(self.acceleration/20000) >= abs(self.velocity[1]):
                self.velocity[1] = 0.00
        self.restrict_speed()

        x, y = self.rect.center
        # vaj ovo mora da bude, provali wtf radi na drugom kodu msm nema smisla stvarno znaci ono -
        x -= self.velocity[0]
        #
        y += self.velocity[1]

        # change position
        self.rect.center = (x, y)

    def restrict_speed(self):
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj)
            self.velocity[0] = self.top_speed*math.cos(angle)
            self.velocity[1] = self.top_speed*math.sin(angle)

    def draw(self, screen):
        self.rotate()
        self.thrust()
        if not self.is_dead:
            screen.blit(self.image, self.rect)
        my_font = pygame.font.SysFont('Vera', 30)
        text_surface = my_font.render(str(self.points), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

    def create_asteroid(self):
        x, y = self.rect.center
        self.asteroids.add(Asteroid(x, y))

    def do_key_stuff(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.left_bool = True
                if self.right_bool:
                    self.rotate_degrees = 0
                else:
                    self.rotate_degrees = self.turning_speed

            if event.key == pygame.K_RIGHT:
                self.right_bool = True
                if self.left_bool:
                    self.rotate_degrees = 0
                else:
                    self.rotate_degrees = -self.turning_speed

            if event.key == pygame.K_RCTRL:
                self.up_bool = True
                self.original_img = pygame.image.load('flying-rocket64.png')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:

                self.left_bool = False
                if self.right_bool:
                    self.rotate_degrees = -self.turning_speed
                else:
                    self.rotate_degrees = 0

            if event.key == pygame.K_RIGHT:
                self.right_bool = False
                if self.left_bool:
                    self.rotate_degrees = self.turning_speed
                else:
                    self.rotate_degrees = 0

            if event.key == pygame.K_RCTRL:
                self.up_bool = False
                self.original_img = pygame.image.load('flying-rocket64_expertly_edited.png')

            if event.key == pygame.K_SPACE:
                x, y = self.rect.center
                self.lasers.add(Laser(x, y, self.rotate_degrees_total))
