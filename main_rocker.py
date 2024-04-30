import pygame
from enum import Enum
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


class Size(Enum):
    HEIGHT = 800
    WIDTH = 1200


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


class Player:
    def __init__(self):
        self.image = pygame.Surface((50, 50))

        self.player_rect = self.image.get_rect()  # Параметри: (x, y, width, height)

        self.player_x = self.player_rect.x
        self.player_y = self.player_rect.y

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
        self.player_rect = self.player_rect.move(Size.WIDTH.value // 2 + 50, Size.HEIGHT.value - 100)

    def player_keyboard_move(self):
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and game.player.player_rect.bottom < Size.HEIGHT.value:
            game.player.move_down()
        if keys[K_UP] and game.player.player_rect.top > 0 < Size.HEIGHT.value:
            game.player.move_up()
        if keys[K_RIGHT] and game.player.player_rect.right < Size.WIDTH.value:
            game.player.move_right()
        if keys[K_LEFT] and game.player.player_rect.left > 0 < Size.WIDTH.value:
            game.player.move_left()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename=None):
        super().__init__()
        if filename is None:
            self.image = pygame.Surface((30, 30))
            self.image.fill(Color.BLACK.value)
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, Size.WIDTH.value - self.rect.width)
            self.rect.y = 0
            self.speed = random.randint(1, 5)
        else:
            self.enemy_rect = pygame.Rect(0, 0, 25, 25)
            self.enemy_size = (30, 30)
            self.image_file = pygame.transform.scale(pygame.image.load("filename"), *self.enemy_size)

    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        if self.rect.y > Size.HEIGHT.value:
            self.kill()

    def __lt__(self, other):  # <
        return True if self.rect.y < other.rect.y else False

    def __gt__(self, other):  # >
        return True if self.rect.y > other.rect.y else False

    def set_color(self):
        self.image.fill(Color.BLUE.value)
        return self

    def get_rect(self):
        return self.rect


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(Color.WHITE.value)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.target_x = None
        self.target_y = None

    def update(self):
        if self.target_x is not None and self.target_y is not None:
            direction_x = self.target_x - self.rect.centerx
            direction_y = self.target_y - self.rect.centery
            distance = max(abs(direction_x), abs(direction_y), 1)
            self.rect.x += (direction_x / distance) * self.speed
            self.rect.y += (direction_y / distance) * self.speed

            # Check for collision with the target coordinates
            if self.rect.colliderect(pygame.Rect(self.target_x - 5, self.target_y - 5, 10, 10)):
                self.kill()



class Game:
    __instance = None
    __score = 0

    def __init__(self, player: Player, enemy: Enemy):
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        pygame.init()
        pygame.display.set_caption("staminaspace")
        self.CREATE_ENEMY = pygame.USEREVENT
        pygame.time.set_timer(self.CREATE_ENEMY, 1500)

        self.playing = True
        self.FPS = pygame.time.Clock()

        self.player = player
        self.enemy = enemy

        self.main_display = pygame.display.set_mode((Size.WIDTH.value, Size.HEIGHT.value))
        self.bg = pygame.transform.scale(pygame.image.load("sprites/background_space.png"), (1200, 800))

        self.enemies.add(Enemy())

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(Game)
        return cls.__instance

    def add_enemy(self, temp: Enemy):
        self.enemies.add(temp)

    def add_bullet(self, temp: Bullet):
        self.bullets.add(temp)



game = Game(player=Player(), enemy=Enemy())

while game.playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            game.playing = False

        if event.type == game.CREATE_ENEMY:
            game.add_enemy(Enemy())

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_center_x, player_center_y = game.player.player_rect.center
                new_bullet = Bullet(player_center_x, player_center_y)
                game.add_bullet(new_bullet)

    game.player.player_keyboard_move()

    for bullet in game.bullets:
        nearest_enemy = max(game.enemies, key=lambda enemy: enemy.rect.centery).set_color()

        bullet.target_x, bullet.target_y = nearest_enemy.rect.center

    game.main_display.blit(game.bg, game.bg.get_rect())
    game.bullets.update()
    game.enemies.update()

    for enemy in game.enemies:
        if enemy.rect.colliderect(game.player.player_rect):
            game.playing = False

    game.enemies.draw(game.main_display)
    game.bullets.draw(game.main_display)
    game.main_display.blit(game.player.image, game.player.player_rect)

    pygame.display.flip()
    game.FPS.tick(60)
