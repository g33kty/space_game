import pygame
from enum import Enum
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


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
    def __init__(self ):
        self.original_image = pygame.image.load("sprites/img_2.png")
        self.player = pygame.transform.scale(self.original_image, (150, 120))
        # self.enemy = pygame.transform.rotate(self.scaled_image, 90)
        self.reeect = pygame.Surface((50, 50)).get_rect()
        self.player.set_colorkey(Constants.color_WHITE.value)
        self.player_rect = self.player.get_rect()  # Параметри: (x, y, width, height)

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
        self.player_rect = self.player_rect.move(Constants.WIDTH.value // 2, Constants.HEIGHT.value // 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename=None):
        super().__init__()
        if filename is None:
            self.image = pygame.Surface((30, 30))
            self.image.fill(Constants.color_BLACK.value)
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, Constants.WIDTH.value - self.rect.width)
            self.rect.y = 0
            self.speed = random.randint(1, 5)
        else:
            self.enemy_rect = pygame.Rect(0, 0, 25, 25)
            self.enemy_size = (30, 30)
            self.image_file = pygame.transform.scale(pygame.image.load("filename"), *self.enemy_size)
    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        if self.rect.y > Constants.HEIGHT.value:
            self.kill()

    def __lt__(self, other):  # <
        return True if self.rect.y < other.rect.y else False

    def __gt__(self, other):  # >
        return True if self.rect.y > other.rect.y else False

    def set_color(self):
        self.image.fill(Constants.color_BLUE.value)
        return self

    def get_rect(self):
        return self.rect


class Game:
    __instance = None
    __score = 0

    def __init__(self, player: Player()):
        pygame.init()
        pygame.display.set_caption("staminaspace")
        self.CREATE_ENEMY = pygame.USEREVENT
        pygame.time.set_timer(self.CREATE_ENEMY, 1500)
        self.playing = True
        self.enemies = pygame.sprite.Group()
        self.FPS = pygame.time.Clock()
        self.player = player
        self.main_display = pygame.display.set_mode((Constants.WIDTH.value, Constants.HEIGHT.value))
        pygame.time.set_timer(Constants.CREATE_ENEMY.value, 200)
        self.bg = pygame.transform.scale(pygame.image.load("sprites/background_space.png"), (1200, 800))

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(Game)
        return cls.__instance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(Constants.color_WHITE.value)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.target_x = target_x
        self.target_y = target_y

    def update(self):
        direction_x = self.target_x - self.rect.centerx
        direction_y = self.target_y - self.rect.centery
        distance = max(abs(direction_x), abs(direction_y), 1)
        self.rect.x += (direction_x / distance) * self.speed
        self.rect.y += (direction_y / distance) * self.speed
        if self.rect.colliderect(pygame.Rect(self.target_x - 5, self.target_y - 5, 10, 10)):
            self.kill()


bullets = pygame.sprite.Group()

game = Game(player=Player())
x = Enemy()
game.enemies.add(x)


temp_x, temp_y = None, None
while game.playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            game.playing = False

        if event.type == game.CREATE_ENEMY:
            x = Enemy()
            game.enemies.add(x)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                x, y, *_ = game.player.player_rect
                new_bullet = Bullet(x + 70, y, *pygame.mouse.get_pos())
                bullets.add(new_bullet)

    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and game.player.player_rect.bottom < Constants.HEIGHT.value:
        game.player.move_down()
    if keys[K_UP] and game.player.player_rect.top > 0 < Constants.HEIGHT.value:
        game.player.move_up()
    if keys[K_RIGHT] and game.player.player_rect.right < Constants.WIDTH.value:
        game.player.move_right()
    if keys[K_LEFT] and game.player.player_rect.left > 0 < Constants.WIDTH.value:
        game.player.move_left()

    game.main_display.blit(game.bg, game.bg.get_rect())

    bullets.update()
    game.enemies.update()



    player_center_x = game.player.player_rect.centerx
    player_center_y = game.player.player_rect.centery

    for enemy in game.enemies:
        if enemy.rect.collidepoint(player_center_x, player_center_y):
            game.playing = False


    for bullet in bullets:
        down_bullet = max(game.enemies).set_color().get_rect()


        bullet.target_x = down_bullet.x
        bullet.target_y = down_bullet.y


    game.enemies.draw(game.main_display)
    bullets.draw(game.main_display)
    game.main_display.blit(game.player.player, game.player.player_rect)

    pygame.display.flip()
    game.FPS.tick(60)
