import pygame
pygame.init()

class Player():
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.lives = 3

# Встановлення розмірів вікна та FPS
WIDTH, HEIGHT = 700, 600
FPS = 60
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
text_lives = font.render("Життя: ", True, (0,0,0))

# Змінні для лічильника очок
score = 0
font_score = pygame.font.Font(None, 36)
text_score = font_score.render("Очки: " + str(score), True, (0,0,0))

py, sy, ay = HEIGHT // 2, 0, 0
player = Player(50, 50, 50, 50, "bird.png")

state = 'start'
timer = 10
pipes = []
play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    window.blit(background_image, (0, 0))
    window.blit(player.image, (player.rect.x, player.rect.y))
    text_lives_display = font.render("Життя: " + str(player.lives), True, (0,0,0))
    window.blit(text_lives_display, (10, 560))

    # Лічильник очок
    text_score = font_score.render("Очки: " + str(score), True, (0,0,0))
    window.blit(text_score, (10, 10))

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

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

        if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, 200))
            pipes.append(pygame.Rect(WIDTH, 400, 50, 200))

        if player.rect.top < 0 or player.rect.bottom > HEIGHT:
            sy, ay = 0, 0
            player.lives -= 1
            if player.lives == 0:
                play = False
            else:
                state = 'fall'
                timer = 60

        for pipe in pipes:
            if player.rect.colliderect(pipe):
                player.lives -= 1
                if player.lives == 0:
                    play = False
                else:
                    state = 'fall'

    elif state == 'fall':
        state = 'start'

    else:
        pass

    # Лічильник очок - підрахунок при проходженні між трубами
    if state == 'play':
        for i in range(1, len(pipes), 2):  # Перевіряємо тільки верхні труби
            pipe = pipes[i]
            if pipe.x + pipe.width < player.rect.x and pipe.x + pipe.width > 0 and pipe.x + pipe.width < WIDTH // 2 and pipe.x + pipe.width > player.rect.x - 3:
                score += 10

    # Видалення труб, які знаходяться перед екраном, коли гра ще не закінчилася
    if state != 'start':
        pipes = [pipe for pipe in pipes if pipe.right > 0]

    for pipe in pipes:
        pygame.draw.rect(window, 'orange', pipe)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

