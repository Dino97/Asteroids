import sys
import pygame
from player import Player


def main_menu_screen(self, screen):
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.counter < 1:
                    self.counter += 1
            if event.key == pygame.K_UP:
                if self.counter > 0:
                    self.counter -= 1
            if event.key == pygame.K_RETURN:
                if self.counter == 0:   # Singleplayer
                    self.main_menu = False
                    self.choose_your_own_player = True
                if self.counter == 1:   # Quit
                    pygame.quit()
                    sys.exit()

    # display main menu background
    screen.blit(pygame.transform.smoothscale(pygame.image.load('images/idiote.png'), (self.screen_w, self.screen_h)), [0, 0])

    my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 60)

    # display main menu options
    text_surface = my_font.render("PLAY", False, (255, 255, 255))
    text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 400))
    screen.blit(text_surface, text_surface_rect)

    text_surface = my_font.render("QUIT", False, (255, 255, 255))
    text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 470))
    screen.blit(text_surface, text_surface_rect)

    player_icon = pygame.transform.smoothscale(pygame.transform.rotate(self.player_icon, -90), (32, 32))
    position = self.screen_w / 2

    if self.counter < 2:
        position = self.screen_w / 2 - 250
    else:
        position = self.screen_w / 2 - 100

    player_icon_rect = player_icon.get_rect(center=(position, 400 + self.counter * 70))
    screen.blit(player_icon, player_icon_rect)


def choose_your_own_player_screen(self, screen):
    screen.blit(pygame.transform.smoothscale(pygame.image.load('images/idiote.png'), (self.screen_w, self.screen_h)),
                [0, 0])

    my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 20)

    text_surface = my_font.render("ENTER", False, (255, 255, 255))
    text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, self.screen_h - 30))
    screen.blit(text_surface, text_surface_rect)

    # select number of players
    if not self.number_of_players_set:
        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 40)
        text_surface = my_font.render("SELECT NUMBER OF PLAYERS", False, (255, 255, 255))
        screen.blit(text_surface, (self.screen_w / 2 - text_surface.get_width() / 2, self.screen_h / 2))

        text_surface = my_font.render(str(self.number_of_players), False, (255, 255, 255))
        screen.blit(text_surface, (self.screen_w / 2 - text_surface.get_width() / 2, self.screen_h / 2 + 48))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.number_of_players_set = True
                if event.key == pygame.K_LEFT:
                    if self.number_of_players > 1:
                        self.number_of_players -= 1
                if event.key == pygame.K_RIGHT:
                    if self.number_of_players < 4:
                        self.number_of_players += 1
        return

    # get number of entered player names
    entered_names_cnt = 0
    for i in range(0, self.number_of_players):
        if self.player_names[i] != "":
            entered_names_cnt += 1

    # enter player names
    if entered_names_cnt < self.number_of_players:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.player_name != "":
                        self.player_names[entered_names_cnt] = self.player_name
                        self.player_name = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if chr(event.key).isalpha:
                        self.player_name += chr(event.key)

        my_font = pygame.font.Font('Fonts//ARCADECLASSIC.TTF', 40)

        text_surface = my_font.render("PLAYER " + str(entered_names_cnt + 1) + " NAME", False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(topright=(self.screen_w / 2, self.screen_h / 2))
        screen.blit(text_surface, text_surface_rect)

        text_surface = my_font.render(self.player_name, False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(topleft=(self.screen_w / 2 + 20, self.screen_h / 2))
        screen.blit(text_surface, text_surface_rect)

    # select each player ship color
    if entered_names_cnt == self.number_of_players:
        currently_selecting_player_id = 0
        for i in self.player_colors:
            if i > -1:
                currently_selecting_player_id += 1
            else:
                break

        # rects for placement of player icons and outlines on selection screen
        player_rects = [
            (self.screen_w / 2 - 48, self.screen_h / 2 - 48, 64, 64),
            (self.screen_w / 2 + 48, self.screen_h / 2 - 48, 64, 64),
            (self.screen_w / 2 - 48, self.screen_h / 2 + 48, 64, 64),
            (self.screen_w / 2 + 48, self.screen_h / 2 + 48, 64, 64)
        ]

        ship_colors_rgb = [
            (69, 79, 110),
            (233, 161, 74),
            (151, 189, 37),
            (140, 37, 178)
        ]

        for i in range(0, 4):
            # draw player icons
            screen.blit(pygame.transform.scale(self.player_pictures[i], (64, 64)), player_rects[i])

            # draw rect around selected player icons
            if i in self.player_colors:
                pygame.draw.rect(pygame.display.get_surface(), ship_colors_rgb[i], player_rects[i], 3)

                text_surface = my_font.render("P" + str(self.player_colors.index(i) + 1), False, ship_colors_rgb[i])
                screen.blit(text_surface, player_rects[i])

        # draw rect around currently selected icon
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), player_rects[self.counter], 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.counter not in self.player_colors:
                    self.player_color = self.player_pictures[self.counter]
                    self.player_colors[currently_selecting_player_id] = self.counter

                    if currently_selecting_player_id + 1 >= self.number_of_players:
                        self.choose_your_own_player = False

                    self.players.add(Player(1, currently_selecting_player_id * 100, self.player_name, self.player_color))

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

    for player in self.players_dead.sprites():
        text_surface = my_font.render(str(player.points), False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(topright=(self.screen_w / 2 - 20, 100 + 50 * player.player_id))
        screen.blit(text_surface, text_surface_rect)

        text_surface = my_font.render(player.name, False, (255, 255, 255))
        text_surface_rect = text_surface.get_rect(topleft=(self.screen_w / 2 + 10, 100 + 50 * player.player_id))
        screen.blit(text_surface, text_surface_rect)

        surface = pygame.transform.rotate(player.original_img, -30)
        surface_rect = surface.get_rect(topleft=(self.screen_w/2 - 160, 100 + 50 * player.player_id))
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
                    self.game_started = False
                    self.players_dead.sprites()[0].clean()
                    self.players.add(self.players_dead.sprites()[0])
                if self.counter == 1:
                    self.players.empty()
                    self.main_menu = True
                    self.counter = 0
                if self.counter == 2:
                    pygame.quit()
                    sys.exit()
                self.game_over = False
                self.game_started = False
                self.players_dead.empty()
                self.player_name = ""
