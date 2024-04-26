import pygame  # Імпорт модуля pygame
import random  # Імпорт модуля random для генерації випадкових чисел

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT  # Імпорт констант з pygame

pygame.init()  # Ініціалізація модулів pygame

HEIGHT = 800  # Висота вікна гри
WIDTH = 1200  # Ширина вікна гри

# Кольори, визначені у форматі RGB
color_WHITE = (255, 255, 0)
color_BLACK = (0, 0, 0)
color_BLUE = (0, 0, 255)
color_RED = (255, 0, 0)

FONT = pygame.font.SysFont("Verdana", 20)  # Шрифт для тексту

player_size = (20, 20)  # Розміри спрайта гравця
FPS = pygame.time.Clock()  # Таймер для контролю частоти оновлення кадрів

main_display = pygame.display.set_mode((WIDTH, HEIGHT))  # Створення вікна гри

# Завантаження та масштабування фону гри
bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_x1 = 0  # Початкова позиція першого фону
bg_x2 = bg.get_width()  # Початкова позиція другого фону

bg_move = 3  # Швидкість переміщення фону
player = pygame.image.load("player.png").convert_alpha()  # Завантаження зображення гравця

player_rect = player.get_rect()  # Отримання прямокутника, що охоплює спрайт гравця
player_rect.x = 200  # Початкова позиція гравця по x
player_rect.y = WIDTH - HEIGHT  # Початкова позиція гравця по y

# Вектори переміщення гравця
player_move_down = [0, 4]
player_mover_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.transform.scale(pygame.image.load("enemy.png"), (100, 50)).convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT - 100), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]  # Створення ворога

def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.transform.scale(pygame.image.load("bonus.png"), (150, 30)).convert_alpha()
    bonus_rect = pygame.Rect(random.randint(300, 700), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 6)]
    return [bonus, bonus_rect, bonus_move]  # Створення бонусу

CREATE_ENEMY = pygame.USEREVENT + 1  # Кастомна подія для створення ворога
CREATE_BONUS = pygame.USEREVENT + 2  # Кастомна подія для створення бонуса
pygame.time.set_timer(CREATE_ENEMY, 1000)  # Таймер для події створення ворога
pygame.time.set_timer(CREATE_BONUS, 4000)  # Таймер для події створення бонуса

enemies = []  # Список ворогів
bonuses = []  # Список бонусів

score = 0  # Рахунок гравця
playing = True  # Прапорець, що контролює основний цикл гри
while playing:
    FPS.tick(60)  # Установка частоти оновлення кадрів
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False  # Вихід з гри при закритті вікна

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())  # Додавання нового ворога
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())  # Додавання нового бонуса

    bg_x1 -= bg_move  # Переміщення першого фону
    bg_x2 -= bg_move  # Переміщення другого фону

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()  # Зациклення першого фону

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()  # Зациклення другого фону

    main_display.blit(bg, (bg_x1, 0))  # Відображення першого фону
    main_display.blit(bg, (bg_x2, 0))  # Відображення другого фону

    keys = pygame.key.get_pressed()  # Отримання стану клавіш
    # Обробка натискання клавіш для руху гравця
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0 < HEIGHT:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_mover_right)
    if keys[K_LEFT] and player_rect.left > 0 < WIDTH:
        player_rect = player_rect.move(player_move_left)

    # Обробка взаємодій гравця з ворогами та бонусами
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False  # Завершення гри при зіткненні з ворогом

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))  # Видалення бонусу при зборі
            score += 1  # Збільшення рахунку

    # Відображення спрайту гравця та рахунку
    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(f"SCORE: {str(score)}", True, color_RED), (WIDTH - 110, HEIGHT))
    pygame.display.flip()  # Оновлення вікна гри

    # Видалення ворогів та бонусів, що вийшли за межі екрану
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].left < 0:
            bonuses.pop(bonuses.index(bonus))
