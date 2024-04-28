import pygame
from pygame.locals import *

# Ініціалізація Pygame
pygame.init()

# Встановлення розміру вікна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Динамічний квадрат")

# Колір
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Початкові координати та розмір квадрата
x, y = 50, 50
size = 50

# Основний цикл гри
running = True
while running:
    # Очистка екрану
    win.fill(WHITE)

    # Опрацювання подій
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Отримання стану натисканих клавіш
    keys = pygame.key.get_pressed()

    # Зміна координат квадрата в залежності від натиснутих клавіш
    if keys[K_LEFT]:
        x -= 5
    if keys[K_RIGHT]:
        x += 5
    if keys[K_UP]:
        y -= 5
    if keys[K_DOWN]:
        y += 5

    # Малювання квадрата на екрані
    pygame.draw.rect(win, BLUE, (x, y, size, size))

    # Оновлення вікна
    pygame.display.update()

# Закриття вікна Pygame
pygame.quit()
