import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *
from menus import *
import csv
from helpfulfunctions import *
from gameclass import Game
from itemdrops import *
from boonfunctions import *
from banefunctions import *


def create_csv_files():
    hall_of_fame_file = 'halloffame.csv'
    player_settings_file = 'player_settings.csv'
    game_settings_file = 'game_settings.csv'
    


    if not os.path.exists(hall_of_fame_file):
        with open(hall_of_fame_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Player_Name", "Score", "Date"])
            # Write initial data
            initial_data = [
                ["McFuddy", 1, "2024-10-07 14:44:55"],
                ["Average Joe", 50, "2024-10-07 15:00:57"],
                ["Decent Doug", 100, "2024-10-07 15:03:16"],
                ["Good Gary", 500, "2024-10-07 15:04:42"],
                ["Impressive Ivan", 1000, "2024-10-07 15:06:16"],
                ["Outstanding Oscar", 2500, "2024-10-07 15:10:38"],
                ["Fantastic Frank", 5000, "2024-10-07 15:10:52"],
                ["Great Greg", 7500, "2024-10-07 15:14:36"],
                ["Amazing Amy", 10000, "2024-10-07 15:19:59"],
                ["Incredible Irene", 15000, "2024-10-07 15:22:07"]
            ]
            writer.writerows(initial_data)

    if not os.path.exists(player_settings_file):
        with open(player_settings_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Player_Name", "Ship_Color", "Bullet_Color", "Background_Color", "Music_Volume", "Sound_Effect_Volume"])
            # Write initial data
            initial_data = (["Buzz Lightyear","(0, 0, 255)","(255, 0, 0)","(0, 0, 0)", "0.5", "0.1"])
            writer.writerows(initial_data)
    
    if not os.path.exists(game_settings_file):
        with open(game_settings_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Music_Volume", "Sound_Effect_Volume"])
            # Write initial data
            initial_data = (["0.0","0.3"])
            writer.writerows(initial_data)
            




def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(3) 
    
    print("Starting asteroids!")

    #check settings
    with open('game_settings.csv', 'r', newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows= list(reader)
    if len(rows) > 1:
        music_setting = float(rows[1][0])
        sound_effect_setting = float(rows[1][1])
    try:
        change_music(MENU_MUSIC_PATH)

        pygame.mixer.music.set_volume(music_setting)
        pygame.mixer.Channel(1).set_volume(sound_effect_setting)
        pygame.mixer.Channel(2).set_volume(sound_effect_setting)

    except pygame.error as e:
        print(f"MUSIC ERROR! {e}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
 

    gameIsRunning = True
    activeGame = False
    item_messages = []
    while gameIsRunning:
        updatable, drawable, asteroids, shots, item_drops, player, game = start_new_game()
        paused = False
        
        if activeGame:
            change_music(INGAME_MUSIC_PATH)
        while activeGame:
            # this makes the games X button actually close the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameIsRunning = False
                    return 
                
                # this makes ESC pause the game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        

            if paused:
                result = pause_menu(screen, clock)
                if result == False:
                    gameIsRunning = False
                elif result == "main_menu":
                    break
                elif result == True:
                    paused = False
                    change_music(INGAME_MUSIC_PATH)
                    pygame.mixer.music.set_pos(2)
                else:
                    print("ERROR UNEXPECTED INPUT FROM PAUSE MENU.")
                pygame.display.flip() 

            else: 
                dt = clock.tick(60) / 1000
                if dt > .02:
                    dt = .001
                

                for obj in updatable:
                    obj.update(dt)

                for obj in asteroids:
                    playerCollision = obj.collided(player)
                    if playerCollision == True:
                        if player.lives <= 1:
                            print("GAME OVER!")
                            activeGame = False
                            gameOver = game_over_menu(screen, clock, player)
                            if gameOver == True:
                                activeGame = True
                                updatable, drawable, asteroids, shots, item_drops, player, game = start_new_game()
                                change_music(INGAME_MUSIC_PATH)  # Reset game
                            elif gameOver == False:
                                gameIsRunning = False 
                            elif gameOver == "main_menu":
                                break
                        else:
                            player.lives -= 1
                            player.score -= obj.split(player, True)

                    for shot in shots:
                        shotCollision = obj.collided(shot)
                        if shotCollision == True:
                            player.score += obj.split(player, False) * game.score_multiplier
                            shot.kill()
                    
                for item in item_drops:
                    if item.collided(player):
                        item.apply_effect(player, game)
                        item_messages.append((item.message, item.expire_time, ((0,75,255) if item.type == "boon" else (255,0,75)), item.undo_effect))
                        item.kill()


                screen.fill(player.background_color)
                
                for obj in drawable:
                    obj.draw(screen)
                
                player.score = player.score + (dt * game.score_multiplier)
                score_font = pygame.font.Font(None,36)
                score_color = (0, 255, 0)

                score_text = score_font.render(f"Score: {int(player.score)}", True, score_color)
                score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # Position at top-right corner
                screen.blit(score_text, score_rect)

                
                lives_font = pygame.font.Font(None,36)
                lives_color = (0, 255, 0)
                lives_text = lives_font.render(f"Lives Remaining: {int(player.lives)}", True, lives_color)
                lives_rect = lives_text.get_rect(topleft=(20, 20))  # Position at top-left corner
                screen.blit(lives_text, lives_rect)



                message_y_position = score_rect.bottom + 25  # Start just below the score text
                expired_messages = []
                for message, expired_time, color, undo_effect in item_messages:
                    if not is_message_expired(expired_time):
                        item_font = pygame.font.Font(None,32)
                        item_text = item_font.render(message, True, color)
                        item_rect = item_text.get_rect(topright=(SCREEN_WIDTH - 50, message_y_position))  # Position at top-right corner
                        screen.blit(item_text, item_rect)
                        message_y_position += 30

                    else:
                        print(undo_effect)
                        undo_effect(player, game)
                        expired_messages.append((message, expired_time, color, undo_effect))
                        
                for expired_message in expired_messages:
                    item_messages.remove(expired_message)


                pygame.display.flip()

        playTime = main_menu(screen, clock)
        if playTime == True:
            activeGame = True
        elif playTime == False:
            gameIsRunning = False   
        elif playTime == "Options":
            options_menu(screen, clock, player, game)    
                
def start_new_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    item_drops = pygame.sprite.Group()

    game = Game()
    game.update_settings()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable

    Player.containers = (updatable, drawable)

    Shot.containers = (shots, updatable, drawable)

    ItemDrops.containers = (updatable, drawable, item_drops)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, game)
    player.update_settings()

    asteroid_field = AsteroidField(game)

    return updatable, drawable, asteroids, shots, item_drops, player, game 

if __name__ == "__main__":
    create_csv_files()
    main()