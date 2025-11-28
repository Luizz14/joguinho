import os

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Menino Guloso"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)      # Unhealthy
GREEN = (50, 255, 50)    # Healthy
BLUE = (50, 50, 255)     # Player
YELLOW = (255, 255, 0)   # Text
SKY_BLUE = (135, 206, 235)

# Game Settings
PLAYER_SPEED = 10
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GROUND_HEIGHT = 100  # Height of the ground image (approx, or visual preference)

FOOD_MIN_SPEED = 5
FOOD_MAX_SPEED = 10
FOOD_SIZE = 45
SPAWN_RATE = 1000  # Milliseconds

# Scoring
SCORE_HEALTHY = 10
SCORE_UNHEALTHY = -5
WIN_SCORE = 1000  # Just a high number, game ends on time or low score
LOSE_SCORE = -20
GAME_DURATION = 60  # Seconds

# Jump Physics
GRAVITY = 0.8  # Pixels per frame squared (acceleration downward)
JUMP_POWER = -15  # Initial jump velocity (negative = upward)

# Junk Food Rain Event
EVENT_SCORE_THRESHOLDS = [50, 150, 300]  # Trigger events at these scores
JUNK_RAIN_DURATION = 8000  # Event duration in milliseconds (8 seconds)
JUNK_RAIN_SPAWN_RATE = 150  # Spawn every 150ms during event (~6-7 foods/sec)
JUNK_RAIN_WARNING_TIME = 2000  # Warning phase duration in milliseconds (2 seconds)
JUNK_RAIN_SURVIVAL_BONUS = 25  # Bonus points for surviving event
JUNK_RAIN_FOOD_MIN_SPEED = 10  # Much faster than normal
JUNK_RAIN_FOOD_MAX_SPEED = 16  # Extremely fast
JUNK_RAIN_MAX_HITS = 0  # Perfect dodging required for bonus

# Health System
PLAYER_MAX_HEALTH = 100  # Maximum and starting health
DAMAGE_UNHEALTHY = 10  # Damage from junk food (normal)
DAMAGE_UNHEALTHY_EVENT = 15  # Damage from junk food during event (more punishing)
HEAL_HEALTHY = 5  # Health restored by healthy food
HEALTH_BAR_WIDTH = 200  # Width of health bar in pixels
HEALTH_BAR_HEIGHT = 20  # Height of health bar in pixels

# Progressive Difficulty System
DIFFICULTY_MIN_MULTIPLIER = 1.0  # Starting difficulty multiplier
DIFFICULTY_MAX_MULTIPLIER = 3.0  # Maximum difficulty multiplier at end of game (3x harder)
