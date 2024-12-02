import pygame
import os
from settings import *
from classes.RaceTrack import Racetrack
from pages.DrawTrack import DrawTrack
from pages.MainPage import MainPage


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption("Main Menu")

    main_track = Racetrack()
    running = True

    pages = {
        'draw_track': DrawTrack(screen, main_track),
        'quit': MainPage(screen, main_track),
        'main_menu': MainPage(screen, main_track)
    }
    current_page = 'main_menu'

    while running:
        next_page = pages[current_page].handle_events()
        if current_page != next_page:
            current_page = next_page

        pages[current_page].update()
        pages[current_page].draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
