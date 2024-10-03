import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *
from menus import *


def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

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
                        gameOver = game_over_menu(screen, clock)
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
                            obj.split()
                            shot.kill()

                screen.fill(BACKGROUND_COLOR)
                
                for obj in drawable:
                    obj.draw(screen)
                    
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
    main()