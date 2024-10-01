import pygame
from constants import *

def main():
    pygame.init
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen =  pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    
    loop = True
    while loop == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(color=(0, 0, 0))
        pygame.display.flip()
        
    
    
    return


if __name__ == "__main__":
    main()