import pygame
import math
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

class Racetrack:
    def __init__(self):
        """Initialize an empty list of track points."""
        self.points = []

    def add_point(self, x, y):
        """Add a new point to the racetrack."""
        self.points.append((x, y))

    def modify_point(self, index, x, y):
        """Modify an existing point by index."""
        if 0 <= index < len(self.points):
            self.points[index] = (x, y)
        else:
            print(f"Invalid index: {index}")

    def remove_point(self, index):
        """Remove a point by index."""
        if 0 <= index < len(self.points):
            self.points.pop(index)
        else:
            print(f"Invalid index: {index}")

    def draw(self, screen):
        """Visualize the racetrack."""
        if len(self.points) > 1:
            pygame.draw.lines(screen, (255, 0, 0), True, self.points, 3)
        for point in self.points:
            pygame.draw.circle(screen, (0, 0, 255), point, 5)

    def calculate_length(self):
        """Calculate the approximate length of the racetrack."""
        if len(self.points) < 2:
            return 0
        length = 0
        for i in range(len(self.points)):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % len(self.points)]
            length += math.hypot(x2 - x1, y2 - y1)
        return length
    
    def save_track(self, file_name = 'test.txt'):
        with open(os.path.join(current_folder, file_name), 'w') as output:
            for i in range(len(self.points)):
                output_text = str(self.points[i][0]) + ' ' + str(self.points[i][1]) + '\n'
                output.write(output_text)
    
    
        

# Example usage with Pygame
if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h


# Set up the display in fullscreen borderless mode
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Racetrack Example")
    clock = pygame.time.Clock()
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (170, 170, 170)

    # Font
    font = pygame.font.Font(None, 36)

    # Button properties
    button_color = GRAY
    button_hover_color = LIGHT_GRAY
    button_rect = pygame.Rect(100, 100, 200, 50)  # (x, y, width, height)
    button_text = font.render("Click Me", True, BLACK)

    track = Racetrack()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add points to the track with left click
                if event.button == 1:
                    x, y = event.pos
                    track.add_point(x, y)
                # Remove the last point with right click
                elif event.button == 3 and track.points:
                    track.remove_point(-1)
                if button_rect.collidepoint(event.pos):
                    print("Button clicked!")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_s:
                    track.save_track()

            
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
        # Draw everything
        
        track.draw(screen)
        
        # Display the track length
        font = pygame.font.Font(None, 36)
        length_text = font.render(f"Track Length: {track.calculate_length():.2f} units", True, (0, 0, 0))
        screen.blit(length_text, (10, 10))

        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(60)
    print(track.points)
    pygame.quit()
