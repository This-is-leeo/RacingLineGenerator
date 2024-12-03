import pygame
from settings import *
import sys
from classes.Button import Button

class DrawTrack():
    def __init__(self, screen, track):
        self.screen = screen
        self.track = track
        self.back_button = Button(10, 10, 200, 60, "Back", FONT, WHITE, ORANGE, PASTEL_ORANGE)
        self.save_button = Button(10, 80, 200, 60, "Save", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.spline_button = Button(10, 150, 200, 60, "Calculate Track", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.reset_button = Button(10, 220, 200, 60, "Reset", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.width_changed = False


    def handle_events(self):

        mouse_pos = pygame.mouse.get_pos()

        self.save_button.check_hover(mouse_pos)
        self.back_button.check_hover(mouse_pos)
        self.spline_button.check_hover(mouse_pos)
        self.reset_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Add points to the track with left click
                if self.back_button.is_clicked(mouse_pos, event.button == 1):
                    return 'main_menu'
                elif self.save_button.is_clicked(mouse_pos, event.button == 1):
                    self.track.save_track("testasda.txt")
                    return 'main_menu'
                elif self.spline_button.is_clicked(mouse_pos, event.button == 1):
                    if len(self.track.guide_points) < 2:
                        draw_text("Not Enought Point!", FONT, RED, self.screen, (SCREEN_WIDTH) / 2, 100)
                        #this does not work!
                    else:
                        self.track.centerline_spline = self.track.generate_centerline_spline()
                        self.track.inner_line, self.track.outer_line = self.track.generate_boundaries()
                    self.track.draw_spline = True
                    #TODO fix this bug here lol
                elif self.reset_button.is_clicked(mouse_pos, event.button == 1):
                    self.track.guide_points = []
                    self.track.centerline_spline = []
                    self.track.inner_line = []
                    self.track.outer_line = []
                    self.track.draw_spline = False
                    

                elif event.button == 1:
                    x, y = event.pos
                    self.track.add_point(x, y)
                # Remove the last point with right click
                elif event.button == 3 and self.track.guide_points:
                    self.track.remove_point(-1)
                
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'
                if event.key == pygame.K_a:
                    self.track.track_width += 4 if self.track.track_width < 100 else 0
                    self.width_changed = True
                if event.key == pygame.K_d:
                    self.track.track_width -= 4 if self.track.track_width > 10 else 0
                    self.width_changed = True
                    

        return 'draw_track'
    
    def update(self):
        #update button colors
        if len(self.track.guide_points) > 2:
            self.spline_button.button_color = ORANGE
            self.spline_button.hover_color = PASTEL_ORANGE
        else:
            self.spline_button.button_color = LIGHT_GRAY
            self.spline_button.hover_color = LIGHT_GRAY
        if len(self.track.guide_points) > 0:
            self.reset_button.button_color = ORANGE
            self.reset_button.hover_color = PASTEL_ORANGE
        else:
            self.reset_button.button_color = LIGHT_GRAY
            self.reset_button.hover_color = LIGHT_GRAY
        if self.track.draw_spline:
            self.save_button.button_color = ORANGE
            self.save_button.hover_color = PASTEL_ORANGE
        else:
            self.save_button.button_color = LIGHT_GRAY
            self.save_button.hover_color = LIGHT_GRAY    


        #rerenders the track if width got changed
        if self.width_changed and self.track.draw_spline:
            self.width_changed = not self.width_changed
            self.track.inner_line, self.track.outer_line = self.track.generate_boundaries()


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 36)
        self.track.draw(self.screen)

        self.save_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.spline_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        # length_text = font.render(f"Track Length: {self.track.calculate_length():.2f} units", True, (100, 100, 100))
        # self.screen.blit(length_text, (10, 10))

        

def draw_text(text, font, color, surface, x, y):
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

        
    
