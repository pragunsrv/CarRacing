import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

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
car_width = 50
car_height = 60
car_speed = 0
car_types = [
    {"color": red, "speed": 5, "handling": 1.0, "acceleration": 0.1},  # Car type 1
    {"color": blue, "speed": 6, "handling": 1.2, "acceleration": 0.15},  # Car type 2
    {"color": green, "speed": 7, "handling": 1.5, "acceleration": 0.2}  # Car type 3
]
selected_car = car_types[0]  # Default car type
car_upgrades = {"speed": 0, "handling": 0}

# Car Customization
car_customizations = {
    "color": [red, blue, green, yellow],
    "accessories": ["none", "spoiler", "neon_lights"]
}
car_customization = {"color": red, "accessory": "none"}

# Track settings
tracks = [
    {"bg_color": green, "obstacle_speed": 7},  # Track 1
    {"bg_color": light_gray, "obstacle_speed": 9},  # Track 2
    {"bg_color": gray, "obstacle_speed": 11}  # Track 3
]
current_track = 0

# Background
background = pygame.Surface(screen.get_size())
background.fill(tracks[current_track]["bg_color"])

# Obstacle settings
obstacle_width = 50
obstacle_height = 60
obstacle_speed = tracks[current_track]["obstacle_speed"]
obstacle_speed_increment = 0.05
obstacle_types = [(blue, 50, 60), (yellow, 60, 70)]  # Different obstacle colors and sizes

# Multiple obstacles
obstacles = []
for i in range(3):
    obstacle_x = random.randrange(0, screen_width - obstacle_width)
    obstacle_y = -600 * (i + 1)
    obstacle_type = random.choice(obstacle_types)
    obstacles.append([obstacle_x, obstacle_y, obstacle_type, random.choice(["static", "moving", "dynamic"])])
    
# Score, level, and lives
score = 0
level = 1
level_threshold = 5
lives = 3
font = pygame.font.SysFont(None, 35)

# Pause functionality
paused = False

# Power-up settings
power_up_active = None
power_up_duration = 5000  # in milliseconds
power_up_start_time = 0
power_up_types = ["invincibility", "extra_life", "slow_motion", "speed_boost"]
power_ups = []
power_up_probability = 0.01

# Game menu
menu = True

# Weather conditions
weather_conditions = ["sunny", "rainy"]
current_weather = random.choice(weather_conditions)

# Player achievements
achievements = {"first_crash": False, "high_score": 0}

# Multiplayer settings
multiplayer_mode = False
player2_x, player2_y = screen_width // 2 + 100, screen_height - car_height
player2_speed = 0
player2_car = {"color": yellow, "speed": 5, "handling": 1.0, "acceleration": 0.1}

# Function to check for collisions
def check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    if (car_y < obstacle_y + obstacle_height and
        car_y + car_height > obstacle_y and
        car_x < obstacle_x + obstacle_width and
        car_x + car_width > obstacle_x):
        return True
    return False

