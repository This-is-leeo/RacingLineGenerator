import pygame
from classes.Button import Button
from settings import *
import sys




class MainPage:
    def __init__(self, screen, track):
        self.track = track
        self.screen = screen
        self.play_button = Button(300, 200, 200, 60, "Play", FONT, WHITE, BLUE, LIGHT_BLUE)
        self.settings_button = Button(300, 300, 200, 60, "Settings", FONT, WHITE, BLUE, LIGHT_BLUE)
        self.quit_button = Button(300, 400, 200, 60, "Quit", FONT, WHITE, BLUE, LIGHT_BLUE)

    def draw(self):
        self.screen.fill(WHITE)
        draw_text("Main Menu", FONT, BLACK, self.screen, 400, 100)
        self.play_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def handle_events(self):
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = any(event.type == pygame.MOUSEBUTTONDOWN for event in pygame.event.get())

        self.play_button.check_hover(mouse_pos)
        self.settings_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)

        if self.play_button.is_clicked(mouse_pos, mouse_click):
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
