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

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Car settings
car_width = 50
car_height = 60
car_x = (screen_width * 0.45)
car_y = (screen_height * 0.8)
car_speed = 0

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

    # Screen background
    screen.fill(white)

    # Draw car
    pygame.draw.rect(screen, red, [car_x, car_y, car_width, car_height])

    # Update display
    pygame.display.update()

pygame.quit()
