import pygame
import random

pygame.init()

# Завантаження звуків
crash_sound = pygame.mixer.Sound('fall.wav')  # Звук при зіткненні
pygame.mixer.music.load('music.mp3')  # Музика під час гри

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

    def update_animation(self):
        self.index += 0.1  
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

# Встановлення розмірів вікна та FPS
WIDTH, HEIGHT = 700, 600
FPS = 60
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
def display_text(text, position):
    text_surface = font.render(text, True, (0,0,0))
    window.blit(text_surface, position)

py, sy, ay = HEIGHT // 2, 0, 0

bird_image = pygame.image.load('bird.png')
frame_width = bird_image.get_width() // 4  
frame_height = bird_image.get_height()
bird_frames = [bird_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(4)]

player = Player(50, 50, 50, 50, bird_frames)

state = 'start'  
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

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    window.blit(background_image, (0, 0))  
    
    for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect in pipes:
        window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
        window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

    window.blit(player.image, (player.rect.x, player.rect.y))  
    
    # Відображення кількості життів та очок
    display_text("Життя: " + str(player.lives), text_lives_position)  
    display_text("Очки: " + str(score), text_score_position)  

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
            pygame.mixer.music.play(-1)  # Початок програвання музики
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
                crash_sound.play()  # Відтворення звуку зіткнення
                if player.lives == 0:
                    play = False
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

    player.update_animation()

    pygame.display.update()  
    clock.tick(FPS)

pygame.quit()  

