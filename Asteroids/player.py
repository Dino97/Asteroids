import math
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, speed_increase):
        super().__init__()

        self.player_id = player_id
        self.original_img = pygame.transform.smoothscale(pygame.image.load('galaga.jpg'), (26, 32)).convert_alpha()

        self.image = self.original_img
        self.rect = self.original_img.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # position variables
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.player_w, self.player_h = self.image.get_size()

        # movement variables
        self.speed = 700 + speed_increase
        self.acceleration = self.speed*3
        self.velocity = [0.0, 0.0]
        self.top_speed = self.speed
        self.rotate_degrees = 0
        self.rotate_degrees_total = 0
        self.turning_speed = 5

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

        # hm
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.is_dead = False
        self.points = 0

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
        self.mask = pygame.mask.from_surface(self.image)

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
        self.mask = pygame.mask.from_surface(self.image)

    def restrict_speed(self):
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj)
            self.velocity[0] = self.top_speed*math.cos(angle)
            self.velocity[1] = self.top_speed*math.sin(angle)

    def draw(self, screen):
        self.rotate()
        self.thrust()
        screen.blit(self.image, self.rect, special_flags=3)
        self.limit_exiting()




