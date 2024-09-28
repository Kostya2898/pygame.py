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
        self.lives = 1  # Starting with 1 life
        self.rotation_angle = 0
        self.sensitivity = 50

    def update_animation(self, velocity):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        
        if velocity != 0:
            self.rotation_angle = min(max(-30, velocity * -2), 30)
        else:
            self.rotation_angle = 0

        self.image = pygame.transform.rotate(self.image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

WIDTH, HEIGHT = 700, 600
FPS = 60

icon_image = pygame.image.load('icon.png')
pygame.display.set_icon(icon_image)

pygame.display.set_caption("Flappy Bird")

background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

text_lives_position = (10, 10)
player_lives = 1  # Display 1 life

text_score_position = (10, 560)
score = 0

def display_text(text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, position)

py, sy, ay = HEIGHT // 2, 0, 0

bird_image = pygame.image.load('bird.png')
frame_width = bird_image.get_width() // 4
frame_height = bird_image.get_height()
bird_frames = [bird_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(4)]

player = Player(50, HEIGHT // 2, 50, 50, bird_frames)

state = 'menu'
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

    return pipe_top_image, pipe_bottom_image, pipe_top_rect, pipe_bottom_rect, False

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

fall_sound = pygame.mixer.Sound('fall.wav')

gear_image = None
gear_position = (10, 10)
try:
    gear_image = pygame.image.load('download.png').convert_alpha()
    gear_image = pygame.transform.scale(gear_image, (50, 50))
    gear_image.set_colorkey((255, 255, 255))
    gear_rect = gear_image.get_rect(topleft=gear_position)
except pygame.error:
    print("download.png")

music_button_image = None
music_button_position = (450, 150)
music_button_size = (80, 80)
music_on = True
try:
    music_button_image = pygame.image.load('downloadss.png').convert_alpha()
    music_button_image = pygame.transform.scale(music_button_image, music_button_size)
    music_button_rect = music_button_image.get_rect(topleft=music_button_position)
except pygame.error:
    print("downloadss.png")

def draw_button(text, position, font, color, bgcolor):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    button_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(window, bgcolor, button_rect)
    window.blit(text_surface, text_rect)

    return button_rect

def draw_music_button():
    if music_button_image:
        window.blit(music_button_image, music_button_position)

def draw_music_text():
    text_position = (music_button_position[0] - 100, music_button_position[1] + 25)
    display_text("Музика:", text_position, font, (0, 0, 0))

passed_pipes = []

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if state == 'menu':
                if start_button.collidepoint(mouse_pos):
                    state = 'start'
                elif quit_button.collidepoint(mouse_pos):
                    play = False
                elif gear_rect and gear_rect.collidepoint(mouse_pos):
                    state = 'settings'
            elif state == 'settings':
                if back_button.collidepoint(mouse_pos):
                    state = 'menu'
                elif music_button_rect and music_button_rect.collidepoint(mouse_pos):
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

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
        window.fill((128, 128, 128))
        title_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        display_text("Налаштування", (150, 10), title_font, (0, 0, 0))
        back_button = draw_button("Назад", (WIDTH // 2, HEIGHT // 2 + 100), button_font, (0, 0, 0), (255, 255, 255))
        draw_music_button()
        draw_music_text()
        
        # Відображення чутливості пташки та руху слайдера
        pygame.draw.rect(window, (192, 192, 192), (100, 250, 500, 50))  # Сірий фон для слайдера
        pygame.draw.rect(window, (0, 0, 0), (100 + player.sensitivity * 5, 250, 10, 50))  # Чорний слайдер
        display_text(" ", (20, 260), font, (0, 0, 0))
        display_text(str(player.sensitivity) + "%", (630, 260), font, (0, 0, 0))

        # Перевірка натискання мишею на текст "Чутливість пташки"
        mouse_pos = pygame.mouse.get_pos()
        if 100 <= mouse_pos[0] <= 600 and 250 <= mouse_pos[1] <= 300:
            if pygame.mouse.get_pressed()[0]:
                player.sensitivity = (mouse_pos[0] - 100) // 5

    else:
        for pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect, pipe_passed in pipes:
            window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
            window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

        window.blit(player.image, (player.rect.x, player.rect.y))  

        display_text("Життя: " + str(player.lives), text_lives_position, font)  
        display_text("Очки: " + str(score), text_score_position, font)  

        press = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        click = press[0] or keys[pygame.K_SPACE]

        ay = 1
        sy += ay
        py += sy * player.sensitivity / 50

        if click:
            sy = -10

        if state == 'start':
            timer += 1
            if timer >= 100:
                timer = 0
                pipe_top_image, pipe_bottom_image, pipe_top_rect, pipe_bottom_rect, pipe_passed = create_pipe()
                pipes.append((pipe_top_image, pipe_bottom_image, pipe_top_rect, pipe_bottom_rect, pipe_passed))

        for i, (pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect, pipe_passed) in enumerate(pipes):
            pipe_top_rect.x -= 2
            pipe_bottom_rect.x -= 2

            if pipe_top_rect.x <= -50:
                passed_pipes.append((pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect))
                pipes.pop(i)

                continue

            window.blit(pipe_top, (pipe_top_rect.x, pipe_top_rect.y))
            window.blit(pipe_bottom, (pipe_bottom_rect.x, pipe_bottom_rect.y))

            # Check collision with both top and bottom pipes
            if player.rect.colliderect(pipe_top_rect) or player.rect.colliderect(pipe_bottom_rect):
                player.lives -= 1
                fall_sound.play()

                if player.lives <= 0:
                    state = 'menu'  # Change game state to menu
                    pipes.clear()
                    passed_pipes.clear()
                    player.lives = 1
                    score = 0
                    timer = 10
                    sy = 0
                    py = HEIGHT // 2
                    break  # Exit the loop and return to menu

                # Reset player position
                py = HEIGHT // 2

            # Increase score when player passes through pipes
            if pipe_top_rect.right < player.rect.left and not pipe_passed:
                score += 1
                pipes[i] = (pipe_top, pipe_bottom, pipe_top_rect, pipe_bottom_rect, True)

        for passed_pipe in passed_pipes:
            window.blit(passed_pipe[0], (passed_pipe[2].x, passed_pipe[2].y))
            window.blit(passed_pipe[1], (passed_pipe[3].x, passed_pipe[3].y))

        player.rect.y = py

        if player.rect.y < 0 or player.rect.y + player.height > HEIGHT:
            player.lives -= 1
            fall_sound.play()

            if player.lives <= 0:
                state = 'menu'
                pipes.clear()
                passed_pipes.clear()
                player.lives = 1
                score = 0
                timer = 10
                sy = 0
                py = HEIGHT // 2

                # Reset player position
                py = HEIGHT // 2

        player.update_animation(sy)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()