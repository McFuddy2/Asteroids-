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


def create_hall_of_fame():
    hall_of_fame_file = 'halloffame.csv'

    if not os.path.exists(hall_of_fame_file):
        with open(hall_of_fame_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Player_Name", "Score", "Date"])
            # Write initial data
            initial_data = [
                ["McFuddy", 1, "2024-10-07 14:44:55"],
                ["Average Joe", 10, "2024-10-07 15:00:57"],
                ["Decent Doug", 50, "2024-10-07 15:03:16"],
                ["Good Gary", 100, "2024-10-07 15:04:42"],
                ["Impressive Ivan", 250, "2024-10-07 15:06:16"],
                ["Outstanding Oscar", 500, "2024-10-07 15:10:38"],
                ["Fantastic Frank", 750, "2024-10-07 15:10:52"],
                ["Great Greg", 1000, "2024-10-07 15:14:36"],
                ["Amazing Amy", 1500, "2024-10-07 15:19:59"],
                ["Incredible Irene", 2500, "2024-10-07 15:22:07"]
            ]
            writer.writerows(initial_data)
            




def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    score_font = pygame.font.Font(None,36)
    score_color = (0, 255, 0)

    clock = pygame.time.Clock()
    dt = 0
 

    gameIsRunning = True
    activeGame = False
    while gameIsRunning:
        updatable, drawable, asteroids, shots, player, asteroid_field = start_new_game()
        paused = False

        

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
                        print("GAME OVER!")
                        activeGame = False
                        gameOver = game_over_menu(screen, clock, player)
                        print("Game Over 7")
                        if gameOver == True:
                            activeGame = True
                            updatable, drawable, asteroids, shots, player, asteroid_field = start_new_game()  # Reset game
                        elif gameOver == False:
                            gameIsRunning = False 
                        elif gameOver == "main_menu":
                            break

                    for shot in shots:
                        shotCollision = obj.collided(shot)
                        if shotCollision == True:
                            player.score += obj.split() * SCORE_MULTIPLYER
                            shot.kill()

                screen.fill(BACKGROUND_COLOR)
                
                for obj in drawable:
                    obj.draw(screen)
                
                player.score = player.score+ (dt * SCORE_MULTIPLYER)
                

                score_text = score_font.render(f"Score: {int(player.score)}", True, score_color)
                score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # Position at top-right corner
                screen.blit(score_text, score_rect)


                pygame.display.flip()
        playTime = main_menu(screen, clock)
        if playTime == True:
            activeGame = True
        elif playTime == False:
            gameIsRunning = False   
        elif playTime == "Settings":
            settings_menu(screen, clock, player)    
                
def start_new_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    return updatable, drawable, asteroids, shots, player, asteroid_field

if __name__ == "__main__":
    create_hall_of_fame()
    main()