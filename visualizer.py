import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Input Feedback Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 74)

# Input storage
input_text = ""

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                # Clear the input on Enter
                input_text = ""
            else:
                # Add character to the input text
                input_text += event.unicode

    # Fill the screen with a background color
    screen.fill(WHITE)

    # Render the text
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (50, 250))  # Position the text

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
