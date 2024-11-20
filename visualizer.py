import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Example")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Circle properties
circle_x, circle_y = width // 2, height // 2
circle_radius = 30
circle_speed = 5

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Movement logic (circle moves to the right)
    circle_x += circle_speed
    if circle_x > width:
        circle_x = -circle_radius  # Reset position when it goes off-screen
    
    # Clear screen
    screen.fill(white)
    
    # Draw the circle
    pygame.draw.circle(screen, blue, (circle_x, circle_y), circle_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)
