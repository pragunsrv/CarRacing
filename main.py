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
    "accessories": ["none", "spoiler", "neon_lights"]
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
        obstacle_speed /= 2
    elif power_up == "speed_boost":
        selected_car["speed"] += 3
    elif power_up == "repair":
        lives += 1

def deactivate_power_up():
    global power_up_active, obstacle_speed, selected_car
    if power_up_active == "slow_motion":
        obstacle_speed *= 2
    elif power_up_active == "speed_boost":
        selected_car["speed"] -= 3
    power_up_active = None

# Function to generate power-ups
def generate_power_up():
    if random.random() < power_up_probability:
        power_up_x = random.randrange(0, screen_width - 30)
        power_up_y = -30
        power_up_type = random.choice(power_up_types)
        power_ups.append([power_up_x, power_up_y, power_up_type])

# Function to draw power-ups
def draw_power_up(power_up):
    color = white
    if power_up[2] == "invincibility":
        color = yellow
    elif power_up[2] == "extra_life":
        color = red
    elif power_up[2] == "slow_motion":
        color = blue
    elif power_up[2] == "speed_boost":
        color = green
    elif power_up[2] == "repair":
        color = light_gray
    pygame.draw.rect(screen, color, (power_up[0], power_up[1], 30, 30))
    pygame.draw.circle(screen, white, (power_up[0] + 15, power_up[1] + 15), 10)

