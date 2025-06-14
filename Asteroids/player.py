import math
import pygame
import asteroidgame
import laser


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, speed_increase, name, picture):
        super().__init__()

        self.player_id = player_id
        self.original_img = pygame.transform.scale(picture, (64, 64))

        self.image = self.original_img
        self.rect = self.original_img.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # position variables
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.player_w, self.player_h = self.image.get_size()

        # movement variables
        self.speed = 300 + speed_increase
        self.acceleration = self.speed*3
        self.velocity = [0.00, 0.00]
        self.top_speed = self.speed
        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5
        self.immune_to_damage = False
        self.time_at_lost_life = 0
        self.blink_duration = 100
        self.blinking = False
        self.counter = 1
        self.time = None
        self.time_set = False

        self.name = name
        # valjda je ovako
        if player_id == 1:
            self.player_x = self.screen_w/2 - self.player_w - 50
            self.player_y = self.screen_h/2 - self.player_h

        if player_id == 2:
            self.player_x = self.screen_w/2 - self.player_w
            self.player_y = self.screen_h/2 - self.player_h

        if player_id == 3:
            self.player_x = self.screen_w / 2 - self.player_w - 50
            self.player_y = self.screen_h / 2 - self.player_h + 50

        if player_id == 4:
            self.player_x = self.screen_w / 2 - self.player_w
            self.player_y = self.screen_h / 2 - self.player_h + 50

        self.rect = self.original_img.get_rect(center=(self.player_x, self.player_y))

        # keys pressed
        self.up_bool = False
        self.right_bool = False
        self.left_bool = False

        self.lives = 3
        self.points = 0

        thrust_key = rotate_left_key = rotate_right_key = fire_key = None

        # setup input map
        if self.player_id == 1:
            self.thrust_key             = pygame.K_UP
            self.rotate_left_key        = pygame.K_LEFT
            self.rotate_right_key       = pygame.K_RIGHT
            self.fire_key               = pygame.K_RCTRL
        elif self.player_id == 2:
            self.thrust_key             = pygame.K_w
            self.rotate_left_key        = pygame.K_a
            self.rotate_right_key       = pygame.K_d
            self.fire_key               = pygame.K_LCTRL
        elif self.player_id == 3:
            self.thrust_key             = pygame.K_KP8
            self.rotate_left_key        = pygame.K_KP4
            self.rotate_right_key       = pygame.K_KP6
            self.fire_key               = pygame.K_KP0
        elif self.player_id == 4:
            self.thrust_key             = pygame.K_i
            self.rotate_left_key        = pygame.K_j
            self.rotate_right_key       = pygame.K_l
            self.fire_key               = pygame.K_RALT

    def rotate(self):
        self.rotate_degrees_total += self.rotate_degrees
        self.rotate_degrees_total %= 360
        self.image = pygame.transform.rotate(self.original_img, self.rotate_degrees_total)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def thrust(self):
        # also dont know why 270
        rads = math.radians(self.rotate_degrees_total + 270)

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
        x -= self.velocity[0]
        y += self.velocity[1]

        # change position
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        input_manager = asteroidgame.AsteroidGame.input_manager

        self.up_bool = input_manager.get_key(self.thrust_key)
        self.left_bool = input_manager.get_key(self.rotate_left_key)
        self.right_bool = input_manager.get_key(self.rotate_right_key)

        # handle rotation speed
        if self.left_bool and not self.right_bool:
            self.rotate_degrees = self.turning_speed
        elif self.right_bool and not self.left_bool:
            self.rotate_degrees = -self.turning_speed
        else:
            self.rotate_degrees = 0

        # handle shooting
        if input_manager.get_key_down(self.fire_key):
            args[0].add(laser.Laser(self))

    def restrict_speed(self):
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj)
            self.velocity[0] = self.top_speed*math.cos(angle)
            self.velocity[1] = self.top_speed*math.sin(angle)

    def move(self):
        # handle player wraping on edges
        x, y = self.rect.center

        # left edge
        if x < -self.player_w / 2:
            x = self.screen_w + self.player_w / 2
        # right edge
        elif x > self.screen_w + self.player_w / 2:
            x = -self.player_w / 2

        # top edge
        if y < -self.player_h / 2:
            y = self.screen_h + self.player_h / 2
        # bottom edge
        elif y > self.screen_h + self.player_h / 2:
            y = -self.player_h / 2

        self.rect.center = (x, y)

        self.rotate()
        self.thrust()

    def draw(self, screen):
        if self.immune_to_damage:
            if not self.time_set:
                self.time = pygame.time.get_ticks()
                self.time_set = True
            if (pygame.time.get_ticks() - self.time) >= self.blink_duration * self.counter:
                self.counter += 1
                self.blinking = not self.blinking

        if not self.blinking:
            screen.blit(self.image, self.rect)

        if asteroidgame.AsteroidGame.debug:
            pygame.draw.rect(pygame.display.get_surface(), (150, 0, 30), self.rect, 1)

            line_origin = self.rect.center
            line_end = (self.rect.center[0] + self.velocity[0] * 10, self.rect.center[1] + self.velocity[1] * 10)

            pygame.draw.line(pygame.display.get_surface(), (150, 0, 30), line_origin, line_end)

    def clean(self):
        # movement variables
        self.velocity = [0.0, 0.0]
        self.rotate_degrees_total = 0
        self.immune_to_damage = False
        self.time_at_lost_life = 0
        self.counter = 1
        self.time = None
        self.time_set = False
        self.player_x = self.screen_w / 2 - self.player_w - 50
        self.player_y = self.screen_h / 2 - self.player_h
        self.lives = 3
        self.points = 0

    def cleanfornextlevel(self):
        self.velocity = [0.0, 0.0]
        self.rotate_degrees_total = 0
        self.immune_to_damage = False
        self.time_at_lost_life = 0
        self.counter = 1
        self.time = None
        self.time_set = False
        self.player_x = self.screen_w / 2 - self.player_w - 50
        self.player_y = self.screen_h / 2 - self.player_h
        self.lives = 3
