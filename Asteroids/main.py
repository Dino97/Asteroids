import pygame
from player import Player
from asteroid import Asteroid
# Initialize
pygame.init()
pygame.font.init()

# game_time
game_clock = pygame.time.Clock()

# create screen
screen = pygame.display.set_mode((900, 700))

player = Player()
x, y = player.rect.center

# set icon
icon = pygame.image.load('flying-rocket.png')
pygame.display.set_icon(icon)

# set window name
pygame.display.set_caption("Asteroids....Okay")
pygame.time.set_timer(player.asteroid_spawn, 1000)
running = True
while running:
    # background color - needs to be first

    screen.fill((128, 128, 128))

    # main loop with events
    running = player.move(screen)

    if pygame.sprite.spritecollideany(player, player.asteroids, collided=None) is not None:
        player.is_dead = True

    s = pygame.sprite.groupcollide(player.lasers, player.asteroids, 1, 1)
    for asteroid in s.values():
        player.points += asteroid[0].points
        if asteroid[0].points > 100:
            asteroid[0].death(asteroid[0], player.asteroids)


    # always update it
    pygame.display.update()

    game_clock.tick(30)
