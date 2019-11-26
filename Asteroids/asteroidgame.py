import math
import pygame


class AsteroidGame:
    def __init__(self):
        super().__init__()

        # game assets - pocetni nivo, igraci, asteroidi, laseri
        self.level = 0
        self.points = 0
        self.players = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        # self.backgrounds se ucitava iz fajlova kao niz imageloadova

    # inicijalizacija igre, resetovanje poena
    def startgame(self, screen):
        self.points = 0
        self.level = 1
        self.startlevel()

    #pocetak svakog nivoa, ovde ce se hendlovati promena nivoa i brzine itd
    def startlevel(self):
        self.level = self.level + 1  # treba da se ubaci mod 25 za infinite loop
        background = self.backgrounds(self.level)
        self.spawnasteroids()
        self.spawnplayers()

    # zamenjuje move iz player.py
    def play(self, screen):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == self.completedlevel: #event koji se trigeruje kad nema vise asteroida na polju
                self.startlevel()
            self.listen_to_keys(event) #do key stuff

        self.draw_lasers(screen) #sve ovo ide u asteroidgame
        self.draw_asteroids(screen)
        # Limit player from exiting the screen
        self.limit_exiting()
        self.draw(screen)
        return True

