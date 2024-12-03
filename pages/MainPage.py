import pygame
from classes.Button import Button
from settings import *
import sys




class MainPage:
    def __init__(self, screen, track):
        self.track = track
        self.screen = screen
        self.button_width = 400
        self.button_height = 60
        self.button_offset = 400
        self.draw_button = Button((SCREEN_WIDTH-self.button_width) / 2 + self.button_offset, 100, self.button_width, self.button_height, "Draw Track", FONT, WHITE, ORANGE, PASTEL_ORANGE)
        self.settings_button = Button((SCREEN_WIDTH-self.button_width) / 2 + self.button_offset, 200, self.button_width, self.button_height, "Load Track", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.calculate_button = Button((SCREEN_WIDTH-self.button_width) / 2 + self.button_offset, 300, self.button_width, self.button_height, "Calculate Racing Line", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.simulate_button = Button((SCREEN_WIDTH-self.button_width) / 2 + self.button_offset, 400, self.button_width, self.button_height, "Simulate", FONT, WHITE, LIGHT_GRAY, LIGHT_GRAY)
        self.quit_button = Button((SCREEN_WIDTH-self.button_width) / 2 + self.button_offset, 500, self.button_width, self.button_height, "Quit", FONT, WHITE, RED, LIGHT_RED)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        draw_text("Racing Line Generator", FONT, BLACK, self.screen, (SCREEN_WIDTH) / 2 + self.button_offset , 50)
        draw_text("Current Track", FONT, BLACK, self.screen, (SCREEN_WIDTH) / 2 - 300 , 50)
        self.draw_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.simulate_button.draw(self.screen)
        self.calculate_button.draw(self.screen)
        self.track.draw_track_preview(self.screen, 40, 100, 600)

    def handle_events(self):
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = any(event.type == pygame.MOUSEBUTTONDOWN for event in pygame.event.get())

        self.draw_button.check_hover(mouse_pos)
        self.settings_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        self.simulate_button.check_hover(mouse_pos)
        self.calculate_button.check_hover(mouse_pos)

        if self.draw_button.is_clicked(mouse_pos, mouse_click):
            return 'draw_track'
        elif self.settings_button.is_clicked(mouse_pos, mouse_click):
            return 'test'
        elif self.quit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        return 'main_menu'

    def update(self):
        pass

def draw_text(text, font, color, surface, x, y):
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