# Function to upgrade car
def upgrade_car(upgrade_type):
    global car_upgrades
    if upgrade_type == "speed":
        car_upgrades["speed"] += 1
    elif upgrade_type == "handling":
        car_upgrades["handling"] += 1
    display_message(f"{upgrade_type.capitalize()} Upgraded!", screen_width // 3, screen_height // 3 + 100)
    pygame.display.update()
    pygame.time.wait(2000)

# Function to update obstacle behavior
def update_obstacle_ai(obstacle):
    if obstacle[3] == "moving":
        obstacle[0] += random.choice([-1, 1]) * random.randint(1, 3)
    elif obstacle[3] == "dynamic":
        obstacle[0] += random.choice([-2, 2])
        obstacle[1] += random.choice([-2, 2])
        if obstacle[0] < 0 or obstacle[0] > screen_width - obstacle_width:
            obstacle[0] = max(0, min(obstacle[0], screen_width - obstacle_width))
        if obstacle[1] < 0 or obstacle[1] > screen_height:
            obstacle[1] = max(0, min(obstacle[1], screen_height))

# Function to update AI opponent behavior
def update_ai_opponents():
    global laps
    for ai_car in ai_opponents:
        ai_car["y"] += ai_car["speed"] + ai_difficulty
        if ai_car["y"] > screen_height:
            ai_car["y"] = random.randrange(-300, -100)
            ai_car["x"] = random.randrange(0, screen_width - car_width)
            laps += 1

        # Move AI cars towards player
        if ai_car["x"] < car_x:
            ai_car["x"] += ai_car["handling"]
        elif ai_car["x"] > car_x:
            ai_car["x"] -= ai_car["handling"]

        # AI overtaking logic
        if ai_car["y"] > car_y and ai_car["x"] < car_x:
            ai_car["x"] += ai_car["handling"] * 2
        elif ai_car["y"] > car_y and ai_car["x"] > car_x:
            ai_car["x"] -= ai_car["handling"] * 2

        # AI blocking logic
        if ai_car["y"] < car_y and ai_car["x"] > car_x - car_width and ai_car["x"] < car_x + car_width:
            ai_car["speed"] += 0.5  # Speed up to block the player

# Function to handle weather effects
def apply_weather_effects():
    global car_speed, obstacle_speed
    if current_weather == "rainy":
        car_speed *= 0.9
        obstacle_speed *= 0.9
    elif current_weather == "foggy":
        obstacle_speed *= 0.8
    elif current_weather == "snowy":
        car_speed *= 0.8
        obstacle_speed *= 0.7
    elif current_weather == "stormy":
        car_speed *= 0.7
        obstacle_speed *= 0.6

# Function to check and update achievements
def update_achievements():
    global achievements
    if not achievements["first_crash"] and lives < 3:
        achievements["first_crash"] = True
        display_message("Achievement Unlocked: First Crash!", screen_width // 3, screen_height // 3 + 100)
        pygame.display.update()
        pygame.time.wait(2000)

    if score > achievements["high_score"]:
        achievements["high_score"] = score
        display_message("Achievement Unlocked: High Score!", screen_width // 3, screen_height // 3 + 150)
        pygame.display.update()
        pygame.time.wait(2000)

    if laps > achievements["max_laps"]:
        achievements["max_laps"] = laps
        display_message("Achievement Unlocked: Max Laps!", screen_width // 3, screen_height // 3 + 150)
        pygame.display.update()
        pygame.time.wait(2000)

# Game Menu
def show_menu():
    global multiplayer_mode, current_mode, current_track, split_screen
    menu = True
    while menu:
        screen.fill(white)
        display_message("Car Racing Game", screen_width // 5, screen_height // 4)
        display_message("Press Enter to Start", screen_width // 5, screen_height // 2)
        display_message("Press C to Change Car", screen_width // 5, screen_height // 2 + 50)
        display_message("Press W to Change Weather", screen_width // 5, screen_height // 2 + 100)
        display_message("Press T for Time Trial Mode", screen_width // 5, screen_height // 2 + 150)
        display_message("Press M for Multiplayer", screen_width // 5, screen_height // 2 + 200)
        display_message("Press R to Change Track", screen_width // 5, screen_height // 2 + 250)
        display_message("Press S for Split-Screen", screen_width // 5, screen_height // 2 + 300)
        display_message("Press H for Championship Mode", screen_width // 5, screen_height // 2 + 350)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                if event.key == pygame.K_c:
                    change_car_type()
                if event.key == pygame.K_w:
                    change_weather()
                if event.key == pygame.K_t:
                    current_mode = "time_trial"
                if event.key == pygame.K_m:
                    multiplayer_mode = not multiplayer_mode
                    display_message("Multiplayer Mode: " + ("On" if multiplayer_mode else "Off"), screen_width // 3, screen_height // 2 + 400)
                    pygame.display.update()
                    pygame.time.wait(1000)
                if event.key == pygame.K_r:
                    current_track = (current_track + 1) % len(tracks)
                    background.fill(tracks[current_track]["bg_color"])
                if event.key == pygame.K_s:
                    split_screen = not split_screen
                    display_message("Split-Screen Mode: " + ("On" if split_screen else "Off"), screen_width // 3, screen_height // 2 + 450)
                    pygame.display.update()
                    pygame.time.wait(1000)
                if event.key == pygame.K_h:
                    current_mode = "championship"

def show_upgrade_menu():
    global car_upgrades
    upgrading = True
    while upgrading:
        screen.fill(white)
        display_message("Upgrade Menu", screen_width // 3, screen_height // 4)
        display_message("Press S to Upgrade Speed", screen_width // 3, screen_height // 2)
        display_message("Press H to Upgrade Handling", screen_width // 3, screen_height // 2 + 50)
        display_message("Press ESC to Return", screen_width // 3, screen_height // 2 + 100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    upgrade_car("speed")
                if event.key == pygame.K_h:
                    upgrade_car("handling")
                if event.key == pygame.K_ESCAPE:
                    upgrading = False

def change_car_type():
    global selected_car
    car_types_cycle = car_types.copy()
    car_types_cycle.append(car_types_cycle.pop(0))
    selected_car = car_types_cycle[0]

def change_weather():
    global current_weather
    weather_conditions_cycle = weather_conditions.copy()
    weather_conditions_cycle.append(weather_conditions_cycle.pop(0))
    current_weather = weather_conditions_cycle[0]

# Start Game
show_menu()

car_x, car_y = screen_width // 2 - car_width // 2, screen_height - car_height
player2_x, player2_y = screen_width // 2 + 100, screen_height - car_height
car_speed = 0
player2_speed = 0

if current_mode == "time_trial":
    time_trial_start_time = pygame.time.get_ticks()
if current_mode == "championship":
    championship_scores = []
if current_mode == "endurance":
    endurance_start_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_game()
            if event.key == pygame.K_UP:
                car_speed = selected_car["speed"] + car_upgrades["speed"]
            if event.key == pygame.K_DOWN:
                car_speed = 0
            if event.key == pygame.K_LEFT:
                car_x -= selected_car["handling"]
            if event.key == pygame.K_RIGHT:
                car_x += selected_car["handling"]
            if event.key == pygame.K_d:
                player2_speed = player2_car["speed"]
            if event.key == pygame.K_w:
                player2_speed = 0
            if event.key == pygame.K_u:
                show_upgrade_menu()

    if not paused:
        # Move player car
        car_x += car_speed
        if car_x < 0:
            car_x = 0
        if car_x > screen_width - car_width:
            car_x = screen_width - car_width

        # Move player 2 car
        if multiplayer_mode:
            player2_x += player2_speed
            if player2_x < 0:
                player2_x = 0
            if player2_x > screen_width - car_width:
                player2_x = screen_width - car_width

        # Move obstacles and check for collisions
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            update_obstacle_ai(obstacle)
            if obstacle[1] > screen_height:
                obstacle[1] = random.randrange(-300, -100)
                obstacle[0] = random.randrange(0, screen_width - obstacle_width)
            if check_collision(car_x, car_y, obstacle[0], obstacle[1], obstacle_width, obstacle_height):
                lives -= 1
                obstacles.remove(obstacle)
                if lives == 0:
                    display_game_over(score)
                    running = False

        # Update AI Opponents
        update_ai_opponents()

        # Check lap counting
        if car_y < lap_start_y - screen_height:
            laps_completed += 1
            lap_times.append(pygame.time.get_ticks() - lap_timer)
            lap_timer = pygame.time.get_ticks()
            if laps_completed >= lap_threshold:
                display_game_over(score)
                running = False

        # Check if time trial mode is over
        if current_mode == "time_trial" and pygame.time.get_ticks() - time_trial_start_time > time_trial_time:
            display_game_over(score)
            running = False

        # Check championship mode
        if current_mode == "championship":
            if current_championship_race < championship_race_count:
                # Perform championship race logic
                pass  # This is a placeholder for additional championship logic
            else:
                # End of championship
                display_message(f"Championship Complete! Final Score: {score}", screen_width // 5, screen_height // 3)
                pygame.display.update()
                pygame.time.wait(2000)
                running = False

        # Check endurance mode
        if current_mode == "endurance" and pygame.time.get_ticks() - endurance_start_time > endurance_time:
            display_game_over(score)
            running = False

        # Apply weather effects
        apply_weather_effects()

        # Power-up logic
        generate_power_up()
        for power_up in power_ups:
            power_up[1] += 5  # Power-up falling speed
            draw_power_up(power_up)
            if check_collision(car_x, car_y, power_up[0], power_up[1], 30, 30):
                activate_power_up(power_up[2])
                power_ups.remove(power_up)
            elif power_up[1] > screen_height:
                power_ups.remove(power_up)

        if power_up_active:
            if pygame.time.get_ticks() - power_up_start_time > power_up_duration:
                deactivate_power_up()

        # Pit Stop logic
        if pit_stop_zone.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)):
            if not in_pit_stop:
                in_pit_stop = True
                pit_stop_timer = pygame.time.get_ticks()
                car_speed = 0
                display_message("In Pit Stop", screen_width // 3, screen_height // 2)
                pygame.display.update()
                pygame.time.wait(pit_stop_duration)
                car_speed = selected_car["speed"] + car_upgrades["speed"]
                in_pit_stop = False

        # Drawing everything
        screen.blit(background, (0, -camera_offset))
        pygame.draw.rect(screen, selected_car["color"], [car_x, car_y, car_width, car_height])
        if multiplayer_mode:
            pygame.draw.rect(screen, player2_car["color"], [player2_x, player2_y, car_width, car_height])

        for obstacle in obstacles:
            pygame.draw.rect(screen, obstacle[2][0], [obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]])

        # Draw AI opponents
        for ai_car in ai_opponents:
            pygame.draw.rect(screen, ai_car["color"], [ai_car["x"], ai_car["y"], car_width, car_height])

        # Display lap counter
        display_score_level_lives_laps(score, level, lives, laps_completed)

        # Update achievements
        update_achievements()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

pygame.quit()
