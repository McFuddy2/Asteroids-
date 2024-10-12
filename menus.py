import pygame
from constants import *
from datetime import datetime
import csv
from helpfulfunctions import *
import time 
import math


class Button:
    def __init__(self, text, x, y, width, height, color=(200,200,200), hover_color=(150,150,150), text_color=(0,0,0), font_size=36, click_delay=0.1):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.last_clicked_time = 0
        self.click_delay = click_delay

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        current_time = time.time()

        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            if current_time - self.last_clicked_time >= self.click_delay:
                self.last_clicked_time = current_time
                return True
        return False


        return self.rect.collidepoint(mouse_pos) and mouse_click[0]

# Pause Menu Function
def pause_menu(screen, clock):
    change_music(MENU_MUSIC_PATH)
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
    window_opened_time = time.time()
    start_game_button = Button("Start Game", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 - 40, 200, 50)
    quit_game_button = Button("Quit Game", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 + 20, 200, 50)
    options_button = Button("Options", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 + 80, 200, 50)


    top_ten_scores = get_top_ten_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

        # Clear screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("ASTEROIDS", True, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() // 4 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        start_game_button.draw(screen)
        quit_game_button.draw(screen)
        options_button.draw(screen)

        # Check for button clicks (for now they will not do anything)
        if start_game_button.is_clicked() and (time.time() - window_opened_time)> .1:
            return True  # This can be changed to start the game later
        if quit_game_button.is_clicked() and (time.time() - window_opened_time)> .1:
            pygame.quit()
            return False
        if options_button.is_clicked() and (time.time() - window_opened_time)> .1:
            print("Options clicked")
            return "Options"


        display_hall_of_fame(screen, top_ten_scores)

        pygame.display.flip()
        clock.tick(60)

