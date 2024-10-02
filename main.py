import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *


def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

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

    def draw_pause_menu(screen):
        font = pygame.font.Font(None, 74) 
        text = font.render("PAUSED", True, (255, 255, 255)) 
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    gameIsRunning = True
    paused = False
    while gameIsRunning:
        # this makes the games X button actually close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsRunning = False
            # this makes ESC pause the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                       

        if paused:
            draw_pause_menu(screen)
            pygame.display.flip() 
        else: 
            dt = clock.tick(60) / 1000
            if dt > .02:
                dt = .001
            

            for obj in updatable:
                obj.isPaused = paused
                obj.update(dt)

            asteroid_field.isPaused = paused

            for obj in asteroids:
                playerCollision = obj.collided(player)
                if playerCollision == True:
                    print("GAME OVER!")
                    return
                for shot in shots:
                    shotCollision = obj.collided(shot)
                    if shotCollision == True:
                        obj.split()
                        shot.kill()

            screen.fill(color=(0, 0, 0))
            
            for obj in drawable:
                obj.draw(screen)
                
            pygame.display.flip()
                
                


if __name__ == "__main__":
    main()