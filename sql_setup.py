""""
import sqlite3 

def setup_database():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bright_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color_code TEXT NOT NULL,
            color_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dark_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color_code TEXT NOT NULL,
            color_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_color_id INTEGER NOT NULL,
            shot_color_id INTEGER NOT NULL,
            background_color_id INTEGER NOT NULL,
            FOREIGN KEY (player_color_id) REFERENCES bright_colors(id),
            FOREIGN KEY (shot_color_id) REFERENCES bright_colors(id),
            FOREIGN KEY (background_color_id) REFERENCES dark_colors(id)
        )
    ''')

    # Insert default bright colors (example colors)
    cursor.executemany('INSERT INTO bright_colors (color_code, color_name) VALUES (?, ?)', [
        ('(255, 255, 255)', "White"),
        ('(255, 0, 0)', "Red"),   
        ('(255, 255, 0)', "Yellow"), 
        ('(0, 255, 0)', "Green"),   
        ('(0, 255, 255)', "Cyan"),
        ('(255, 0, 255)', "Magenta"), 
        ('(255, 165, 0)', "Orange"), 
    ])

    # Insert default dark colors (example colors)
    cursor.executemany('INSERT INTO dark_colors (color_code, color_name) VALUES (?, ?)', [
        ('(5, 0, 10)', "Dark Purple"),
        ('(50, 50, 50)', "Dark Gray"),  
        ('(100, 100, 100)', "Medium Gray"), 
        ('(10, 0, 0)', "Dark Red"),    
        ('(0, 10, 0)', "Dark Green"),
        ('(0, 0, 10)', "Dark Blue"),
        ('(0, 0, 0)', "Black"),
    ])

    # Insert default current colors with foreign keys for existing colors
    cursor.execute('INSERT INTO current_colors (player_color_id, shot_color_id, background_color_id) VALUES (?, ?, ?)', 
                   (1, 1, 1))  # Ensure these IDs correspond to existing colors in bright_colors and dark_colors

    conn.commit()
    conn.close()

# Function to get the player color from the current_colors table
def get_player_color():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bright_colors.color_code 
        FROM current_colors
        JOIN bright_colors ON current_colors.player_color_id = bright_colors.id
        WHERE current_colors.id = 1
    ''')
    color = cursor.fetchone()
    conn.close()
    return tuple(map(int, color[0].strip('()').split(', '))) if color else (255, 0, 0)   # Safely convert to tuple

# Function to update the player color in the current_colors table
def update_player_color(new_color_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE current_colors SET player_color_id = ? WHERE id = 1', (new_color_id,))
    conn.commit()
    conn.close()
 
"""