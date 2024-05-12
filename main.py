import pygame
import random

pygame.init()

class Player():
    def __init__(self, x, y, width, height, image):
        # Ініціалізація гравця
        self.original_image = pygame.image.load(image)  # Завантаження зображення гравця
        self.image = pygame.transform.scale(self.original_image, (width, height))  # Зміна розміру зображення
        self.rect = self.image.get_rect()  # Отримання прямокутника, обведеного навколо зображення
        self.rect.x = x  # Встановлення початкової позиції гравця по горизонталі
        self.rect.y = y  # Встановлення початкової позиції гравця по вертикалі
        self.width = width  # Ширина гравця
        self.height = height  # Висота гравця
        self.lives = 3  # Кількість життів гравця

# Встановлення розмірів вікна та FPS
WIDTH, HEIGHT = 700, 600
FPS = 60
background_image = pygame.image.load('background.png')  # Завантаження зображення тла
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Зміна розміру зображення тла

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Створення вікна гри з встановленими розмірами
clock = pygame.time.Clock()  # Створення годинника для обмеження частоти кадрів

font = pygame.font.Font(None, 36)  # Створення шрифту для тексту
text_lives = font.render("Життя: ", True, (0,0,0))  # Створення тексту для відображення кількості життів

# Змінні для лічильника очок
score = 0
font_score = pygame.font.Font(None, 36)  # Створення шрифту для лічильника очок
text_score = font_score.render("Очки: " + str(score), True, (0,0,0))  # Створення тексту для відображення кількості очок

# Початкові координати гравця
py, sy, ay = HEIGHT // 2, 0, 0
player = Player(50, 50, 50, 50, "bird.png")  # Створення об'єкта гравця з заданими параметрами

state = 'start'  # Початковий стан гри
timer = 10  # Лічильник часу до початку гри
pipes = []  # Список труб
play = True  # Флаг, що вказує на те, чи триває гра

# Функція для створення нової пари труб
def create_pipe():
    gap = 200  # Відстань між верхньою та нижньою трубою
    pipe_height = random.randint(50, HEIGHT - gap - 50)  # Випадкова висота верхньої труби
    pipe_top_height = pipe_height  # Висота верхньої труби
    pipe_bottom_height = HEIGHT - pipe_height - gap  # Висота нижньої труби

    # Завантаження зображень труб та зміна їх розмірів
    pipe_top_image = pygame.image.load('pipe_top.png')
    pipe_bottom_image = pygame.image.load('pipe_bottom.png')
    pipe_top_image = pygame.transform.scale(pipe_top_image, (50, pipe_top_height))
    pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (50, pipe_bottom_height))

    # Встановлення початкової позиції труб
    pipe_top_rect = pipe_top_image.get_rect(topleft=(WIDTH, 0))
    pipe_bottom_rect = pipe_bottom_image.get_rect(topleft=(WIDTH, pipe_top_height + gap))

    return pipe_top_image, pipe_bottom_image, pipe_top_rect, pipe_bottom_rect  # Повернення пари труб

# Основний цикл гри
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    window.blit(background_image, (0, 0))  # Відображення тла
    window.blit(player.image, (player.rect.x, player.rect.y))  # Відображення гравця
    text_lives_display = font.render("Життя: " + str(player.lives), True, (0,0,0))  # Створення тексту для відображення кількості життів
    window.blit(text_lives_display, (10, 560))  # Відображення тексту про життя

    # Відображення лічильника очок
    text_score = font_score.render("Очки: " + str(score), True, (0,0,0))
    window.blit(text_score, (10, 10))

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    # Обробка труб
    for pipe_pair in pipes:
        pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect = pipe_pair
        pipe_top_rect.x -= 3
        pipe_bottom_rect.x -= 3
        if pipe_top_rect.right < 0:
            pipes.remove(pipe_pair)

    # Логіка гри
    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'
        py += (HEIGHT // 2 - py) * 0.1
        player.rect.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.rect.y = py
        if len(pipes) == 0 or pipes[len(pipes)-1][2].right < WIDTH - 200:
            pipes.append(create_pipe())
        if player.rect.top < 0 or player.rect.bottom > HEIGHT:
            sy, ay = 0, 0
            player.lives -= 1
            if player.lives == 0:
                play = False
            else:
                state = 'fall'
                timer = 60
        for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
            if player.rect.colliderect(pipe_top_rect) or player.rect.colliderect(pipe_bottom_rect):
                player.lives -= 1
                if player.lives == 0:
                    play = False
                else:
                    state = 'fall'
    elif state == 'fall':
        state = 'start'
    else:
        pass

    # Лічильник очок
    if state == 'play':
        for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
            if pipe_top_rect.right < player.rect.x and pipe_top_rect.right > 0 and pipe_top_rect.right < WIDTH // 2 and pipe_top_rect.right > player.rect.x - 3:
                score += 10

    # Видалення труб, які знаходяться перед екраном, коли гра ще не закінчилася
    if state != 'start':
        pipes = [pipe_pair for pipe_pair in pipes if pipe_pair[2].right > 0]

    # Відображення труб
    for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
        window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
        window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

    pygame.display.update()  # Оновлення екрану
    clock.tick(FPS)  # Обмеження кадрів за секунду

pygame.quit()  # Завершення гри

