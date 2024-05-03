import pygame
from enum import Enum
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, \
    K_k, K_m, K_n, K_p, K_r, K_l, K_o, K_q, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z
import random
from itertools import zip_longest

# words = [
#     "adventure", "blossom", "curiosity", "delight", "envision",
#     "flourish", "graceful", "harmony", "insight", "jubilant",
#     "kinship", "luminous", "mystique", "nomadic", "opulence",
#     "pristine", "quaint", "resilient", "tranquil", "vivacious"
# ]
#
words = [
    "abrakadabra", "aaaaaaaaaaaa", "graceful", "harmony"
]


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
        self.rect = self.image.get_rect(center=(Size.WIDTH.value // 2, Size.HEIGHT.value - 100))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.font.init()

        self.word = random.choice(words)
        self.word2 = self.word

        self.len_word = len(self.word)
        self.start_word = self.word[0]

        self.image = pygame.Surface((30, 30))
        self.image.fill(Color.BLACK.value)

        self.inner_color = Color.WHITE.value

        self.focus = None
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, Size.WIDTH.value - self.rect.width)
        self.rect.y = 0

        self.speed = 0.7
        self.font = pygame.font.Font(None, 36)
        self.text_surface = None

    def draw(self):
        self.text_surface = self.font.render(self.word, True, self.inner_color, (0, 0, 0))
        game.main_display.blit(self.text_surface, (self.rect.x, self.rect.y))

    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        if self.rect.y > Size.HEIGHT.value:
            self.kill()

    def __lt__(self, other):  # <
        return True if self.rect.y < other.rect.y else False

    def __gt__(self, other):  # >
        return True if self.rect.y > other.rect.y else False

    def set_color(self):
        self.inner_color = Color.GREEN.value

    def delete_symbol(self, symbol):
        if self.word[0] == symbol:
            self.word = self.word[1:]
            if self.word == "":
                self.word = None


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(Color.WHITE.value)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20
        self.target_x = target_x
        self.target_y = target_y
        self.velocity_x = (self.target_x - x) / max(abs(self.target_x - x), abs(self.target_y - y), 1) * self.speed
        self.velocity_y = (self.target_y - y) / max(abs(self.target_x - x), abs(self.target_y - y), 1) * self.speed

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if pygame.Rect(self.target_x - 5, self.target_y - 5, 10, 10).colliderect(self.rect):
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
        pygame.time.set_timer(self.CREATE_ENEMY, 2000)

        self.playing = True
        self.FPS = pygame.time.Clock()

        self.player = player
        self.enemy = enemy
        self.main_display = pygame.display.set_mode((Size.WIDTH.value, Size.HEIGHT.value))
        self.bg = pygame.transform.scale(pygame.image.load("sprites/background_space.png"), (1200, 800))
        self.current_key = None

        self.focus = None
        self.enemies.add(Enemy())

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(Game)
        return cls.__instance

    def add_enemy(self, temp: Enemy):
        self.enemies.add(temp)

    def add_bullet(self, temp: Bullet):
        self.bullets.add(temp)

    def get_pressed_key(self, key):
        alphabet_keys = {
            K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e', K_f: 'f', K_g: 'g',
            K_h: 'h', K_i: 'i', K_j: 'j', K_k: 'k', K_l: 'l', K_m: 'm', K_n: 'n',
            K_o: 'o', K_p: 'p', K_q: 'q', K_r: 'r', K_s: 's', K_t: 't', K_u: 'u',
            K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y', K_z: 'z'
        }
        return alphabet_keys[key]

    def check_keys(self):
        keys = pygame.key.get_pressed()
        for i in range(pygame.K_a, pygame.K_z + 1):
            if keys[i]:
                self.current_key = chr(i)
                return chr(i)

    def generate_fragments(self, x, y):
        for _ in range(10):
            w = random.randint(10, 20)
            h = random.randint(10, 20)
            x = x
            y = y
            # x = rect.x + random.randint(0, rect.width - w)
            # y = rect.y + random.randint(0, rect.height - h)
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            fragments.append([pygame.Rect(x, y, w, h), dx, dy])


group = []
group2 = []

animating = False
game_active = True
fragments = []
enemy_obj = Enemy()
game = Game(player=Player(), enemy=Enemy())

while game.playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            game.playing = False
        if event.type == game.CREATE_ENEMY:
            # game.add_enemy(Enemy())
            group.append(Enemy())

    game.main_display.blit(game.bg, (0, 0))
    game.bullets.update()

    collisions = pygame.sprite.groupcollide(game.bullets, game.enemies, True, False)

    for i in group:
        if game.check_keys() == i.word2[0] and len(group2) == 0:
            group2.append(i)
            i.set_color()
            break

    for i in group2:
        if i.word is None or i.rect.y > Size.HEIGHT.value:
            group2.remove(i)
            group.remove(i)
            break

    for enemy in group:
        enemy.draw()
        enemy.update()

    for enemy2 in group2:
        enemy2.draw()
        enemy2.update()

        if game.current_key == enemy2.word[0]:
            enemy2.delete_symbol(game.current_key)
            if not enemy2.word:
                enemy2.kill()

            player_center_x, player_center_y = game.player.rect.center
            target_x, target_y = enemy2.rect.center
            new_bullet = Bullet(player_center_x, player_center_y, target_x, target_y)
            game.add_bullet(new_bullet)

        if enemy2.rect.colliderect(game.player.rect):
            game.playing = False

    # game.enemies.draw(game.main_display)
    for bullet in game.bullets:
        game.main_display.blit(bullet.image, bullet.rect)

    game.main_display.blit(game.player.image, game.player.rect)
    pygame.display.flip()
    game.FPS.tick(60)
