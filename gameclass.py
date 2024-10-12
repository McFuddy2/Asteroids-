from constants import *
import csv

class Game:

    def __init__(self):
        self.asteroid_min_radius = BASE_ASTEROID_MIN_RADIUS
        self.asteroid_kinds = BASE_ASTEROID_KINDS
        self.asteroid_spawn_rate = BASE_ASTEROID_SPAWN_RATE
        self.asteroid_max_radius = BASE_ASTEROID_MAX_RADIUS
        self.asteroid_points = BASE_ASTEROID_POINTS

        self.player_radius = BASE_PLAYER_RADIUS
        self.player_turn_speed = BASE_PLAYER_TURN_SPEED
        self.player_movement_speed = BASE_PLAYER_SPEED
        self.player_shot_speed = BASE_PLAYER_SHOOT_SPEED
        self.player_shoot_cooldown = BASE_PLAYER_SHOOT_COOLDOWN

        self.item_drop_radius = BASE_ITEM_DROP_RADIUS
        self.pos_item_drop_chance = BASE_POS_ITEM_DROP_CHANCE
        self.neg_item_drop_chance = BASE_NEG_ITEM_DROP_CHANCE

        self.shot_radius = BASE_SHOT_RADIUS

        self.score_multiplier = BASE_SCORE_MULTIPLIER
        self.update_settings()

    def update_settings(self):
        try:
            with open('game_settings.csv', 'r', newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            if len(rows) > 1:
                # Assign values from the second row
                self.music_volume = float(rows[1][0]) 
                self.sound_effect_volume = float(rows[1][1])
            else:
                self.music_volume = 0.5
                self.sound_effect_volume = .15

        except FileNotFoundError:
            print("Error: game_settings.csv file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
