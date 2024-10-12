import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.game = game
        self.edges = [
                [
                    pygame.Vector2(1, 0),
                    lambda y: pygame.Vector2(-self.game.asteroid_max_radius, y * (SCREEN_HEIGHT*1.5)),
                ],
                [
                    pygame.Vector2(-1, 0),
                    lambda y: pygame.Vector2(
                        SCREEN_WIDTH + self.game.asteroid_max_radius, y * (SCREEN_HEIGHT *1.5)
                    ),
                ],
                [
                    pygame.Vector2(0, 1),
                    lambda x: pygame.Vector2(x * (SCREEN_WIDTH * 1.5), -self.game.asteroid_max_radius),
                ],
                [
                    pygame.Vector2(0, -1),
                    lambda x: pygame.Vector2(
                        x * (SCREEN_WIDTH * 1.5), (SCREEN_HEIGHT * 1.5) + self.game.asteroid_max_radius
                    ),
                ],
            ]

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, self.game)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > self.game.asteroid_spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, self.game.asteroid_kinds)
            self.spawn(self.game.asteroid_min_radius * kind, position, velocity)