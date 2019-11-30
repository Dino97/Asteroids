import sys
import pygame
from player import Player

def main_menu_screen(self, screen):
    screen.blit(pygame.transform.smoothscale(pygame.image.load('idiote.png'), (self.screen_w, self.screen_h)), [0, 0])
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
    screen.blit(text_surface, text_surface_rect)
    text_surface = my_font.render("MULTIPLAYER", False, (0, 0, 0))
    text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 470))
    screen.blit(text_surface, text_surface_rect)
    text_surface = my_font.render("QUIT", False, (0, 0, 0))
    text_surface_rect = text_surface.get_rect(center=(self.screen_w / 2, 540))
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