import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from constants import *



def main():
    pygame.init
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    loop = True
    while loop == True:
        # this makes the games X button actually close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        screen.fill(color=(0, 0, 0))
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        
    
    
    return


if __name__ == "__main__":
    main()