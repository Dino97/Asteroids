import pygame
from asteroidgame import AsteroidGame

from engine.game import Game
from engine.gameobject import GameObject
from engine.component import Component

# Initialize
pygame.init()
pygame.font.init()

# game_time

game_clock = pygame.time.Clock()

# create screen
screen = pygame.display.set_mode((900, 700))
asteroid_game = AsteroidGame()


# set icon
icon = pygame.image.load('images/flying-rocket.png')
pygame.display.set_icon(icon)

# set window name
pygame.display.set_caption("Asteroids")

running = True
while running:
    # background color - needs to be first

    #screen.fill((128, 128, 128))

    # main loop with events
    #running = asteroid_game.play(screen)

    # always update it
    #pygame.display.update()

    #game_clock.tick(60)

    game = Game()

    comp = Component()
    comp.name = "Sprite"

    go = GameObject()
    go.add_component(comp)

    game.loadedscene.gameobjects.append(go)

    game.start()