# Function to display score, level, and lives
def display_score_level_lives(score, level, lives):
    score_text = font.render(f"Score: {score}", True, black)
    level_text = font.render(f"Level: {level}", True, black)
    lives_text = font.render(f"Lives: {lives}", True, black)
    screen.blit(score_text, [10, 10])
    screen.blit(level_text, [screen_width // 2 - 50, 10])
    screen.blit(lives_text, [screen_width - 120, 10])

# Function to display game over
def display_game_over(score):
    large_font = pygame.font.SysFont(None, 75)
    text = large_font.render(f"Game Over! Score: {score}", True, red)
    screen.blit(text, [screen_width // 8, screen_height // 3])
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
    large_font = pygame.font.SysFont(None, 75)
    message = large_font.render(text, True, green)
    screen.blit(message, [x, y])

# Function to increase the level
def increase_level():
    global level, obstacle_speed, current_track
    level += 1
    obstacle_speed += obstacle_speed_increment
    if level % 10 == 0:  # Change track every 10 levels
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
        power_up_active = None  # Extra life power-up is instantaneous
    elif power_up == "slow_motion":
        obstacle_speed /= 2
    elif power_up == "speed_boost":
        selected_car["speed"] += 2

def deactivate_power_up():
    global power_up_active, obstacle_speed, selected_car
    if power_up_active == "slow_motion":
        obstacle_speed *= 2
    elif power_up_active == "speed_boost":
        selected_car["speed"] -= 2
    power_up_active = None

# Function to generate power-ups randomly
def generate_power_up():
    if random.random() < power_up_probability:
        power_up_x = random.randrange(0, screen_width - 30)
        power_up_y = -30
        power_up_type = random.choice(power_up_types)
        power_ups.append([power_up_x, power_up_y, power_up_type])

# Function to draw power-ups
def draw_power_up(power_up):
    if power_up[2] == "invincibility":
        pygame.draw.circle(screen, purple, (power_up[0], power_up[1]), 15)
    elif power_up[2] == "extra_life":
        pygame.draw.circle(screen, yellow, (power_up[0], power_up[1]), 15)
    elif power_up[2] == "slow_motion":
        pygame.draw.circle(screen, gray, (power_up[0], power_up[1]), 15)
    elif power_up[2] == "speed_boost":
        pygame.draw.circle(screen, blue, (power_up[0], power_up[1]), 15)

# Function to upgrade the car
def upgrade_car(upgrade_type):
    global car_upgrades
    if upgrade_type == "speed":
        car_upgrades["speed"] += 1
    elif upgrade_type == "handling":
        car_upgrades["handling"] += 0.1

    # Apply upgrades
    selected_car["speed"] += car_upgrades["speed"]
    selected_car["handling"] += car_upgrades["handling"]

# Function to enhance obstacle AI
def update_obstacle_ai(obstacle):
    if obstacle[3] == "moving":
        obstacle[0] += random.choice([-3, 3])  # Horizontal movement
        if obstacle[0] < 0 or obstacle[0] > screen_width - obstacle_width:
            obstacle[0] = max(0, min(obstacle[0], screen_width - obstacle_width))
    elif obstacle[3] == "dynamic":
        obstacle[0] += random.choice([-2, 2])
        obstacle[1] += random.choice([-2, 2])
        if obstacle[0] < 0 or obstacle[0] > screen_width - obstacle_width:
            obstacle[0] = max(0, min(obstacle[0], screen_width - obstacle_width))
        if obstacle[1] < 0 or obstacle[1] > screen_height:
            obstacle[1] = max(0, min(obstacle[1], screen_height))

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

# Game Menu
def show_menu():
    global multiplayer_mode
    menu = True
    while menu:
        screen.fill(white)
        display_message("Car Racing Game", screen_width // 5, screen_height // 4)
        display_message("Press Enter to Start", screen_width // 5, screen_height // 2)
        display_message("Press C to Change Car", screen_width // 5, screen_height // 2 + 50)
        display_message("Press W to Change Weather", screen_width // 5, screen_height // 2 + 100)
        display_message("Press U to Upgrade Car", screen_width // 5, screen_height // 2 + 150)
        display_message("Press M for Multiplayer", screen_width // 5, screen_height // 2 + 200)
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
                if event.key == pygame.K_u:
                    show_upgrade_menu()
                if event.key == pygame.K_m:
                    multiplayer_mode = not multiplayer_mode
                    display_message("Multiplayer Mode: " + ("On" if multiplayer_mode else "Off"), screen_width // 3, screen_height // 2 + 250)
                    pygame.display.update()
                    pygame.time.wait(1000)

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Car movement for player 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_speed = -selected_car["speed"]
            if event.key == pygame.K_RIGHT:
                car_speed = selected_car["speed"]
            if event.key == pygame.K_p:
                pause_game()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car_speed = 0

        # Car movement for player 2 (multiplayer mode)
        if multiplayer_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player2_speed = -player2_car["speed"]
            if keys[pygame.K_d]:
                player2_speed = player2_car["speed"]
            if keys[pygame.K_w]:
                player2_speed = 0
            if keys[pygame.K_s]:
                player2_speed = 0

    # Update player positions
    car_x += car_speed
    player2_x += player2_speed

    # Boundary checking
    if car_x < 0:
        car_x = 0
    if car_x > screen_width - car_width:
        car_x = screen_width - car_width
    if player2_x < 0:
        player2_x = 0
    if player2_x > screen_width - car_width:
        player2_x = screen_width - car_width

    # Update obstacle positions and movement patterns
    for obstacle in obstacles:
        update_obstacle_ai(obstacle)
        obstacle[1] += obstacle_speed

        # Reset obstacle when it goes off screen
        if obstacle[1] > screen_height:
            obstacle[1] = 0 - obstacle[2][1]
            obstacle[0] = random.randrange(0, screen_width - obstacle[2][1])
            obstacle[2] = random.choice(obstacle_types)
            obstacle[3] = random.choice(["static", "moving", "dynamic"])
            score += 1

            # Increase level
            if score % level_threshold == 0:
                increase_level()

        # Check for collision with player 1
        if not power_up_active == "invincibility" and check_collision(car_x, car_y, obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]):
            lives -= 1
            update_achievements()
            if lives == 0:
                display_game_over(score)
                running = False
            else:
                obstacle[1] = screen_height  # Move the obstacle off the screen

        # Check for collision with player 2
        if multiplayer_mode and not power_up_active == "invincibility" and check_collision(player2_x, player2_y, obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]):
            lives -= 1
            update_achievements()
            if lives == 0:
                display_game_over(score)
                running = False
            else:
                obstacle[1] = screen_height  # Move the obstacle off the screen

    # Generate and update power-ups
    generate_power_up()
    for power_up in power_ups:
        power_up[1] += 5
        if power_up[1] > screen_height:
            power_ups.remove(power_up)
        elif check_collision(car_x, car_y, power_up[0], power_up[1], 30, 30):
            activate_power_up(power_up[2])
            power_ups.remove(power_up)
        elif multiplayer_mode and check_collision(player2_x, player2_y, power_up[0], power_up[1], 30, 30):
            activate_power_up(power_up[2])
            power_ups.remove(power_up)

    # Handle power-up activation
    if power_up_active and pygame.time.get_ticks() - power_up_start_time > power_up_duration:
        deactivate_power_up()

    # Screen background
    background.fill(tracks[current_track]["bg_color"])
    screen.blit(background, (0, 0))

    # Draw cars
    pygame.draw.rect(screen, selected_car["color"], [car_x, car_y, car_width, car_height])
    pygame.draw.rect(screen, player2_car["color"], [player2_x, player2_y, car_width, car_height]) if multiplayer_mode else None

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle[2][0], [obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]])

    # Draw power-ups
    for power_up in power_ups:
        draw_power_up(power_up)

    # Display score, level, and lives
    display_score_level_lives(score, level, lives)

    # Update display
    pygame.display.update()

pygame.quit()
