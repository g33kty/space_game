import pygame
from enum import Enum
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

pygame.init()


# Завантаження та масштабування фону гри
# original_image = pygame.image.load("background_space.png")
# scaled_image = pygame.transform.scale(original_image, (1200, 800))

# bg = pygame.transform.rotate(original_image, 90)
#
# bg_y1 = 0  # Початкова позиція першого фону
# bg_y2 = bg.get_height()  # Початкова позиція другого фону
#
# bg_move = 1 # Швидкість переміщення фону


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

        self.original_image = pygame.image.load("sprites/img_2.png")
        self.player = pygame.transform.scale(self.original_image, (150, 120))
        # self.enemy = pygame.transform.rotate(self.scaled_image, 90)

        self.player.set_colorkey(Constants.color_WHITE.value)
        self.player_rect = self.player.get_rect()  # Параметри: (x, y, width, height)

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
        pygame.draw.rect(game.main_display, (255, 0, 0), game.player.player_rect)

    def set_center_pos(self):
        self.player_rect = self.player_rect.move(Constants.WIDTH.value // 2, Constants.HEIGHT.value // 2)

class Enemy:
    def __init__(self):
        self.enemy_rect = pygame.Rect(0, 0, 25, 25)
        self.enemy_size = (30, 30)
        self.original_image = pygame.image.load("sprites/enemy.png")
        self.scaled_image = pygame.transform.scale(self.original_image, (100, 50))

        self.enemy = pygame.transform.rotate(self.scaled_image, 90)
        self.enemy_rect = pygame.Rect(random.randint(0, Constants.WIDTH.value), 0, *self.enemy_size)
        self.enemy_move = [0, random.randint(4, 8)]


class Game:
    __instance = None
    __score = 0
    enemies = []
    playing = True

    def __init__(self, player: Player()):
        self.FPS = pygame.time.Clock()
        self.player = player
        self.main_display = pygame.display.set_mode((Constants.WIDTH.value, Constants.HEIGHT.value))
        pygame.time.set_timer(Constants.CREATE_ENEMY.value, 200)
        self.bg = pygame.transform.scale(pygame.image.load("sprites/background_space.png"), (1200, 800))

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

    # bg_y1 -= bg_move  # Переміщення першого фону
    # bg_y2 -= bg_move  # Переміщення другого фону
    #
    # if bg_y1 < -bg.get_height():
    #     bg_y1 = bg.get_height()  # Зациклення першого фону
    #
    # if bg_y2 < -bg.get_height():
    #     bg_y2 = bg.get_height()  # Зациклення другого фону


    keys = pygame.key.get_pressed()  # Отримання стану клавіш
    if keys[K_DOWN] and game.player.player_rect.bottom < Constants.HEIGHT.value:
        game.player.move_down()
    if keys[K_UP] and game.player.player_rect.top > 0 < Constants.HEIGHT.value:
        game.player.move_up()
    if keys[K_RIGHT] and game.player.player_rect.right < Constants.WIDTH.value:
        game.player.move_right()
    if keys[K_LEFT] and game.player.player_rect.left > 0 < Constants.WIDTH.value:
        game.player.move_left()

    game.main_display.fill(Constants.color_WHITE.value)

    game.main_display.blit(game.bg, (0, 0))
    # game.main_display.blit(bg, (bg_y1, 0))  # Відображення першого фону
    # game.main_display.blit(bg, (bg_y2, 0))  # Відображення другого фону

    for obj in Game.enemies:
        obj.enemy_rect = obj.enemy_rect.move(obj.enemy_move)
        game.main_display.blit(obj.enemy, obj.enemy_rect)

        if game.player.player_rect.colliderect(obj.enemy_rect):
            Game.playing = False  # Завершення гри при зіткненні з ворого гри при зіткненні з ворогоn_display, Constants.color_GREEN.value, enemy.enemy_rect)

        # if game.player.player_rect.colliderect(enemy):
        #     Constants.PLAYING = False
    game.main_display.blit(game.player.player, game.player.player_rect)
    # game.player.draw_player()
    pygame.display.flip()  # Оновлення вікна гри

    # Видалення ворогів та бонусів, що вийшли за межі екрану
    for obj in Game.enemies:
        if obj.enemy_rect.left < 0:
            Game.enemies.pop(Game.enemies.index(obj))
