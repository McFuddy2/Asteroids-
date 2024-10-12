import csv
from datetime import datetime
from helpfulfunctions import *
import pygame
import random


def get_top_ten_scores():
    hall_of_fame = []
    try:
        with open('halloffame.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    if row[0] == "Player_Name":
                        continue
                    player_name, score, date = row

                    try:
                        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                        formatted_date = date_obj.strftime("%m-%d-%y")
                    except:
                        formatted_date = date

                    hall_of_fame.append([player_name, int(score), formatted_date])
        hall_of_fame.sort(key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        print("Hall Of Fame Not Found")
    return hall_of_fame[:10]

def update_player_settings(player):
    with open('player_settings.csv', 'r', newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows= list(reader)
    if len(rows) > 1:
        rows[1] = [player.name, player.ship_color, player.bullet_color, player.background_color]
    
    with open('player_settings.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def update_game_settings(game):
    with open('game_settings.csv', 'r', newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows= list(reader)
    if len(rows) > 1:
        rows[1] = [game.music_volume, game.sound_effect_volume]
    
    with open('game_settings.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def change_music(new_song):
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(new_song)
        pygame.mixer.music.play(-1)
        if new_song == "music/menu_background.mp3":
            pygame.mixer.music.set_pos(1.5)
    except pygame.error as e:
        print(f"Error playing the music: {e}") 

def display_hall_of_fame(screen, top_ten_scores):
    hall_of_fame_font = pygame.font.Font(None, 90)
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
    score_x = screen.get_width() * 0.72  # Position for the scores
    date_x = screen.get_width() * 0.82  # Position for the dates


    for i, (name, score, date) in enumerate(top_ten_scores):
            entry_font_size = 40 - (i * 2)
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
    
def check_item_drop(game):
    drop_chance = random.randint(1,100)

    good_drop_chance = 100 * game.pos_item_drop_chance
    Bad_drop_chance = 100 - (100 * game.neg_item_drop_chance)

    if 1 <= drop_chance <= good_drop_chance:
        return "boon"
    elif Bad_drop_chance <= drop_chance <= 100:
        return "bane"
    else:
        return None
    
def is_message_expired(expire_time):
        expired = pygame.time.get_ticks() >= expire_time
        return expired











