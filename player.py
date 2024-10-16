from circleshape import *
from constants import *
from shots import *
import csv


class Player(CircleShape):
    def __init__(self, x, y, game):
        super().__init__(x, y, game.player_radius)

        self.game = game
        self.radius = game.player_radius
        self.rotation = 0
        self.shoot_timer = 0
        self.score = 0
        self.name = "Buzz Lightyear"
        self.ship_color = (255,255,255)
        self.bullet_color = (0,255,0)
        self.background_color = (0,0,0)
        self.lives = 1

    def get_color_from_db(self):
        # return get_player_color()
       pass
    
     
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.ship_color, self.triangle(), 2)
        pass

    def rotate(self, dt):
        self.rotation += self.game.player_turn_speed * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()       

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.shoot_timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.game.player_movement_speed * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return        
        
        shot = Shot(self.position.x, self.position.y, self.game.shot_radius, self.bullet_color)

        forward = pygame.Vector2(0, 1).rotate(self.rotation)  
        shot.velocity = forward * self.game.player_shot_speed

        self.shoot_timer = self.game.player_shoot_cooldown

        if self.game.shot_radius == 5:
                shot_channel = pygame.mixer.Channel(1)
                normal_shot_sound = pygame.mixer.Sound(NORMAL_SHOT_PATH)
                shot_channel.play(normal_shot_sound)
                normal_shot_sound.set_volume(self.game.sound_effect_volume)
        elif self.game.shot_radius > 5:
                shot_channel = pygame.mixer.Channel(1)
                big_shot_sound = pygame.mixer.Sound(BIG_SHOT_PATH)
                shot_channel.play(big_shot_sound)
                big_shot_sound.set_volume(self.game.sound_effect_volume)


        return shot
    
    def update_settings(self):
        try:
            with open('player_settings.csv', 'r', newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            if len(rows) > 1:
                # Assign values from the second row
                self.name = rows[1][0].strip()  # Player_Name
                self.ship_color = tuple(map(int, rows[1][1].strip('()').split(',')))  # Convert to tuple of ints
                self.bullet_color = tuple(map(int, rows[1][2].strip('()').split(',')))  # Convert to tuple of ints
                self.background_color = tuple(map(int, rows[1][3].strip('()').split(',')))  # Convert to tuple of ints

        except FileNotFoundError:
            print("Error: player_settings.csv file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")