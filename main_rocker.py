import pygame
from enum import Enum
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT  # Імпорт констант з pygame
import random

pygame.init()


class Constants(Enum):
    HEIGHT = 800
    WIDTH = 1200
    color_WHITE = (255, 255, 255)
    color_BLACK = (0, 0, 0)
    color_BLUE = (0, 0, 255)
    color_RED = (255, 0, 0)
    color_GREEN = (0, 255, 0)
    CREATE_ENEMY = pygame.USEREVENT + 1

class Player:
    def __init__(self):
        self.player_rect = pygame.Rect(0, 0, 50, 50)  # Параметри: (x, y, width, height)
        self.player_move_down = [0, 4]
        self.player_mover_right = [4, 0]
        self.player_move_up = [0, -4]
        self.player_move_left = [-4, 0]
        self.set_center_pos()

    def move_down(self):
        self.player_rect = self.player_rect.move(self.player_move_down)

    def move_up(self):
        self.player_rect = self.player_rect.move(self.player_move_up)

    def move_right(self):
        self.player_rect = self.player_rect.move(self.player_mover_right)

    def move_left(self):
        self.player_rect = self.player_rect.move(self.player_move_left)

    def draw_player(self):
        pygame.draw.rect(game.main_display, (255, 0, 0), game.player.player_rect)  # Параметри: (surface, color, rect)

    def set_center_pos(self):
        self.player_rect = self.player_rect.move(Constants.WIDTH.value // 2, Constants.HEIGHT.value // 2)

class Enemy:
    def __init__(self):
        self.enemy_rect = pygame.Rect(0, 0, 25, 25)  # Параметри: (x, y, width, height)
        self.enemy_size = (30, 30)
        self.original_image = pygame.image.load("enemy.png")
        self.scaled_image = pygame.transform.scale(self.original_image, (100, 50))

        self.enemy = pygame.transform.rotate(self.scaled_image, 90)
        self.enemy_rect = pygame.Rect(random.randint(0, Constants.WIDTH.value), 0, *self.enemy_size)
        self.enemy_move = [0, random.randint(4, 8)]


class Game:
    __instance = None
    score = 0
    enemies = []
    playing = True
    def __init__(self, player: Player()):
        self.FPS = pygame.time.Clock()
        self.player = player
        self.main_display = pygame.display.set_mode((Constants.WIDTH.value, Constants.HEIGHT.value))
        pygame.time.set_timer(Constants.CREATE_ENEMY.value, 200)  # Таймер для події створення ворога

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(Game)
        return cls.__instance


game = Game(player=Player())


while Game.playing:
    game.FPS.tick(60)  # Установка частоти оновлення кадрів
    for event in pygame.event.get():
        if event.type == QUIT:
            Game.playing = False  # Вихід з гри при закритті вікна
        if event.type == Constants.CREATE_ENEMY.value:
            Game.enemies.append(Enemy())  #
        # if event.type == CREATE_BONUS:
        #     bonuses.append(create_bonus())  # Додавання нового бонуса

    keys = pygame.key.get_pressed()  # Отримання стану клавіш
    # Обробка натискання клавіш для руху гравця
    if keys[K_DOWN] and game.player.player_rect.bottom < Constants.HEIGHT.value:
        game.player.move_down()
    if keys[K_UP] and game.player.player_rect.top > 0 < Constants.HEIGHT.value:
        game.player.move_up()
    if keys[K_RIGHT] and game.player.player_rect.right < Constants.WIDTH.value:
        game.player.move_right()
    if keys[K_LEFT] and game.player.player_rect.left > 0 < Constants.WIDTH.value:
        game.player.move_left()

    game.main_display.fill(Constants.color_WHITE.value)


    for obj in Game.enemies:
        obj.enemy_rect = obj.enemy_rect.move(obj.enemy_move)
        game.main_display.blit(obj.enemy, obj.enemy_rect)

        if game.player.player_rect.colliderect(obj.enemy_rect):
            Game.playing = False  # Завершення гри при зіткненні з ворого гри при зіткненні з ворогоn_display, Constants.color_GREEN.value, enemy.enemy_rect)

        # if game.player.player_rect.colliderect(enemy):
        #     Constants.PLAYING = False

    game.player.draw_player()
    pygame.display.flip()  # Оновлення вікна гри

    # Видалення ворогів та бонусів, що вийшли за межі екрану
    for obj in Game.enemies:
        if obj.enemy_rect.left < 0:
            Game.enemies.pop(Game.enemies.index(obj))
