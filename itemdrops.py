import pygame
import random
from constants import *
from circleshape import CircleShape
from boonfunctions import *
from banefunctions import *


class ItemDrops(CircleShape):
    def __init__(self, x, y, radius, type):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x,y)
        self.radius = radius
        self.type = type
        self.effect = self.get_effect()
        self.color = (0,200,0) if self.type == "boon" else (200,0,0)
        self.message = ""
        self.expire_time = 0
        self.undo_effect = None
        

    def get_effect(self):
        banes = [
            more_asteroids,
            reduce_speed,
            shoot_slower,
            slow_turning,
            increased_neg_item_drop
        ]
    
        boons = [
            double_score_multiplier,
            speed_boost,
            shoot_faster,
            extra_life,
            bigger_bullets,
            increased_pos_item_drop
        ]
        if self.type == "boon":
            return random.choice(boons)
        else:
            return random.choice(banes)

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, (self.radius // 2))

    def apply_effect(self, player, game):
        self.player = player
        self.game = game
        effect_result = self.effect(player,game)
        if effect_result:
            self.message, self.undo_effect = effect_result  # Call the effect method
            self.expire_time = pygame.time.get_ticks() + 10000
        else:
            print("No effect to apply.")

    def draw_text(self, screen, text, x, y, color=(255, 255, 255)):
        if self.message and not self.is_message_expired():
            font = pygame.font.SysFont(None, 32)  # You can change the font and size
            text_surface = font.render(self.message, True, (0,100,255))
            screen.blit(text_surface, (x, y))

