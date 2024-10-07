import pygame
import random
from constants import *
from circleshape import CircleShape
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),  self.position, self.radius, 2)
        

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        asteroidPoints = BASE_ASTEROID_POINTS
        self.kill()
        if self.radius <=  ASTEROID_MIN_RADIUS:
            return asteroidPoints
        
        newAngle = random.uniform(20, 50)
        Velocity1 = self.velocity.rotate(newAngle)
        Velocity2 = self.velocity.rotate(-newAngle)

        newRadius = self.radius - ASTEROID_MIN_RADIUS
        if newRadius <= ASTEROID_MIN_RADIUS:
            asteroidPoints -= 5
        else:
            asteroidPoints -= 10


        lAsteroid = Asteroid(self.position.x, self.position.y, newRadius)
        lAsteroid.velocity = Velocity1 * 1.2
        rAsteroid = Asteroid(self.position.x, self.position.y, newRadius)
        rAsteroid.velocity = Velocity2 * 1.2
        return asteroidPoints