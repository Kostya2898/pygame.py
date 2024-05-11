import pygame
pygame.init()

class Player(): # клас для створення шаблону персонажа
    def __init__(self,x,y,width,height,image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))  # Зміна розміру зображення
        self.rect = self.image.get_rect() # "межі" персонажа
        self.rect.x = x # координати по ширині
        self.rect.y = y # координати по висоті
        self.width = width # ширина
        self.height = height # висота

# Встановлення розмірів вікна та FPS (кількість кадрів в секунду)
WIDTH, HEIGHT = 700, 600
FPS = 60
#створення фону
background_image = pygame.image.load('background.png')  # Замість 'background.jfif' вкажіть шлях до вашого зображення фону
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) # задання розмірів фонового зображення

 

# Створення вікна відображення та встановлення годинника
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Шрифт та розмір
font = pygame.font.Font(None, 36) # 36 - це розмір тексту, при потребі можна змінити на бажаний розмір
text = font.render("Очки:", True, (0,0,0)) # "Привіт!" - текст, який виводиться; (0,0,0) - колір у форматі RGB
text2 = font.render("Життя:", True, (0,0,0)) # "Привіт!" - текст, який виводиться; (0,0,0) - колір у форматі RGB

# Початкове положення гравця та швидкості його падіння
py, sy, ay = HEIGHT // 2, 0, 0
player = Player(50,50,50,50,"bird.png")

# Стан гри ('start' - початок гри, 'play' - гра в процесі, 'fall' - гравець падає)
state = 'start'

# Таймер для початку гри
timer = 10

# Список для зберігання труб, через які пролітає гравець
pipes = []

# Прапорець для керування ігровим циклом
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    # Відображення фону
    window.blit(background_image, (0, 0))
    window.blit(player.image, (player.rect.x, player.rect.y))  
    window.blit(text, (10,10)) # (10,10) - координати розміщення тексту
    window.blit(text2, (10,560)) # (10,10) - координати розміщення тексту
    
    # Отримання стану натискання миші та клавіш
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    # Зменшення таймера
    if timer > 0:
        timer -= 1

    # Оновлення позицій та видалення труб, що виходять за межі екрану
    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3
        if pipe.right < 0:
            pipes.remove(pipe)
        
    if state == 'start':
        # Якщо гра знаходиться в стані 'start', гравець рухається до центру екрану
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.rect.y = py
        
    elif state == 'play':
        # Якщо гра в процесі, обробляється натискання миші або клавіші пробіл,
        # визначається падіння гравця та створюються нові труби
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

        # Перевірка зіткнень гравця з трубами або виходу за межі екрану
        if player.rect.top < 0 or player.rect.bottom > HEIGHT:
            sy, ay = 0, 0
            state = 'fall'
            timer = 60

        for pipe in pipes:
            if player.rect.colliderect(pipe):
                state = 'fall'
        
    elif state == 'fall':
        # Якщо гравець впав або зіткнувся, гра повертається в стан 'start'
        state = 'start'
    
    else:
        pass
    
    # Відображення ігрових об'єктів

    for pipe in pipes:
        pygame.draw.rect(window, 'orange', pipe)
    

    
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
