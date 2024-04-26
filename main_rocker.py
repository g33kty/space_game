import pygame
from enum import Enum


class Сonstants(Enum):
    HEIGHT = 800
    WIDTH = 1200

    color_WHITE = (255, 255, 0)
    color_BLACK = (0, 0, 0)
    color_BLUE = (0, 0, 255)
    color_RED = (255, 0, 0)
    FONT = pygame.font.SysFont("Verdana", 20)
    FPS = pygame.time.Clock()


class Player:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()

        self.player_rect = self.player.get_rect()
        self.player_rect.x = 200
        self.player_rect.y = Сonstants.WIDTH - Сonstants.HEIGHT

        self.player_move_down = [0, 4]
        self.player_mover_right = [4, 0]
        self.player_move_up = [0, -4]
        self.player_move_left = [-4, 0]

class Enemy:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()

        self.player_rect = self.player.get_rect()
        self.player_rect.x = 200
        self.player_rect.y = Сonstants.WIDTH - Сonstants.HEIGHT

        self.player_move_down = [0, 4]
        self.player_mover_right = [4, 0]
        self.player_move_up = [0, -4]
        self.player_move_left = [-4, 0]