def game_over_menu(screen, clock, player):
    change_music(MENU_MUSIC_PATH)
    start_new_game_button = Button("Start New Game", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 - 40, 200, 50)
    quit_game_button = Button("Quit Game", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 + 20, 200, 50)
    main_menu_button = Button("Main Menu", (screen.get_width() // 4 - 100), SCREEN_HEIGHT // 2 + 80, 200, 50)


    top_ten_score_menu(screen, player)
    top_ten_scores = get_top_ten_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

       
        screen.fill((128, 0, 12))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 4 - text_surface.get_width() // 2, screen.get_height() // 4))

        final_score_font = pygame.font.Font(None, 50)
        final_score_text = final_score_font.render(f"Final Score: {math.floor(player.score)}", True, (0, 0, 0))
        screen.blit(final_score_text, (screen.get_width() // 4 - final_score_text.get_width() // 2, screen.get_height() // 8))

        # Draw buttons
        start_new_game_button.draw(screen)
        quit_game_button.draw(screen)
        main_menu_button.draw(screen)

        if start_new_game_button.is_clicked():
            return True 
        if quit_game_button.is_clicked():
            pygame.quit()
            return False
        if main_menu_button.is_clicked():
            return "main_menu"

        display_hall_of_fame(screen, top_ten_scores)


        pygame.display.flip()
        clock.tick(60)

def options_menu(screen, clock, player, game):
    window_opened_time = time.time()
    change_player_color_button = Button("Change Ship Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 160, 400, 50)
    change_player_bullet_color_button = Button("Change Bullet Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100, 400, 50)
    change_background_color_button = Button("Change Background Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 40, 400, 50)
    how_to_play_button = Button("How To Play", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 400, 50)
    music_button = Button("Music Settings", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 80, 400, 50)
    back_button = Button("Back", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 200, 200, 50)

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game

        # Clear screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("Options", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Draw buttons
        change_player_color_button.draw(screen)
        change_player_bullet_color_button.draw(screen)
        change_background_color_button.draw(screen)
        how_to_play_button.draw(screen)
        music_button.draw(screen)
        back_button.draw(screen)
        
        if change_player_color_button.is_clicked() and (time.time() - window_opened_time)> .1:
            new_ship_color = change_ship_color_menu(screen, clock, player.ship_color)
            player.ship_color = new_ship_color
            update_player_settings(player)
           
        if change_player_bullet_color_button.is_clicked() and (time.time() - window_opened_time)> .1:
            new_bullet_color = change_bullet_color_menu(screen, clock, player.bullet_color)
            player.bullet_color = new_bullet_color
            update_player_settings(player)

        if change_background_color_button.is_clicked() and (time.time() - window_opened_time)> .1:
            new_background_color = change_background_color_menu(screen, clock, player.background_color)
            player.background_color = new_background_color
            update_player_settings(player)

        if music_button.is_clicked() and (time.time() - window_opened_time)> .1:
            game.music_volume, game.sound_effect_volume = change_music_settings_menu(screen, clock, game)
            update_game_settings(game)
            

        if how_to_play_button.is_clicked()  and (time.time() - window_opened_time)> .1:
            how_to_play_menu(screen, clock)

        if back_button.is_clicked()  and (time.time() - window_opened_time) > .1:
            return "main_menu"

        pygame.display.flip()
        clock.tick(60)

def top_ten_score_menu(screen, player):

    def add_to_hall_of_fame(player_name, score):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('halloffame.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score, current_date])
    

    submit_score_button = Button("Submit", SCREEN_WIDTH // 2, SCREEN_HEIGHT *.75 + 25, 200, 50)
    input_active = True
    player_name = player.name if player.name else ""
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                # Handle text input
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  # Remove last character if backspace is pressed
                    elif event.key == pygame.K_RETURN:
                        if player_name:  # Ensure the player name is not empty
                            player.name = player_name
                            add_to_hall_of_fame(player.name, int(player.score))
                            return
                    elif len(player_name) < 20:  # Limit name length to 15 characters
                        player_name += event.unicode  # Add typed character to name
        player.name = player_name
        update_player_settings(player)
    

        screen.fill((0, 0, 200))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("NEW HIGH SCORE", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 4))

        # Render the input box for player name
        font = pygame.font.Font(None, 74)
        name_surface = font.render(player_name, True, (255, 255, 255))
        input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 400, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)  # Draw input box outline
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        submit_score_button.draw(screen)

        if submit_score_button.is_clicked():
            if player_name:  # Ensure the player name is not empty
                player.name = player_name
                # Call function to save score, e.g., add_to_hall_of_fame
                add_to_hall_of_fame(player.name, int(player.score))
                return
            
        pygame.display.flip()

def how_to_play_menu(screen, clock):
    window_size = {"x":1000, "y":400}
    x_close_button = Button("X", SCREEN_WIDTH // 2 + (window_size["x"] // 2) - 25, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) -25, 50, 50, (255,0,0), (153,0,0))




    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

        # Dim the screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128) #Transparency level from 0-255
        s.fill((0, 0, 0))
        screen.blit(s, (0,0))

        #Draw the small how to window
        pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH // 2 - (window_size["x"] // 2), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), window_size["x"], window_size["y"]))
        
        # Add some instructions text
        font = pygame.font.Font(None, 36)
        how_to_play = ["How to Play:", 
                        "Use A and D to rotate",
                        "Use W and S to move forward and backward", 
                        "Press space to shoot",
                        "You get points for destroying Asteroids and for the time you have survived", 
                        "Destroyed Asteroids have a chance to drop an item. Some are good, others are not",
                        "Avoid asteroids and stay alive!",
                        "",
                        "TIP: Killing smaller asteroids is worth more points"]
        
        for i, line in enumerate(how_to_play):
            if i == 0:
                # First line of how_to_play
                font = pygame.font.Font(None, 64)
                text_surface = font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - (window_size["y"] // 2)+10))
            elif i == len(how_to_play) -1:
                # last line of how_to play
                font = pygame.font.Font(None, 24)
                text_surface = font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) + 60 + i * 40))
            else:
                # all lines in how_to_play other than first and last
                font = pygame.font.Font(None, 36)
                text_surface = font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) + 60 + i * 40))

        # Draw button
        x_close_button.draw(screen)

    
        if x_close_button.is_clicked():
            return True

        pygame.display.flip()
        clock.tick(60)

def change_background_color_menu(screen, clock, color):
    window_size = {"x":400, "y":400}
    button_x = (SCREEN_WIDTH // 4 + 150)
    colors = {
        "black": (0,0,0), #black
        "dark red": (30,0,0), #red
        "dark green": (0,30,0),#green
        "dark blue": (0,0,30),#blue 
        "dark grey": (25,25,25) #grey
    }
    x_close_button = Button("X", SCREEN_WIDTH // 2 + (window_size["x"] // 2) - 25, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) -25, 50, 50, (255,0,0), (153,0,0))
    black_button = Button("Black", button_x, SCREEN_HEIGHT // 2 - 160, 100, 50, (200,200,200), colors["black"])
    red_button = Button("Red", button_x, SCREEN_HEIGHT // 2 - 100, 100, 50, (200,200,200), colors["dark red"])
    green_button = Button("Green", button_x, SCREEN_HEIGHT // 2 - 40, 100, 50, (200,200,200), colors["dark green"])
    blue_button = Button("Blue", button_x, SCREEN_HEIGHT // 2 + 20, 100, 50, (200,200,200), colors["dark blue"])
    grey_button = Button("Grey", button_x, SCREEN_HEIGHT // 2 + 80, 100, 50,(200,200,200), colors["dark grey"])

    selected_color = color


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return selected_color

        # Dim the screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128) #Transparency level from 0-255
        s.fill((0, 0, 0))
        screen.blit(s, (0,0))

        #Draw the small window and the tiny example screen
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH // 2 - (window_size["x"] // 2), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), window_size["x"], window_size["y"]))
        pygame.draw.rect(screen, selected_color, ((SCREEN_WIDTH // 2 + (window_size["x"] // 2)-150), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), 150, 150))
        
        # Draw button
        x_close_button.draw(screen)
        black_button.draw(screen)
        red_button.draw(screen)
        green_button.draw(screen)
        blue_button.draw(screen)
        grey_button.draw(screen)

    
        if x_close_button.is_clicked():
            return selected_color
        if black_button.is_clicked():
            selected_color = colors["black"]
        if red_button.is_clicked():
            selected_color = colors["dark red"]
        if green_button.is_clicked():
            selected_color = colors["dark green"]
        if blue_button.is_clicked():
            selected_color = colors["dark blue"]
        if grey_button.is_clicked():
            selected_color = colors["dark grey"]


    

        pygame.display.flip()
        clock.tick(60)    

    return selected_color

def change_bullet_color_menu(screen, clock, color):
    window_size = {"x":400, "y":400}
    button_x = (SCREEN_WIDTH // 4 + 150)
    x_close_button = Button("X", SCREEN_WIDTH // 2 + (window_size["x"] // 2) - 25, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) -25, 50, 50, (255,0,0), (153,0,0))
    white_button = Button("White", button_x, SCREEN_HEIGHT // 2 - 160, 100, 50, (200,200,200), (255,255,255))
    red_button = Button("Red", button_x, SCREEN_HEIGHT // 2 - 100, 100, 50, (200,200,200), (255,0,0))
    green_button = Button("Green", button_x, SCREEN_HEIGHT // 2 - 40, 100, 50, (200,200,200), (0,255,0))
    blue_button = Button("Blue", button_x, SCREEN_HEIGHT // 2 + 20, 100, 50, (200,200,200), (0,0,255))
    grey_button = Button("Grey", button_x, SCREEN_HEIGHT // 2 + 80, 100, 50,(200,200,200), (150,150,150))

    colors = {
        "white": (255,255,255), #black
        "red": (255,0,0), #red
        "green": (0,255,0),#green
        "blue": (0,0,255),#blue 
        "grey": (150,150,150) #grey
    }

    selected_color = color


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return selected_color

        # Dim the screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128) #Transparency level from 0-255
        s.fill((0, 0, 0))
        screen.blit(s, (0,0))

        #Draw the small window and the tiny example screen
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH // 2 - (window_size["x"] // 2), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), window_size["x"], window_size["y"]))
        pygame.draw.rect(screen, selected_color, ((SCREEN_WIDTH // 2 + (window_size["x"] // 2)-150), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), 150, 150))
        
        # Draw button
        x_close_button.draw(screen)
        white_button.draw(screen)
        red_button.draw(screen)
        green_button.draw(screen)
        blue_button.draw(screen)
        grey_button.draw(screen)

    
        if x_close_button.is_clicked():
            return selected_color
        if white_button.is_clicked():
            selected_color = colors["white"]
        if red_button.is_clicked():
            selected_color = colors["red"]
        if green_button.is_clicked():
            selected_color = colors["green"]
        if blue_button.is_clicked():
            selected_color = colors["blue"]
        if grey_button.is_clicked():
            selected_color = colors["grey"]


    

        pygame.display.flip()
        clock.tick(60)    

    return selected_color

def change_ship_color_menu(screen, clock, color):
    window_size = {"x":400, "y":400}
    button_x = (SCREEN_WIDTH // 4 + 150)
    x_close_button = Button("X", SCREEN_WIDTH // 2 + (window_size["x"] // 2) - 25, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) -25, 50, 50, (255,0,0), (153,0,0))
    white_button = Button("White", button_x, SCREEN_HEIGHT // 2 - 160, 100, 50, (200,200,200), (255,255,255))
    red_button = Button("Red", button_x, SCREEN_HEIGHT // 2 - 100, 100, 50, (200,200,200), (255,0,0))
    green_button = Button("Green", button_x, SCREEN_HEIGHT // 2 - 40, 100, 50, (200,200,200), (0,255,0))
    blue_button = Button("Blue", button_x, SCREEN_HEIGHT // 2 + 20, 100, 50, (200,200,200), (0,0,255))
    grey_button = Button("Grey", button_x, SCREEN_HEIGHT // 2 + 80, 100, 50,(200,200,200), (150,150,150))

    colors = {
        "white": (255,255,255), #black
        "red": (255,0,0), #red
        "green": (0,255,0),#green
        "blue": (0,0,255),#blue 
        "grey": (150,150,150) #grey
    }

    selected_color = color


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return selected_color

        # Dim the screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128) #Transparency level from 0-255
        s.fill((0, 0, 0))
        screen.blit(s, (0,0))

        #Draw the small window and the tiny example screen
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH // 2 - (window_size["x"] // 2), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), window_size["x"], window_size["y"]))
        pygame.draw.rect(screen, selected_color, ((SCREEN_WIDTH // 2 + (window_size["x"] // 2)-150), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), 150, 150))
        
        # Draw button
        x_close_button.draw(screen)
        white_button.draw(screen)
        red_button.draw(screen)
        green_button.draw(screen)
        blue_button.draw(screen)
        grey_button.draw(screen)

    
        if x_close_button.is_clicked():
            return selected_color
        if white_button.is_clicked():
            selected_color = colors["white"]
        if red_button.is_clicked():
            selected_color = colors["red"]
        if green_button.is_clicked():
            selected_color = colors["green"]
        if blue_button.is_clicked():
            selected_color = colors["blue"]
        if grey_button.is_clicked():
            selected_color = colors["grey"]


    

        pygame.display.flip()
        clock.tick(60)    

    return selected_color

def change_music_settings_menu(screen, clock, game):
    window_opened_time = time.time()

    rows_of_buttons = 2
    button_size = {"x":250, "y":50}
    window_size = {"x":(button_size["x"]* 2 + 150), "y":(button_size["y"] * rows_of_buttons + (100+ (rows_of_buttons*10)))}
    
    x_close_button = Button("X", SCREEN_WIDTH // 2 + (window_size["x"] // 2) - 25, SCREEN_HEIGHT // 2 - (window_size["y"] // 2) -25, 50, 50, (255,0,0), (153,0,0))
    
    button_x1_coord = (SCREEN_WIDTH // 2 - (window_size["x"]//2) + 25)
    button_x2_coord = (button_x1_coord + button_size["x"] + 25)
    button_y_coord = (SCREEN_HEIGHT // 2 - (window_size["y"]//2) + 50)

    music_volume_up_button = Button("Music +", button_x1_coord, button_y_coord, button_size["x"],button_size["y"])
    music_volume_down_button = Button("Music -", button_x2_coord, button_y_coord, button_size["x"],button_size["y"])
    
    sound_effects_volume_up_button = Button("Sound Effects +", button_x1_coord, button_y_coord + button_size["y"] + 10, button_size["x"],button_size["y"])
    sound_effects_volume_down_button = Button("Sound Effects -", button_x2_coord, button_y_coord + button_size["y"] + 10, button_size["x"],button_size["y"])
    

    selected_music_volume = game.music_volume
    selected_sound_effect_volume = game.sound_effect_volume
    
    pygame.font.init()
    font = pygame.font.Font(None, 46)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Close the menu and game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return selected_music_volume, selected_sound_effect_volume

        # Dim the screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128) #Transparency level from 0-255
        s.fill((0, 0, 0))
        screen.blit(s, (0,0))

        #Draw the small window and the tiny example screen
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH // 2 - (window_size["x"] // 2), SCREEN_HEIGHT // 2 - (window_size["y"] // 2), window_size["x"], window_size["y"]))
               
        # Draw button
        x_close_button.draw(screen)
        music_volume_up_button.draw(screen)
        music_volume_down_button.draw(screen)
        sound_effects_volume_up_button.draw(screen)
        sound_effects_volume_down_button.draw(screen)



        if x_close_button.is_clicked() and (time.time() - window_opened_time)> .1:
            return selected_music_volume, selected_sound_effect_volume
        
        if music_volume_up_button.is_clicked() and (time.time() - window_opened_time)> .1:
            if selected_music_volume < .9:
                selected_music_volume += .1
                pygame.mixer.music.set_volume(selected_music_volume)
            else:
                selected_music_volume = 1.0
                pygame.mixer.music.set_volume(selected_music_volume)
                
        if music_volume_down_button.is_clicked() and (time.time() - window_opened_time)> .1:
            if selected_music_volume > .1:
                selected_music_volume -= .1
                pygame.mixer.music.set_volume(selected_music_volume)
            else:
                selected_music_volume = 0.0
                pygame.mixer.music.set_volume(selected_music_volume)
        
        if sound_effects_volume_up_button.is_clicked() and (time.time() - window_opened_time)> .1:
            if selected_sound_effect_volume < .27:
                selected_sound_effect_volume += .03
                normal_shot_sound = pygame.mixer.Sound(NORMAL_SHOT_PATH)
                pygame.mixer.Channel(1).set_volume(selected_sound_effect_volume)
                pygame.mixer.Channel(1).play(normal_shot_sound)
            else:
                selected_sound_effect_volume = .3
                normal_shot_sound = pygame.mixer.Sound(NORMAL_SHOT_PATH)
                pygame.mixer.Channel(1).set_volume(selected_sound_effect_volume)
                pygame.mixer.Channel(1).play(normal_shot_sound)

        if sound_effects_volume_down_button.is_clicked() and (time.time() - window_opened_time)> .1:
            if selected_sound_effect_volume > .03:
                selected_sound_effect_volume -= .03
                normal_shot_sound = pygame.mixer.Sound(NORMAL_SHOT_PATH)
                pygame.mixer.Channel(1).set_volume(selected_sound_effect_volume)
                pygame.mixer.Channel(1).play(normal_shot_sound)
            else:
                selected_sound_effect_volume = 0.00
                normal_shot_sound = pygame.mixer.Sound(NORMAL_SHOT_PATH)
                pygame.mixer.Channel(1).set_volume(selected_sound_effect_volume)
                pygame.mixer.Channel(1).play(normal_shot_sound)

        normalized_sound_effect_volume = (selected_sound_effect_volume / 0.3) * 100
        music_volume_percentage = font.render(f"{int(selected_music_volume * 100)}%", True, (0, 200, 0))
        sound_effect_volume_percentage = font.render(f"{int(normalized_sound_effect_volume)}%", True, (0, 200, 0))

        screen.blit(music_volume_percentage, (button_x2_coord + button_size["x"] + 25, button_y_coord + 10))  # Display next to music buttons
        screen.blit(sound_effect_volume_percentage, (button_x2_coord + button_size["x"] + 25, button_y_coord + button_size["y"] + 20))  # Display next to sound effects buttons


        pygame.display.flip()
        clock.tick(60)    
  


