from engine.game import *


class PlayerController(Component):
    def __init__(self):
        super().__init__()

        # Player movement speed
        self.speed = 100
        # After how many seconds player is able to shoot again
        self.fire_cooldown = 0.5
        self._fire_cooldown_timer = 0

    def on_update(self, dt):
        transform = self.gameobject.transform

        # Movement
        if Input.is_key_down(pygame.K_RIGHT):
            transform.x += self.speed * dt
        if Input.is_key_down(pygame.K_LEFT):
            transform.x -= self.speed * dt
        if Input.is_key_down(pygame.K_UP):
            transform.y -= self.speed * dt
        if Input.is_key_down(pygame.K_DOWN):
            transform.y += self.speed * dt

        # Firing projectiles
        if Input.is_key_down(pygame.K_SPACE):
            if self._fire_cooldown_timer <= 0:
                self._fire_projectile()

        # If weapon is on cooldown, decrease cd
        if self._fire_cooldown_timer > 0:
            self._fire_cooldown_timer -= dt

    def _fire_projectile(self):
        self._fire_cooldown_timer = self.fire_cooldown

        projectile = GameObject()
        projectile.add_component(Projectile())
        projectile.add_component(Sprite(game.window, "images/laser_red.png", 10, 30))
        projectile.transform.x = self.gameobject.transform.x
        projectile.transform.y = self.gameobject.transform.y

        game.loadedscene.register_gameobject(projectile)


class Projectile(Component):
    def __init__(self):
        super().__init__()

        self.speed = 300

    def on_update(self, dt):
        self.gameobject.transform.x += self.speed * dt
        self.gameobject.transform.y += self.speed * dt


if __name__ == "__main__":
    game = Game("Asteroids", resolution=(960, 720))

    player = GameObject()
    player.add_component(PlayerController())
    player.add_component(Sprite(game.window, "images/spaceships/battleship1.png", width=64, height=64))

    game.loadedscene.register_gameobject(player)

    game.start()
