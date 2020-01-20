import pygame
from asteroidgame import AsteroidGame

if __name__ == '__main__':
    # Initialize
    pygame.init()
    pygame.font.init()

    # game_time
    game_clock = pygame.time.Clock()

    # create screen
    screen = pygame.display.set_mode((1024, 642))
    asteroid_game = AsteroidGame()

    # set icon
    icon = pygame.image.load('images/flying-rocket.png')
    pygame.display.set_icon(icon)

    # set window name
    pygame.display.set_caption("Asteroids")

    running = True
    while running:
        # background color - needs to be first
        screen.fill((128, 128, 128))

        # main loop with events
        running = asteroid_game.play(screen)

        # swap frame buffers
        pygame.display.update()

        game_clock.tick(60)
