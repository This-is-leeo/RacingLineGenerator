import pygame
import sys

class DrawTrack():
    def __init__(self, screen, track):
        self.screen = screen
        self.track = track


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add points to the track with left click
                if event.button == 1:
                    x, y = event.pos
                    self.track.add_point(x, y)
                # Remove the last point with right click
                elif event.button == 3 and self.track.points:
                    self.track.remove_point(-1)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_page'
                if event.key == pygame.K_s:
                    self.track.save_track()
        return 'draw_track'
    
    def update(self):
        pass

    def draw(self):
        font = pygame.font.Font(None, 36)
        self.track.draw(self.screen)
        length_text = font.render(f"Track Length: {self.track.calculate_length():.2f} units", True, (0, 0, 0))
        self.screen.blit(length_text, (10, 10))



        
    
