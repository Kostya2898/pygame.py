import pygame
import random

pygame.init()

class Player():
    def __init__(self, x, y, width, height, frames):
        self.frames = frames  
        self.index = 0  
        self.image = self.frames[self.index]  
        self.rect = self.image.get_rect()  
        self.rect.x = x  
        self.rect.y = y  
        self.width = width  
        self.height = height  
        self.lives = 3  
        self.rotation_angle = 0  # Початковий кут нахилу

    def update_animation(self, velocity):
        self.index += 0.1  
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        
        if velocity != 0:  # Перевірка, чи пташка летить
            # Застосування нахилу пташки вперед залежно від швидкості
            self.rotation_angle = min(max(-30, velocity * -2), 30)  # Кут нахилу пташки
        else:
            self.rotation_angle = 0  # Якщо не летить, нахил = 0

        self.image = pygame.transform.rotate(self.image, self.rotation_angle)

# Встановлення розмірів вікна та FPS
WIDTH, HEIGHT = 700, 600
FPS = 60

# Завантаження іконки вікна гри
icon_image = pygame.image.load('icon.png')
pygame.display.set_icon(icon_image)

# Встановлення заголовка вікна гри
pygame.display.set_caption("Flappy Bird")

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

state = 'menu'  # Початковий стан - меню
timer = 10  
pipes = []  
play = True  

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
pygame.mixer.music.load('music.mp3')  # Музика під час гри
pygame.mixer.music.play(-1)  # Запуск музики з постійним повторенням

# Додавання звуку при втраті життя
fall_sound = pygame.mixer.Sound('fall.wav')

# Завантаження зображення шестеренки
gear_image = pygame.image.load('download.png')
scaled_gear_width = 40  # Нова ширина зображення
scaled_gear_height = 40  # Нова висота зображення
gear_image = pygame.transform.scale(gear_image, (scaled_gear_width, scaled_gear_height))
gear_position = (10, 10)  # Координати зображення

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
                if start_button.collidepoint(mouse_pos):
                    state = 'start'
                    player.lives = 3
                    score = 0
                    timer = 10
                    pipes = []
                    py, sy, ay = HEIGHT // 2, 0, 0
                    player.rect.y = py
                if quit_button.collidepoint(mouse_pos):
                    play = False

    window.blit(background_image, (0, 0))  
    
    if state == 'menu':
        title_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        display_text("Flappy Bird", (WIDTH // 2, HEIGHT // 4), title_font, (255, 255, 255))
        start_button = draw_button("Почати гру", (WIDTH // 2, HEIGHT // 2), button_font, (255, 255, 255), (0, 0, 0))
        quit_button = draw_button("Вийти", (WIDTH // 2, HEIGHT // 2 + 100), button_font, (255, 255, 255), (0, 0, 0))
        
        # Зображення шестеренки
        window.blit(gear_image, gear_position)

    else:
        for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
            window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
            window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

        window.blit(player.image, (player.rect.x, player.rect.y))  

        # Відображення кількості життів та очок
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
                fall_sound.play()  # Відтворення звуку при втраті життя
                if player.lives == 0:
                    state = 'menu'
                else:
                    state = 'fall'
                    timer = 60
            for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
                if player.rect.colliderect(pipe_top_rect) or player.rect.colliderect(pipe_bottom_rect):
                    player.lives -= 1
                    fall_sound.play()  # Відтворення звуку при втраті життя
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

        player.update_animation(sy)  # Передача швидкості польоту для визначення нахилу пташки

    pygame.display.update()  
    clock.tick(FPS)

pygame.quit()


