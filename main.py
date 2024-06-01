import pygame
import random

pygame.init()

# Клас для гравця
class Player():
    def __init__(self, x, y, width, height, frames):
        self.frames = frames  # Список кадрів анімації пташки
        self.index = 0  # Поточний індекс кадру анімації
        self.image = self.frames[self.index]  # Зображення поточного кадру
        self.rect = self.image.get_rect()  # Прямокутник, який оточує пташку
        self.rect.x = x  # Початкове положення по осі X
        self.rect.y = y  # Початкове положення по осі Y
        self.width = width  # Ширина пташки
        self.height = height  # Висота пташки
        self.lives = 3  # Кількість життів гравця
        self.rotation_angle = 0  # Кут повороту пташки
        self.sensitivity = 50  # Початкове значення чутливості пташки

    # Функція оновлення анімації пташки
    def update_animation(self, velocity):
        self.index += 0.1  # Зміна індексу анімації
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]  # Оновлення зображення анімації
        
        if velocity != 0:
            self.rotation_angle = min(max(-30, velocity * -2), 30)  # Обчислення кута повороту
        else:
            self.rotation_angle = 0

        self.image = pygame.transform.rotate(self.image, self.rotation_angle)  # Поворот зображення

# Встановлення розмірів вікна та FPS
WIDTH, HEIGHT = 700, 600
FPS = 60

# Завантаження іконки вікна гри
icon_image = pygame.image.load('icon.png')
pygame.display.set_icon(icon_image)

# Встановлення заголовка вікна гри
pygame.display.set_caption("Flappy Bird")

# Завантаження фонового зображення
background_image = pygame.image.load('background.png')  
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  

window = pygame.display.set_mode((WIDTH, HEIGHT))  
clock = pygame.time.Clock()  

font = pygame.font.Font(None, 36)  

# Відображення кількості життів
text_lives_position = (10, 10)
player_lives = 3

# Відображення кількості очок
text_score_position = (10, 560)
score = 0

# Функція для відображення тексту
def display_text(text, position, font, color=(0,0,0)):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, position)

py, sy, ay = HEIGHT // 2, 0, 0

bird_image = pygame.image.load('bird.png')
frame_width = bird_image.get_width() // 4  
frame_height = bird_image.get_height()
bird_frames = [bird_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(4)]

player = Player(50, 50, 50, 50, bird_frames)

state = 'menu'
timer = 10  
pipes = []  
play = True  

# Функція для створення труб
def create_pipe():
    gap = 200  
    pipe_height = random.randint(50, HEIGHT - gap - 50)  
    pipe_top_height = pipe_height  
    pipe_bottom_height = HEIGHT - pipe_height - gap  

    pipe_top_image = pygame.image.load('pipe_top.png')
    pipe_bottom_image = pygame.image.load('pipe_bottom.png')
    pipe_top_image = pygame.transform.scale(pipe_top_image, (50, pipe_top_height))
    pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (50, pipe_bottom_height))

    pipe_top_rect = pipe_top_image.get_rect(topleft=(WIDTH, 0))
    pipe_bottom_rect = pipe_bottom_image.get_rect(topleft=(WIDTH, pipe_top_height + gap))

    return pipe_top_image, pipe_bottom_image, pipe_top_rect, pipe_bottom_rect  

# Додавання музики
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# Додавання звуку при втраті життя
fall_sound = pygame.mixer.Sound('fall.wav')

# Завантаження зображення шестерні та обрізання білого фону
gear_image = None
gear_position = (10, 10)
try:
    gear_image = pygame.image.load('download.png').convert_alpha()
    gear_image = pygame.transform.scale(gear_image, (50, 50))  # Масштабування до 50x50
    gear_image.set_colorkey((255, 255, 255))  # Робимо білий колір прозорим
    gear_rect = gear_image.get_rect(topleft=gear_position)
except pygame.error:
    print("Файл 'download.png' не знайдено в робочій директорії.")

# Функція для відображення кнопки
def draw_button(text, position, font, color, bgcolor):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    pygame.draw.rect(window, bgcolor, text_rect.inflate(20, 10))
    window.blit(text_surface, text_rect)
    return text_rect

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'menu':
                mouse_pos = event.pos
                if gear_rect.collidepoint(mouse_pos):
                    state = 'settings'
            elif state == 'settings':
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):
                    state = 'menu'

    window.blit(background_image, (0, 0))  
    
    if state == 'menu':
        title_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        display_text("Flappy Bird", (WIDTH // 2, HEIGHT // 4), title_font, (255, 255, 255))
        start_button = draw_button("Почати гру", (WIDTH // 2, HEIGHT // 2), button_font, (255, 255, 255), (0, 0, 0))
        quit_button = draw_button("Вийти", (WIDTH // 2, HEIGHT // 2 + 100), button_font, (255, 255, 255), (0, 0, 0))
        
        if gear_image:
            window.blit(gear_image, gear_position)

    elif state == 'settings':
        title_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        display_text("Налаштування", (150, 10), title_font, (255, 255, 255))
        back_button = draw_button("Назад", (WIDTH // 2, HEIGHT // 2 + 100), button_font, (255, 255, 255), (0, 0, 0))
        
        # Відображення чутливості пташки та руху слайдера
        pygame.draw.rect(window, (192, 192, 192), (100, 200, 500, 50))  # Сірий фон для слайдера
        pygame.draw.rect(window, (0, 0, 0), (100 + player.sensitivity * 5, 200, 10, 50))  # Чорний слайдер
        display_text("Чутливість пташки:", (20, 210), font, (255, 255, 255))
        display_text(str(player.sensitivity) + "%", (630, 210), font, (255, 255, 255))

        # Перевірка натискання мишею на текст "Чутливість пташки"
        mouse_pos = pygame.mouse.get_pos()
        if 100 <= mouse_pos[0] <= 600 and 200 <= mouse_pos[1] <= 250:
            if pygame.mouse.get_pressed()[0]:
                player.sensitivity = (mouse_pos[0] - 100) // 5

    else:
        for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
            window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
            window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

        window.blit(player.image, (player.rect.x, player.rect.y))  

        display_text("Життя: " + str(player.lives), text_lives_position, font)  
        display_text("Очки: " + str(score), text_score_position, font)  

        press = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        click = press[0] or keys[pygame.K_SPACE]

        if timer > 0:
            timer -= 1

        for pipe_pair in pipes:
            pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect = pipe_pair
            pipe_top_rect.x -= 3
            pipe_bottom_rect.x -= 3
            if pipe_top_rect.right < 0:
                pipes.remove(pipe_pair)

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
                fall_sound.play()
                if player.lives == 0:
                    state = 'menu'
                else:
                    state = 'fall'
                    timer = 60
            for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
                if player.rect.colliderect(pipe_top_rect) or player.rect.colliderect(pipe_bottom_rect):
                    player.lives -= 1
                    fall_sound.play()
                    if player.lives == 0:
                        state = 'menu'
                    else:
                        state = 'fall'
        elif state == 'fall':
            state = 'start'
        else:
            pass

        if state == 'play':
            for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
                 if pipe_top_rect.right < player.rect.x and pipe_top_rect.right > 0 and pipe_top_rect.right < WIDTH // 2 and pipe_top_rect.right > player.rect.x - 3:
                    score += 10

        if state != 'start':
            pipes = [pipe_pair for pipe_pair in pipes if pipe_pair[2].right > 0]

        player.update_animation(sy)
    pygame.display.update()  
    clock.tick(FPS)
pygame.quit()





