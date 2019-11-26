import math
import pygame
from player import Player
from laser import Laser
from asteroid import Asteroid


class AsteroidGame:
    def __init__(self):
        super().__init__()

        # game assets - pocetni nivo, igraci, asteroidi, laseri
        self.level = 0
        self.players = pygame.sprite.Group()
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

        self.increase_asteroid_speed = 0
        self.increase_player_speed = 0
        self.current_background = pygame.image.load('background_level_1.png').convert()
        self.backgrounds = None
    # inicijalizacija igre, resetovanje poena

    def start_game(self, screen):
        self.level = 1
        self.game_started = True
        self.start_level()
        pygame.time.set_timer(self.asteroid_spawn, 1000)

    def over_screen(self, screen):
        screen.blit(pygame.image.load('gameover.jpg'), (0, 0))

    def play(self, screen):

        if not self.game_started:
            self.start_game(screen)

        #dodala sam u start_level() metodi promenu da se zapravo menja level_complete
        if self.level_complete:
            self.start_level()

        if self.game_over:
            self.over_screen(screen)
            return True

        screen.blit(self.current_background, [0, 0])
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == self.asteroid_spawn:
                self.spawn_asteroids()

            self.listen_to_keys(event, self.players.sprites()[0])  # zasad samo jedan igrac posto tek kad napravimo mrezno sa vise igraca

        self.determine_collides()
        self.draw_all_sprites(screen)
        self.draw_scores(screen)
        self.check_game_state()
        return True

    def check_game_state(self):
        if len(self.players.sprites()) == 0:
            self.game_over = True

        if len(self.asteroids.sprites()) == 0:
            self.level_complete = True

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

    # pocetak svakog nivoa, ovde ce se hendlovati promena nivoa i brzine itd
    def start_level(self):
        self.level = self.level + 1  # treba da se ubaci mod 25 za infinite loop
        self.num_of_asteroids = 10
        #background = self.backgrounds(self.level)
        self.spawn_players()
        self.spawn_asteroids()
        # da se ne bi asteroidi spawnovali u beskonacno nego samo na pocetku nivoa
        self.level_complete = False

        self.increase_asteroid_speed += 50
        self.increase_player_speed += 50

    def spawn_players(self):
        # mrezno programiranje imacemo neki buffer? nzm  al zasad ovako
        self.players.add(Player(1, self.increase_player_speed))

    def spawn_asteroids(self):
        # promeni iz if u when da ne bi spawnovao samo jedan ako se iskljucuje event
        if self.num_of_asteroids > 0:
            self.asteroids.add(Asteroid(self.players.sprites()[0],self.increase_asteroid_speed))
            self.num_of_asteroids -= 1

    def draw_scores(self, screen):
        for player in self.players.sprites():
            my_font = pygame.font.SysFont('Vera', 30)
            text_surface = my_font.render(str(player.points), False, (0, 0, 0))
            if player.player_id == 1:
                screen.blit(text_surface, (0, 0))
            if player.player_id == 2:
                screen.blit(text_surface, (0, self.screen_w - 100))
            if player.player_id == 3:
                screen.blit(text_surface, (self.screen_h - 100, 0))
            if player.player_id == 4:
                screen.blit(text_surface, (self.screen_h - 100, self.screen_w - 100))

    def determine_collides(self):
        for player in self.players.sprites():
            if pygame.sprite.spritecollideany(player, self.asteroids, pygame.sprite.collide_mask) is not None:
                self.players.remove(player)

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

