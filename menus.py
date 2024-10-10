import pygame
from constants import *
from datetime import datetime
import csv
from helpfulfunctions import *
import time 


class Button:
    def __init__(self, text, x, y, width, height, color=(200,200,200), hover_color=(150,150,150), font_size=36, click_delay=0.1):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
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
        text_surface = font.render(self.text, True, (0, 0, 0))
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
        if start_game_button.is_clicked():
            return True  # This can be changed to start the game later
        if quit_game_button.is_clicked():
            pygame.quit()
            return False
        if options_button.is_clicked():
            print("Options clicked")
            return "Options"


        hall_of_fame_font = pygame.font.Font(None, 96)
        hall_of_fame_title = hall_of_fame_font.render("HALL OF FAME", True, (255, 255, 255))
        title_x = screen.get_width() * 0.75 - hall_of_fame_title.get_width() // 2
        title_y = screen.get_height() // 12
        screen.blit(hall_of_fame_title, (title_x, title_y))

        
        # Draw a line under the title
        line_y = title_y + hall_of_fame_title.get_height() + 3  # 10 pixels below the title
        pygame.draw.line(screen, (255, 255, 255), (title_x - 15, line_y), (title_x + hall_of_fame_title.get_width() + 15, line_y), 1)  # White line with thickness of 1
        pygame.draw.line(screen, (255, 255, 255), (title_x - 15, line_y + 4), (title_x + hall_of_fame_title.get_width() + 15, line_y +4), 1)


        rank_x = screen.get_width() * 0.47  # 60% across the screen, adjust as needed
        name_x = screen.get_width() * 0.51  # Position for the player names
        score_x = screen.get_width() * 0.75  # Position for the scores
        date_x = screen.get_width() * 0.82  # Position for the dates



        for i, (name, score, date) in enumerate(top_ten_scores):
            entry_font_size = 50 - (i * 3)
            font = pygame.font.Font(None, entry_font_size)
            if i == 0:
                # Top on Hall Of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (255, 255, 0))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (255, 255, 0))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (255, 255, 0))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (255, 255, 0))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))
            
            elif i % 2 == 0:
                # odd entries on Hall of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (255, 255, 255))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (255, 255, 255))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (255, 255, 255))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (255, 255, 255))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))
        
            elif i % 2 != 0:
                # even entries on Hall of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (200, 200, 200))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (200, 200, 200))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (200, 200, 200))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (200, 200, 200))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))




        pygame.display.flip()
        clock.tick(60)

def game_over_menu(screen, clock, player):
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

        # Clear screen
        screen.fill((128, 0, 12))
        font = pygame.font.Font(None, 120)
        text_surface = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() // 4 - text_surface.get_width() // 2, screen.get_height() // 4))

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

        score_font = pygame.font.Font(None,64)
        score_color = (0, 0, 0)    
        score_text = score_font.render(f"FINAL SCORE: {int(player.score)}", True, score_color)
        screen.blit(score_text, (screen.get_width() // 4 - score_text.get_width() // 2, screen.get_height() // 8))

        hall_of_fame_font = pygame.font.Font(None, 96)
        hall_of_fame_title = hall_of_fame_font.render("HALL OF FAME", True, (255, 255, 255))
        title_x = screen.get_width() * 0.75 - hall_of_fame_title.get_width() // 2
        title_y = screen.get_height() // 12
        screen.blit(hall_of_fame_title, (title_x, title_y))

        
        # Draw a line under the title
        line_y = title_y + hall_of_fame_title.get_height() + 3  # 10 pixels below the title
        pygame.draw.line(screen, (255, 255, 255), (title_x - 15, line_y), (title_x + hall_of_fame_title.get_width() + 15, line_y), 1)  # White line with thickness of 1
        pygame.draw.line(screen, (255, 255, 255), (title_x - 15, line_y + 4), (title_x + hall_of_fame_title.get_width() + 15, line_y +4), 1)


        rank_x = screen.get_width() * 0.47  # 60% across the screen, adjust as needed
        name_x = screen.get_width() * 0.51  # Position for the player names
        score_x = screen.get_width() * 0.75  # Position for the scores
        date_x = screen.get_width() * 0.82  # Position for the dates



        for i, (name, score, date) in enumerate(top_ten_scores):
            entry_font_size = 50 - (i * 3)
            font = pygame.font.Font(None, entry_font_size)
            if i == 0:
                # Top on Hall Of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (255, 255, 0))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (255, 255, 0))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (255, 255, 0))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (255, 255, 0))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))
            
            elif i % 2 == 0:
                # odd entries on Hall of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (255, 255, 255))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (255, 255, 255))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (255, 255, 255))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (255, 255, 255))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))
        
            elif i % 2 != 0:
                # even entries on Hall of Fame
                rank_text = f"#{i + 1}"
                rank_surface = font.render(rank_text, True, (200, 200, 200))
                screen.blit(rank_surface, (rank_x, (120 + i * 45)+10))  

                name_surface = font.render(name, True, (200, 200, 200))
                screen.blit(name_surface, (name_x, (120 + i * 45)+10))

                score_surface = font.render(str(score), True, (200, 200, 200))
                screen.blit(score_surface, (score_x, (120 + i * 45)+10))

                date_surface = font.render(date, True, (200, 200, 200))
                screen.blit(date_surface, (date_x, (120 + i * 45)+10))


        pygame.display.flip()
        clock.tick(60)

def options_menu(screen, clock, player):
    change_player_color_button = Button("Change Ship Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 160, 400, 50)
    change_player_bullet_color_button = Button("Change Bullet Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100, 400, 50)
    change_background_color_button = Button("Change Background Color", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 40, 400, 50)
    how_to_play_button = Button("How To Play", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 400, 50)
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
        if how_to_play_button.is_clicked():
            print("How to Play clicked")
            how_to_play_menu(screen, clock)
            pass
        if back_button.is_clicked():
            return "main_menu"

        pygame.display.flip()
        clock.tick(60)

def top_ten_score_menu(screen, player):

    def add_to_hall_of_fame(player_name, score):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('halloffame.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score, current_date])
    

    submit_score_button = Button("Submit", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, 200, 50)
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
                        input_active = False  # Stop input when "Enter" is pressed
                    elif len(player_name) < 20:  # Limit name length to 15 characters
                        player_name += event.unicode  # Add typed character to name
        
    

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
    window_size = {"x":900, "y":400}
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