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

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Car settings
car_width = 50
car_height = 60
car_x = (screen_width * 0.45)
car_y = (screen_height * 0.8)
car_speed = 0

# Background
background = pygame.Surface(screen.get_size())
background.fill(green)

# Obstacle settings
obstacle_width = 50
obstacle_height = 60
obstacle_speed = 7
obstacle_speed_increment = 0.02
obstacle_types = [(blue, 50, 60), (yellow, 60, 70)]  # Different obstacle colors and sizes

# Multiple obstacles
obstacles = []
for i in range(3):  # Increase the number of obstacles to 3
    obstacle_x = random.randrange(0, screen_width - obstacle_width)
    obstacle_y = -600 * (i + 1)
    obstacle_type = random.choice(obstacle_types)
    obstacles.append([obstacle_x, obstacle_y, obstacle_type])

# Score and level
score = 0
level = 1
level_threshold = 5
font = pygame.font.SysFont(None, 35)

# Pause functionality
paused = False

# Function to check for collisions
def check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    if (car_y < obstacle_y + obstacle_height and
        car_y + car_height > obstacle_y and
        car_x < obstacle_x + obstacle_width and
        car_x + car_width > obstacle_x):
        return True
    return False

# Function to display the score and level
def display_score_and_level(score, level):
    score_text = font.render(f"Score: {score}", True, black)
    level_text = font.render(f"Level: {level}", True, black)
    screen.blit(score_text, [10, 10])
    screen.blit(level_text, [screen_width - 120, 10])

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
    global level, obstacle_speed
    level += 1
    obstacle_speed += 2

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Car movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_speed = -5
            if event.key == pygame.K_RIGHT:
                car_speed = 5
            if event.key == pygame.K_p:
                pause_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car_speed = 0

    car_x += car_speed

    # Update obstacle positions
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed

        # Reset obstacle when it goes off screen
        if obstacle[1] > screen_height:
            obstacle[1] = 0 - obstacle[2][1]
            obstacle[0] = random.randrange(0, screen_width - obstacle[2][1])
            obstacle[2] = random.choice(obstacle_types)
            score += 1

            # Increase level
            if score % level_threshold == 0:
                increase_level()

        # Check for collision
        if check_collision(car_x, car_y, obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]):
            display_game_over(score)
            running = False

    # Screen background
    screen.blit(background, (0, 0))

    # Draw car
    pygame.draw.rect(screen, red, [car_x, car_y, car_width, car_height])

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle[2][0], [obstacle[0], obstacle[1], obstacle[2][1], obstacle[2][2]])

    # Display score and level
    display_score_and_level(score, level)

    # Update display
    pygame.display.update()

pygame.quit()
