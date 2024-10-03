from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = SHOT_COLOR
    

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,  self.position, self.radius, 2)
        

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position[0] > (SCREEN_HEIGHT * 1.5) or self.position[0] < (SCREEN_HEIGHT * -1.5):
            self.kill()
        if self.position[1] > (SCREEN_WIDTH * 1.5) or self.position[0] < (SCREEN_WIDTH * -1.5):
            self.kill()  