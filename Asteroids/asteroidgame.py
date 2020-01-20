import math
import sys
import screens
import pygame
import random
from player import Player
from laser import Laser
from asteroid import Asteroid
from scoremanager import ScoreManager
from inputmanager import InputManager
from supernova import Supernova

BATTLESHIP1_PATH = "images/spaceships/battleship1.png"
BATTLESHIP2_PATH = "images/spaceships/battleship2.png"
BATTLESHIP3_PATH = "images/spaceships/battleship3.png"
BATTLESHIP4_PATH = "images/spaceships/battleship4.png"


class AsteroidGame:
    debug = False
    input_manager = InputManager()

    STARTING_ASTEROIDS = 3

    def __init__(self):

        self.player_pictures = [
            pygame.image.load(BATTLESHIP1_PATH),
            pygame.image.load(BATTLESHIP2_PATH),
            pygame.image.load(BATTLESHIP3_PATH),
            pygame.image.load(BATTLESHIP4_PATH)]

        self.number_of_players = 1
        self.number_of_players_set = False

        # game assets - pocetni nivo, igraci, asteroidi, laseri
        self.level = 0
        self.num_of_asteroids = 0
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()

        self.players = pygame.sprite.Group()
        self.players_dead = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.game_over = False
        self.level_complete = True
        self.game_started = False

        # timed events
        self.asteroid_spawn = pygame.USEREVENT + 1
        self.move_sprites = pygame.USEREVENT + 2
        self.supernova_event = pygame.USEREVENT + 3
        self.increase_asteroid_speed = 0
        self.increase_player_speed = 0

        self.num_background = str(1)
        self.background = pygame.image.load('images/background_level_' + self.num_background + '.png')
        self.current_background = pygame.transform.scale(self.background, (self.screen_w, self.screen_h))

        self.backgrounds = None
        self.players_immune_to_damage_duration = 3000
        self.time_between_levels = 3000

        self.completed_pause = False
        self.counter = 0
        self.game_pause = False

        self.main_menu = True
        self.player_icon = pygame.transform.scale(pygame.image.load('images/galaga.png'), (64, 48))
        self.choose_your_own_player = False
        self.player_name = ""
        self.player_names = ["", "", "", ""]
        self.player_colors = [-1, -1, -1, -1]

        self.supernova = None

        self.score_manager = None

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

        # dodala sam u start_level() metodi promenu da se zapravo menja level_complete
        if self.level_complete and not self.completed_pause:
            self.start_level()
            return True

        screen.blit(self.current_background, [0, 0])

        AsteroidGame.input_manager.poll_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == self.asteroid_spawn:
                self.spawn_asteroids()
            elif event.type == self.move_sprites:
                self._move_all_sprites()
            elif event.type == self.supernova_event:
                random_pos = (random.randint(0, self.screen_w), random.randint(0, self.screen_h))
                self.supernova = Supernova(random_pos)

        self._determine_collides()
        self._draw_all_sprites(screen)
        self._draw_scores_and_lives(screen)
        self.check_game_state()

        if self.completed_pause:
            screens.level_clear_and_complete_screen(self, screen)

        self.players.update(self.lasers)
        self.asteroids.update()

        # if supernova exists, update it and check for explosion
        if self.supernova is not None:
            self.supernova.update(screen)

            if pygame.time.get_ticks() - self.supernova.spawn_time > Supernova.PULSE_DURATION:
                players_in_supernova = pygame.sprite.spritecollide(self.supernova, self.players, False)

                # knockback for players
                for player in players_in_supernova:
                    sn_center = self.supernova.rect.center
                    pl_center = player.rect.center
                    direction = pygame.math.Vector2(sn_center[0] - pl_center[0], sn_center[1] - pl_center[1])
                    direction = direction.normalize()
                    player.velocity = [player.velocity[0] + 10 * direction.x, player.velocity[1] + -10 * direction.y]

                self.supernova = None

        return True

    def start_game(self, screen):
        self.level = 1
        self.asteroids.empty()
        self.lasers.empty()
        self.game_over = False
        self.game_started = True
        self.start_level()

        self.score_manager = ScoreManager()
        self.score_manager.start()

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

    def _draw_all_sprites(self, screen):

        for player in self.players.sprites():
            player.draw(screen)  # svaki igrac sebe ogranici da ne izadje

        for asteroid in self.asteroids.sprites():
            # make bounce logic
            asteroid.draw(screen)

        for laser in self.lasers.sprites():
            x, y = laser.rect.center
            if x < 0 or x > self.screen_w or y < 0 or y > self.screen_h:
                laser.kill()
            laser.draw(screen)

    def _move_all_sprites(self):
        for player in self.players.sprites():
            player.move()

        for asteroid in self.asteroids.sprites():
            asteroid.move()

        for laser in self.lasers.sprites():
            laser.move()

    # pocetak svakog nivoa, ovde ce se hendlovati promena nivoa i brzine itd
    def start_level(self):
        self.level += 1  # treba da se ubaci mod 25 za infinite loop
        self.num_background = str(self.level % 2 + 1)
        self.background = pygame.image.load('images/background_level_'+self.num_background+'.png')
        self.current_background = pygame.transform.scale(self.background, (self.screen_w, self.screen_h))

        self.num_of_asteroids = AsteroidGame.STARTING_ASTEROIDS + self.level // 2
        self.supernova = None

        self.spawn_asteroids()
        # da se ne bi asteroidi spawnovali u beskonacno nego samo na pocetku nivoa
        for player in self.players.sprites():
            player.cleanfornextlevel()
            player.speed += self.level * 500
            player.turning_speed *= 1.1
        self.level_complete = False

        self.increase_asteroid_speed = self.level * 50
        self.increase_player_speed = self.level * 50
        pygame.time.set_timer(self.asteroid_spawn, 1000)
        pygame.time.set_timer(self.move_sprites, 35)
        pygame.time.set_timer(self.supernova_event, random.randint(5000, 10000))

    def spawn_asteroids(self):
        # promeni iz if u when da ne bi spawnovao samo jedan ako se iskljucuje event

        if self.num_of_asteroids > 0 and not self.game_pause:
            self.asteroids.add(Asteroid(self.players.sprites()[0], self.increase_asteroid_speed))
            self.num_of_asteroids -= 1

    def _draw_scores_and_lives(self, screen):
        ship_colors_rgb = [
            (69, 79, 110),
            (233, 161, 74),
            (151, 189, 37),
            (140, 37, 178)
        ]

        my_font = pygame.font.SysFont('Vera', 30)

        for player in self.players.sprites():
            serial_num = player.player_id - 1

            label_text = player.name + ": " + str(self.score_manager.get_score(serial_num))
            text_surface = my_font.render(label_text, False, ship_colors_rgb[serial_num])
            section_height = text_surface.get_height() + self.player_pictures[serial_num].get_height()
            screen.blit(text_surface, (0, serial_num * section_height))

            for x in range(player.lives):
                player_picture_id = self.player_colors[serial_num]
                screen.blit(self.player_pictures[player_picture_id], (32*x, serial_num * section_height + text_surface.get_height()))

    def _determine_collides(self):
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

                self.score_manager.add_score(laser.player_id - 1, asteroid[0].points)
