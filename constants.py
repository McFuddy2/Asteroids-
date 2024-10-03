SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # 0.8 seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500 #500
PLAYER_SHOOT_COOLDOWN = 0.3

SHOT_RADIUS = 5

BRIGHT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)] #red, green, blue, yellow, white
PLAYER_COLOR_INDEX = 2
PLAYER_COLOR = BRIGHT_COLORS[PLAYER_COLOR_INDEX]
SHOT_COLOR_INDEX = 1
SHOT_COLOR = BRIGHT_COLORS[SHOT_COLOR_INDEX]

DARK_COLORS = [(10, 0, 0), (0, 10, 0), (0, 0, 10), (5, 0, 5), (0, 0, 0)]
BACKGROUND_COLOR = (0, 0, 0)

    