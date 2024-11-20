import pygame
import math

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

# Example usage with Pygame
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Racetrack Example")
    clock = pygame.time.Clock()

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

        # Draw everything
        screen.fill((255, 255, 255))
        track.draw(screen)
        
        # Display the track length
        font = pygame.font.Font(None, 36)
        length_text = font.render(f"Track Length: {track.calculate_length():.2f} units", True, (0, 0, 0))
        screen.blit(length_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
