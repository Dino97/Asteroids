import math
import sys
import screens
import pygame
from player import Player
from laser import Laser
from asteroid import Asteroid


class AsteroidGame:
    def __init__(self):
        super().__init__()

        self.player_pictures = [pygame.image.load("spaceships/one.png"), pygame.image.load("spaceships/two.png"), pygame.image.load("spaceships/three.png"), pygame.image.load("spaceships/four.png")]
        self.player_pictures_b = [pygame.image.load("spaceships/one.png"), pygame.image.load("spaceships/two.png"),
                                pygame.image.load("spaceships/three.png"), pygame.image.load("spaceships/four.png")]
        # game assets - pocetni nivo, igraci, asteroidi, laseri
        self.level = 0
        self.players = pygame.sprite.Group()
        self.players_dead = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.num_of_asteroids = 0
        # self.backgrounds = None  # se ucitava iz fajlova kao niz imageloadova
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()

        self.game_over = False
        self.level_complete = True
        self.game_started = False
        # timed events
        self.asteroid_spawn = pygame.USEREVENT + 1
        self.move_sprites = pygame.USEREVENT + 2
        self.increase_asteroid_speed = 0
        self.increase_player_speed = 0
        self.current_background = pygame.transform.smoothscale(pygame.image.load('background_level_1.png'), (self.screen_w, self.screen_h))

        self.backgrounds = None
        self.players_immune_to_damage_duration = 3000
        self.time_between_levels = 3000

        self.completed_pause = False
        self.counter = 0
        self.game_pause = False

        self.main_menu = True
        self.player_icon = pygame.transform.smoothscale(pygame.image.load('galaga.png'), (64, 48))
        self.choose_your_own_player = False
        self.player_name = ""
        self.player_name_chosen = False
        self.player_color = ""
        self.player_color_chosen = False

    def play(self, screen):
        if self.main_menu:
            screens.main_menu_screen(self, screen)
            return True

        if self.choose_your_own_player:
            screens.choose_your_own_player_screen(self, screen)
            return True

        if self.game_over:
            screens.over_screen(self, screen)
            return True

        if not self.game_started:
            self.start_game(screen)
            return True

        #dodala sam u start_level() metodi promenu da se zapravo menja level_complete

        if self.level_complete and not self.completed_pause:
            self.start_level()
            return True

        screen.blit(self.current_background, [0, 0])
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == self.asteroid_spawn:
                self.spawn_asteroids()
            if event.type == self.move_sprites:
                self.move_all_sprites()
            self.listen_to_keys(event, self.players.sprites()[0])  # zasad samo jedan igrac posto tek kad napravimo mrezno sa vise igraca

        self.determine_collides()
        #if not self.game_pause:
            #self.move_all_sprites()
        self.draw_all_sprites(screen)
        self.draw_scores_and_lives(screen)
        self.check_game_state()
        if self.completed_pause:
            screens.level_clear_and_complete_screen(self, screen)

        return True

    def start_game(self, screen):

        self.level = 1
        self.game_started = True
        # move self.players.add(Player(1, 0))
        self.asteroids.empty()
        self.lasers.empty()
        self.num_of_asteroids = 10
        self.start_level()
        self.game_over = False

    def check_game_state(self):
        for player in self.players.sprites():
            if player.immune_to_damage:
                if (pygame.time.get_ticks() - player.time_at_lost_life) >= self.players_immune_to_damage_duration:
                    player.immune_to_damage = False
                    player.blinking = False

        if len(self.players.sprites()) == 0:
            self.game_over = True

        if len(self.asteroids.sprites()) == 0:
            self.level_complete = True
            if not self.completed_pause:
                self.time = pygame.time.get_ticks()
            self.completed_pause = True


        self.counter = 0

    def draw_all_sprites(self, screen):

        for player in self.players.sprites():
            player.draw(screen) # svaki igrac sebe ogranici da ne izadje

        for asteroid in self.asteroids.sprites():
            # make bounce logic
            asteroid.draw(screen)

        for laser in self.lasers.sprites():
            x, y = laser.rect.center
            if x < 0 or x > self.screen_w or y < 0 or y > self.screen_h:
                laser.kill()
            laser.draw(screen)

    def move_all_sprites(self):
        for player in self.players.sprites():
            player.move() # svaki igrac sebe ogranici da ne izadje

        for asteroid in self.asteroids.sprites():
            # make bounce logic
            asteroid.move()

        for laser in self.lasers.sprites():
            laser.move()

    # pocetak svakog nivoa, ovde ce se hendlovati promena nivoa i brzine itd
    def start_level(self):
        self.level = self.level + 1  # treba da se ubaci mod 25 za infinite loop
        self.num_of_asteroids = 10
        # background = self.backgrounds(self.level)

        self.spawn_asteroids()
        # da se ne bi asteroidi spawnovali u beskonacno nego samo na pocetku nivoa
        for player in self.players.sprites():
            player.cleanfornextlevel()
        self.level_complete = False

        self.increase_asteroid_speed = self.level * 50
        self.increase_player_speed = self.level * 50
        pygame.time.set_timer(self.asteroid_spawn, 1000)
        pygame.time.set_timer(self.move_sprites, 35)

    def spawn_asteroids(self):
        # promeni iz if u when da ne bi spawnovao samo jedan ako se iskljucuje event

        if self.num_of_asteroids > 0 and not self.game_pause:
            self.asteroids.add(Asteroid(self.players.sprites()[0],self.increase_asteroid_speed))
            self.num_of_asteroids -= 1

    def draw_scores_and_lives(self, screen):
        for player in self.players.sprites():
            my_font = pygame.font.SysFont('Vera', 30)
            text_surface = my_font.render(str(player.points), False, (0, 0, 0))
            if player.player_id == 1:
                screen.blit(text_surface, (0, 0))
                for x in range(player.lives):
                    screen.blit(pygame.transform.rotate(player.original_img, 40), (0 + 50*x, 50))
            if player.player_id == 2:
                screen.blit(text_surface, (0, self.screen_w - 100))
            if player.player_id == 3:
                screen.blit(text_surface, (self.screen_h - 100, 0))
            if player.player_id == 4:
                screen.blit(text_surface, (self.screen_h - 100, self.screen_w - 100))

    def determine_collides(self):
        for player in self.players.sprites():
            if pygame.sprite.spritecollideany(player, self.asteroids, pygame.sprite.collide_mask) is not None:
                if player.immune_to_damage:
                    continue
                if player.lives == 1:
                    self.players.remove(player)
                    self.players_dead.add(player)
                else:
                    player.lives -= 1
                    player.immune_to_damage = True
                    player.time_at_lost_life = pygame.time.get_ticks()

        collided_units = pygame.sprite.groupcollide(self.lasers, self.asteroids, 1, 1, pygame.sprite.collide_mask)
        if collided_units is not None:
            for laser, asteroid in collided_units.items():
                if asteroid[0].points > 100:
                    asteroid[0].death(asteroid[0], self.asteroids)
                for player in self.players.sprites():
                    if player.player_id == laser.player_id:
                        player.points += asteroid[0].points

    def listen_to_keys(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game_pause = not self.game_pause
            if event.key == pygame.K_LEFT:
                player.left_bool = True
                if player.right_bool:
                    player.rotate_degrees = 0
                else:
                    player.rotate_degrees = player.turning_speed

            if event.key == pygame.K_RIGHT:
                player.right_bool = True
                if player.left_bool:
                    player.rotate_degrees = 0
                else:
                    player.rotate_degrees = -player.turning_speed

            if event.key == pygame.K_RCTRL:
                player.up_bool = True
                #player.original_img = pygame.image.load('flying-rocket64.png')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:

                player.left_bool = False
                if player.right_bool:
                    player.rotate_degrees = -player.turning_speed
                else:
                    player.rotate_degrees = 0

            if event.key == pygame.K_RIGHT:
                player.right_bool = False
                if player.left_bool:
                    player.rotate_degrees = player.turning_speed
                else:
                    player.rotate_degrees = 0

            if event.key == pygame.K_RCTRL:
                player.up_bool = False
                #player.original_img = pygame.image.load('flying-rocket64_expertly_edited.png')

            if event.key == pygame.K_SPACE:
                x, y = player.rect.center
                self.lasers.add(Laser(player))


