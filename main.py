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

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Car settings
car_width = 50
car_height = 60
car_x = (screen_width * 0.45)
car_y = (screen_height * 0.8)
car_speed = 0

# Obstacle settings
obstacle_width = 50
obstacle_height = 60
obstacle_x = random.randrange(0, screen_width - obstacle_width)
obstacle_y = -600
obstacle_speed = 7
obstacle_speed_increment = 0.01

# Score
score = 0
font = pygame.font.SysFont(None, 35)

# Function to check for collisions
def check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    if (car_y < obstacle_y + obstacle_height and
        car_y + car_height > obstacle_y and
        car_x < obstacle_x + obstacle_width and
        car_x + car_width > obstacle_x):
        return True
    return False

# Function to display the score
def display_score(score):
    text = font.render(f"Score: {score}", True, black)
    screen.blit(text, [10, 10])

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car_speed = 0

    car_x += car_speed

    # Update obstacle position
    obstacle_y += obstacle_speed

    # Reset obstacle when it goes off screen
    if obstacle_y > screen_height:
        obstacle_y = 0 - obstacle_height
        obstacle_x = random.randrange(0, screen_width - obstacle_width)
        score += 1
        obstacle_speed += obstacle_speed_increment

    # Check for collision
    if check_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
        running = False

    # Screen background
    screen.fill(white)

    # Draw car
    pygame.draw.rect(screen, red, [car_x, car_y, car_width, car_height])

    # Draw obstacle
    pygame.draw.rect(screen, blue, [obstacle_x, obstacle_y, obstacle_width, obstacle_height])

    # Display score
    display_score(score)

    # Update display
    pygame.display.update()

pygame.quit()
