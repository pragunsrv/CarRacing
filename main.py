import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 720

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
purple = (128, 0, 128)
gray = (169, 169, 169)
light_gray = (211, 211, 211)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Car settings
car_width = 70
car_height = 80
car_speed = 0
car_types = [
    {"color": red, "speed": 7, "handling": 1.0, "acceleration": 0.2},
    {"color": blue, "speed": 8, "handling": 1.2, "acceleration": 0.25},
    {"color": green, "speed": 9, "handling": 1.5, "acceleration": 0.3}
]
selected_car = car_types[0]
car_upgrades = {"speed": 0, "handling": 0}

# Car Customization
car_customizations = {
    "color": [red, blue, green, yellow],
    "accessories": ["none", "spoiler", "neon_lights", "racing_stripes", "custom_wheels"]
}
car_customization = {"color": red, "accessory": "none"}

# Track settings
tracks = [
    {"bg_color": green, "obstacle_speed": 8, "track_name": "Forest Run"},
    {"bg_color": light_gray, "obstacle_speed": 10, "track_name": "City Streets"},
    {"bg_color": gray, "obstacle_speed": 12, "track_name": "Desert Dash"},
    {"bg_color": black, "obstacle_speed": 15, "track_name": "Night Race"},
    {"bg_color": blue, "obstacle_speed": 18, "track_name": "Ocean Drive"}
]
current_track = 0

# Background
background = pygame.Surface(screen.get_size())
background.fill(tracks[current_track]["bg_color"])

# Obstacle settings
obstacle_width = 70
obstacle_height = 80
obstacle_speed = tracks[current_track]["obstacle_speed"]
obstacle_speed_increment = 0.2
obstacle_types = [(blue, 70, 80), (yellow, 80, 90), (purple, 90, 100)]

# Multiple obstacles
obstacles = []
for i in range(5):
    obstacle_x = random.randrange(0, screen_width - obstacle_width)
    obstacle_y = -screen_height // 2 * (i + 1)
    obstacle_type = random.choice(obstacle_types)
    obstacles.append([obstacle_x, obstacle_y, obstacle_type, random.choice(["static", "moving", "dynamic"])])

# Score, level, lives, and laps
score = 0
level = 1
level_threshold = 15
lives = 3
laps = 0
lap_threshold = 6
font = pygame.font.SysFont(None, 50)

# Pause functionality
paused = False

# Power-up settings
power_up_active = None
power_up_duration = 7000  # in milliseconds
power_up_start_time = 0
power_up_types = ["invincibility", "extra_life", "slow_motion", "speed_boost", "repair"]
power_ups = []
power_up_probability = 0.03

# Game menu
menu = True

# Weather conditions
weather_conditions = ["sunny", "rainy", "foggy", "snowy", "stormy"]
current_weather = random.choice(weather_conditions)

# Player achievements
achievements = {"first_crash": False, "high_score": 0, "first_lap": False, "max_laps": 0}

# Multiplayer settings
multiplayer_mode = False
player2_x, player2_y = screen_width // 2 + 200, screen_height - car_height
player2_speed = 0
player2_car = {"color": yellow, "speed": 7, "handling": 1.0, "acceleration": 0.2}

# AI Opponents
ai_opponents = []
num_ai_opponents = 8
ai_difficulty = 2.5
for i in range(num_ai_opponents):
    ai_car = {
        "x": random.randrange(0, screen_width - car_width),
        "y": random.randrange(-400, -100),
        "speed": random.randint(5, 7),
        "color": purple,
        "handling": 1.2,
    }
    ai_opponents.append(ai_car)

# Dynamic camera
camera_offset = 0
camera_speed = 0.15

# Race Modes
race_modes = ["standard", "time_trial", "championship", "endurance"]
current_mode = "standard"
time_trial_time = 90000  # 90 seconds time trial
time_trial_start_time = 0
championship_race_count = 7
current_championship_race = 0
championship_scores = []
endurance_time = 180000  # 3 minutes endurance
endurance_start_time = 0

# Lap Counting
lap_start_y = screen_height
laps_completed = 0
lap_timer = pygame.time.get_ticks()
lap_times = []

# Split-screen mode
split_screen = False

# Pit Stop settings
pit_stop_zone = pygame.Rect(0, screen_height - 150, screen_width, 150)
in_pit_stop = False
pit_stop_timer = 0
pit_stop_duration = 4000  # 4 seconds

# Function to check for collisions
def check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    if (car_y < obstacle_y + obstacle_height and
        car_y + car_height > obstacle_y and
        car_x < obstacle_x + obstacle_width and
        car_x + car_width > obstacle_x):
        return True
    return False

