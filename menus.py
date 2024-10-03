import pygame
from constants import *
from sql_setup import *


class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]

# Pause Menu Function
def pause_menu(screen, clock):
    close_menu_button = Button("Close Menu", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 200, 50)
    quit_game_button = Button("Quit Game", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 60, 200, 50)
    main_menu_button = Button("Main Menu", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 120, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  True# Close the pause menu

        # Clear screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text_surface = font.render("Paused", True, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        close_menu_button.draw(screen)
        quit_game_button.draw(screen)
        main_menu_button.draw(screen)

        # Check for button clicks
        if close_menu_button.is_clicked():
            return  True # Close the pause menu
        if quit_game_button.is_clicked():
            pygame.quit()
            return False
        if main_menu_button.is_clicked():
            print("You clicked MAIN MENU")
            return "main_menu"

        pygame.display.flip()
        clock.tick(60)  # Control the frame rate


def main_menu(screen, clock):
    start_game_button = Button("Start Game", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 40, 200, 50)
    quit_game_button = Button("Quit Game", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 200, 50)
    settings_button = Button("Settings", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 80, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

        # Clear screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text_surface = font.render("Main Menu", True, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        start_game_button.draw(screen)
        quit_game_button.draw(screen)
        settings_button.draw(screen)

        # Check for button clicks (for now they will not do anything)
        if start_game_button.is_clicked():
            return True  # This can be changed to start the game later
        if quit_game_button.is_clicked():
            pygame.quit()
            return False
        if settings_button.is_clicked():
            print("Settings clicked")
            return "Settings"


        pygame.display.flip()
        clock.tick(60)


def game_over_menu(screen, clock,):
    start_new_game_button = Button("Start New Game", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 40, 200, 50)
    quit_game_button = Button("Quit Game", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 200, 50)
    main_menu_button = Button("Main Menu", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 80, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

        # Clear screen
        screen.fill((255, 0, 0))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        start_new_game_button.draw(screen)
        quit_game_button.draw(screen)
        main_menu_button.draw(screen)

        # Check for button clicks (for now they will not do anything)
        if start_new_game_button.is_clicked():
            print("Start New Game clicked")
            return True  # This can be changed to start the game later
        if quit_game_button.is_clicked():
            pygame.quit()
            return False
        if main_menu_button.is_clicked():
            print("You clicked MAIN MENU")
            return "main_menu"

        pygame.display.flip()
        clock.tick(60)

def settings_menu(screen, clock, player):
    change_player_color_button = Button("Change Ship Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 40, 400, 50)
    change_player_bullet_color_button = Button("Change Bullet Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 400, 50)
    change_background_color_button = Button("Change Background Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 80, 400, 50)
    back_button = Button("Back", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 200, 200, 50)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

        # Clear screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("Settings", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        change_player_color_button.draw(screen)
        change_player_bullet_color_button.draw(screen)
        change_background_color_button.draw(screen)
        back_button.draw(screen)

     
        
        if change_player_color_button.is_clicked():
            """
            new_color = (255, 0, 0)  
            update_player_color(new_color) 
            player.update_color()  
            print("Player color changed")
            """
            pass
           
        if change_player_bullet_color_button.is_clicked():
            print("bullet color clicked")
            pass
        if change_background_color_button.is_clicked():
            print("background color clicked")
            pass
        if back_button.is_clicked():
            return "main_menu"

        pygame.display.flip()
        clock.tick(60)