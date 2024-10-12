import pygame
import random
from constants import *
from circleshape import CircleShape
from helpfulfunctions import *
from itemdrops import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, game):
        super().__init__(x, y, radius)
        self.game = game
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),  self.position, self.radius, 2)
        

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, player, hit_player):
        # Sounds
        asteroid_channel = pygame.mixer.Channel(2)
        asteroid_explode_sound = pygame.mixer.Sound(ASTEROID_EXPLOSION)
        asteroid_channel.play(asteroid_explode_sound)
        asteroid_explode_sound.set_volume(self.game.sound_effect_volume*3)

        asteroidPoints = self.game.asteroid_points
        if self.radius <= self.game.asteroid_min_radius:
            asteroidPoints *= 3
        elif self. radius <= self.game.asteroid_min_radius * 2:
            asteroidPoints *= 2

        self.kill()

        if hit_player:
            return asteroidPoints
        
        item_drop = check_item_drop(self.game)
        if item_drop is not None:
            item = ItemDrops(self.position[0], self.position[1], self.game.item_drop_radius, item_drop)

        if self.radius <=  self.game.asteroid_min_radius:
            return asteroidPoints
        
        newAngle = random.uniform(20, 50)
        Velocity1 = self.velocity.rotate(newAngle)
        Velocity2 = self.velocity.rotate(-newAngle)

        newRadius = self.radius - self.game.asteroid_min_radius

        lAsteroid = Asteroid(self.position.x, self.position.y, newRadius, self.game)
        lAsteroid.velocity = Velocity1 * 1.2
        rAsteroid = Asteroid(self.position.x, self.position.y, newRadius, self.game)
        rAsteroid.velocity = Velocity2 * 1.2
        return asteroidPoints