# Function to display score, level, lives, and laps
def display_score_level_lives_laps(score, level, lives, laps):
    score_text = font.render(f"Score: {score}", True, black)
    level_text = font.render(f"Level: {level}", True, black)
    lives_text = font.render(f"Lives: {lives}", True, black)
    laps_text = font.render(f"Laps: {laps}/{lap_threshold}", True, black)
    screen.blit(score_text, [10, 10])
    screen.blit(level_text, [screen_width // 4, 10])
    screen.blit(lives_text, [screen_width - 200, 10])
    screen.blit(laps_text, [screen_width // 2 + 50, 10])

# Function to display game over
def display_game_over(score):
    large_font = pygame.font.SysFont(None, 100)
    text = large_font.render(f"Game Over! Score: {score}", True, red)
    screen.blit(text, [screen_width // 5, screen_height // 3])
    pygame.display.update()
    pygame.time.wait(2000)

# Function to pause the game
def pause_game():
    global paused
    paused = True
    display_message("Paused", screen_width // 3, screen_height // 3)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        pygame.display.update()

# Function to display messages
def display_message(text, x, y):
    large_font = pygame.font.SysFont(None, 100)
    message = large_font.render(text, True, green)
    screen.blit(message, [x, y])

# Function to increase the level
def increase_level():
    global level, obstacle_speed, current_track, ai_difficulty
    level += 1
    obstacle_speed += obstacle_speed_increment
    ai_difficulty += 0.3
    if level % 15 == 0:  # Change track every 15 levels
        current_track = (current_track + 1) % len(tracks)
        obstacle_speed = tracks[current_track]["obstacle_speed"]
        background.fill(tracks[current_track]["bg_color"])

# Function to handle power-ups
def activate_power_up(power_up):
    global power_up_active, power_up_start_time, lives, selected_car, obstacle_speed
    power_up_active = power_up
    power_up_start_time = pygame.time.get_ticks()
    if power_up == "extra_life":
        lives += 1
        power_up_active = None
    elif power_up == "slow_motion":
        # Slow down the game
        global game_speed
        game_speed *= 0.5
    elif power_up == "speed_boost":
        selected_car["speed"] += 5
    elif power_up == "invincibility":
        # Make car invincible
        pass  # Placeholder for invincibility logic
    elif power_up == "repair":
        # Repair car damage
        pass  # Placeholder for repair logic

# Function to deactivate power-ups
def deactivate_power_up():
    global power_up_active, game_speed, selected_car
    if power_up_active:
        if power_up_active == "slow_motion":
            game_speed *= 2  # Reset game speed
        elif power_up_active == "speed_boost":
            selected_car["speed"] -= 5
        power_up_active = None

# Function to update weather conditions
def update_weather():
    global current_weather
    current_weather = random.choice(weather_conditions)
    if current_weather == "rainy":
        # Adjust game physics for rain
        pass  # Placeholder for rain effects
    elif current_weather == "foggy":
        # Reduce visibility
        pass  # Placeholder for fog effects
    elif current_weather == "snowy":
        # Adjust game physics for snow
        pass  # Placeholder for snow effects
    elif current_weather == "stormy":
        # Add storm effects
        pass  # Placeholder for storm effects

# Function to handle AI behavior
def update_ai_opponents():
    for ai in ai_opponents:
        ai["y"] += ai["speed"] + ai_difficulty
        if ai["y"] > screen_height:
            ai["y"] = -obstacle_height
            ai["x"] = random.randrange(0, screen_width - obstacle_width)
            ai["speed"] = random.randint(5, 7) + ai_difficulty

# Function to check for lap completion
def check_lap_completion(car_y):
    global laps_completed, lap_start_y, lap_timer, lap_times
    if car_y < lap_start_y:
        laps_completed += 1
        lap_time = pygame.time.get_ticks() - lap_timer
        lap_times.append(lap_time)
        lap_timer = pygame.time.get_ticks()
        if laps_completed >= lap_threshold:
            increase_level()

# Main game loop
def game_loop():
    global car_speed, paused, score, level, lives, laps, power_up_active, pit_stop_timer, in_pit_stop, multiplayer_mode, player2_x, player2_y, player2_speed, split_screen
    car_x = screen_width // 2 - car_width // 2
    car_y = screen_height - car_height
    clock = pygame.time.Clock()
    game_speed = 1.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_UP:
                    car_speed = selected_car["speed"]
                if event.key == pygame.K_DOWN:
                    car_speed = -selected_car["speed"]
                if event.key == pygame.K_LEFT:
                    car_x -= selected_car["speed"]
                if event.key == pygame.K_RIGHT:
                    car_x += selected_car["speed"]
                if event.key == pygame.K_m:
                    multiplayer_mode = not multiplayer_mode

        if not paused:
            screen.blit(background, (0, 0))
            # Move car
            car_y -= car_speed * game_speed
            if car_y < -car_height:
                car_y = screen_height

            # Update AI
            update_ai_opponents()

            # Handle collisions with obstacles
            for obstacle in obstacles:
                obstacle_x, obstacle_y, obstacle_color, obstacle_type = obstacle
                obstacle_y += obstacle_speed
                if obstacle_y > screen_height:
                    obstacle_y = -obstacle_height
                    obstacle_x = random.randrange(0, screen_width - obstacle_width)
                pygame.draw.rect(screen, obstacle_color, [obstacle_x, obstacle_y, obstacle_width, obstacle_height])
                if check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
                    lives -= 1
                    if lives <= 0:
                        display_game_over(score)
                        return

            # Update weather
            update_weather()

            # Display score, level, lives, and laps
            display_score_level_lives_laps(score, level, lives, laps)

            # Check for lap completion
            check_lap_completion(car_y)

            # Update display
            pygame.display.update()
            clock.tick(60)  # Frame rate

game_loop()
pygame.quit()
