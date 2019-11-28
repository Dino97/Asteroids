import math
import sys

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
    # inicijalizacija igre, resetovanje poena

    def start_game(self, screen):

        self.level = 1
        self.game_started = True
        #move self.players.add(Player(1, 0))
        self.asteroids.empty()
        self.lasers.empty()
        self.num_of_asteroids = 10
        self.start_level()
        self.game_over = False

    def main_menu_screen(self, screen):

        screen.blit(pygame.transform.smoothscale(pygame.image.load('idiote.png'), (self.screen_w, self.screen_h)),[0,0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.counter <= 1:
                        self.counter += 1
                if event.key == pygame.K_UP:
                    if self.counter > 0:
                        self.counter -= 1
                if event.key == pygame.K_RETURN:
                    if self.counter == 0:
                        self.main_menu = False
                        self.choose_your_own_player = True
                    if self.counter == 1:
                        continue
                    if self.counter == 2:
                        pygame.quit()
                        sys.exit()

        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 60)
        text_surface = my_font.render("SINGLE PLAYER", False, (0, 0, 0))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 400))
        screen.blit(text_surface,text_surface_rect)
        text_surface = my_font.render("MULTIPLAYER", False, (0, 0, 0))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 470))
        screen.blit(text_surface, text_surface_rect)
        text_surface = my_font.render("QUIT", False, (0, 0, 0))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 540))
        screen.blit(text_surface, text_surface_rect)
        player_icon = pygame.transform.smoothscale(pygame.transform.rotate(self.player_icon, -90), (32, 32))
        position = self.screen_w/2
        if self.counter < 2:
            position = self.screen_w/2 - 250
        else:
           position = self.screen_w/2 - 100
        player_icon_rect = player_icon.get_rect(center=(position, 400 + self.counter * 70))
        screen.blit(player_icon, player_icon_rect)

    def choose_your_own_player_screen(self, screen):
        screen.blit(pygame.transform.smoothscale(pygame.image.load('idiote.png'), (self.screen_w, self.screen_h)),
                    [0, 0])
        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 20)
        text_surface = my_font.render("ENTER", False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, self.screen_h - 30))
        screen.blit(text_surface, text_surface_rect)
        if not self.player_name_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name != "":
                            self.player_name = self.player_name[:-1]
                            self.player_name_chosen = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += chr(event.key)
            my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 40)
            text_surface = my_font.render("PLAYER NAME", False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(topright=(self.screen_w / 2 , self.screen_h / 2))
            screen.blit(text_surface, text_surface_rect)
            text_surface = my_font.render(self.player_name , False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(topleft=(self.screen_w / 2 + 20, self.screen_h / 2))
            screen.blit(text_surface, text_surface_rect)
        if not self.player_color_chosen and self.player_name_chosen:
            first = self.player_pictures[0]
            second = self.player_pictures[1]
            third = self.player_pictures[2]
            fourth = self.player_pictures[3]
            first_b = self.player_pictures_b[0]
            second_b = self.player_pictures_b[1]
            third_b = self.player_pictures_b[2]
            fourth_b = self.player_pictures_b[3]
            pygame.draw.rect(first_b, (255, 0, 0), first_b.get_rect(), 3)
            pygame.draw.rect(second_b, (255, 0, 0), second_b.get_rect(), 3)
            pygame.draw.rect(third_b, (255, 0, 0), third_b.get_rect(), 3)
            pygame.draw.rect(fourth_b, (255, 0, 0), fourth_b.get_rect(), 3)
            if self.counter == 0:
                screen.blit(first_b, first_b.get_rect(topleft=(self.screen_w / 2 - 64, self.screen_h / 2 - 64)))
            else:
                screen.blit(first, first.get_rect(topleft=(self.screen_w / 2 - 64, self.screen_h / 2 - 64)))
            if self.counter == 1:
                screen.blit(second_b, second.get_rect(topleft=(self.screen_w / 2, self.screen_h / 2 - 64)))
            else:
                screen.blit(second, second.get_rect(topleft=(self.screen_w / 2, self.screen_h / 2 - 64)))
            if self.counter == 2:
                screen.blit(third_b, third.get_rect(topleft=(self.screen_w / 2 - 64, self.screen_h / 2)))
            else:
                screen.blit(third, third.get_rect(topleft=(self.screen_w / 2 - 64, self.screen_h / 2)))
            if self.counter == 3:
                screen.blit(fourth_b, fourth.get_rect(topleft=(self.screen_w / 2 , self.screen_h / 2)))
            else:
                screen.blit(fourth, fourth.get_rect(topleft=(self.screen_w / 2 , self.screen_h / 2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.player_color = self.player_pictures[self.counter]
                        self.player_color_chosen = True
                        self.choose_your_own_player = False
                        self.players.add(Player(1, 0, self.player_name, self.player_color))
                    if event.key == pygame.K_LEFT:
                        if self.counter == 1:
                            self.counter = 0
                        if self.counter == 3:
                            self.counter = 2
                    if event.key == pygame.K_RIGHT:
                        if self.counter == 0:
                            self.counter = 1
                        if self.counter == 2:
                            self.counter = 3
                    if event.key == pygame.K_UP:
                        if self.counter == 2:
                            self.counter = 0
                        if self.counter == 3:
                            self.counter = 1
                    if event.key == pygame.K_DOWN:
                        if self.counter == 0:
                            self.counter = 2
                        if self.counter == 1:
                            self.counter = 3

    def play(self, screen):
        if self.main_menu:
            self.main_menu_screen(screen)
            return True

        if self.choose_your_own_player:
            self.choose_your_own_player_screen(screen)
            return True

        if self.completed_pause:
            self.level_clear_and_complete_screen(screen)
            return True

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
            if event.type == self.move_sprites:
                self.move_all_sprites()
            self.listen_to_keys(event, self.players.sprites()[0])  # zasad samo jedan igrac posto tek kad napravimo mrezno sa vise igraca

        self.determine_collides()
        #if not self.game_pause:
            #self.move_all_sprites()
        self.draw_all_sprites(screen)
        self.draw_scores_and_lives(screen)
        self.check_game_state()
        return True

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
            self.completed_pause = True
            self.time = pygame.time.get_ticks()

        self.counter = 0

    def level_clear_and_complete_screen(self,screen):
        latest_time = pygame.time.get_ticks()
        if latest_time - self.time <= 3000:
            my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 40)
            text_surface = my_font.render("LEVEL CLEARED", False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, self.screen_h/2))
            screen.blit(text_surface, text_surface_rect)
        elif latest_time - self.time <= 6000:
            screen.fill((169,169,169))
            my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 60)
            text_surface = my_font.render("LEVEL " + str(self.level), False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, self.screen_h/2))
            screen.blit(text_surface, text_surface_rect)
        else:
            self.completed_pause = False

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
            player.lives = 3
        self.level_complete = False

        self.increase_asteroid_speed += 50
        self.increase_player_speed += 50
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

    def over_screen(self, screen):
        screen.fill((0, 0, 0))

        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 100)
        text_surface = my_font.render("GAME OVER", False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w/2, 50))
        screen.blit(text_surface, text_surface_rect)
        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 50)
        text_surface = my_font.render("SCORES", False, (255,255, 255))
        text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 100))
        screen.blit(text_surface, text_surface_rect)
        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 50)
        for player in self.players_dead.sprites():
            text_surface = my_font.render(str(player.points), False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(topright=(self.screen_w / 2 - 20, 100 + 50 * player.player_id))
            screen.blit(text_surface, text_surface_rect)
            text_surface = my_font.render(player.name, False, (255, 255, 255))
            text_surface_rect = text_surface.get_rect(topleft=(self.screen_w / 2 + 10, 100 + 50 * player.player_id))
            screen.blit(text_surface, text_surface_rect)
            surface = pygame.transform.rotate(player.original_img, -30)
            surface_rect = surface.get_rect(topleft = (self.screen_w/2 - 160, 100 + 50 * player.player_id))
            screen.blit(surface, surface_rect)

        screen.blit(pygame.transform.smoothscale(pygame.transform.rotate(self.players_dead.sprites()[0].original_img, -90), (32,32)),(220, 310 + 100 * self.counter))
        text_surface = my_font.render("TRY AGAIN", False, (255, 255, 255))
        screen.blit(text_surface, (250, 300))
        text_surface = my_font.render("MAIN MENU", False, (255, 255, 255))
        screen.blit(text_surface, (250, 400))
        text_surface = my_font.render("QUIT", False, (255, 255, 255))
        screen.blit(text_surface, (250, 500))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.counter < 2:
                        self.counter += 1
                if event.key == pygame.K_UP:
                    if self.counter > 0:
                        self.counter -= 1
                if event.key == pygame.K_RETURN:
                    if self.counter == 0:
                        self.game_over = False
                        self.game_started = False
                        self.players_dead.sprites()[0].clean()
                        self.players.add(self.players_dead.sprites()[0])
                        self.players_dead.empty()
                    if self.counter == 1:
                        self.players.empty()
                        self.game_over = False
                        self.main_menu = True
                        self.counter = 0
                    if self.counter == 2:
                        pygame.quit()
                        sys.exit()
