import pygame
import random

window = pygame.display.set_mode((600, 600))
back_color = (255, 255, 0)
game = True
bullets = []
bullets3 = []
player1 = pygame.Rect(100, 100, 50, 50)
clock = pygame.time.Clock()

while game:
    

    window.fill(back_color)
    pygame.draw.rect(window, (0, 0, 225), player1)

    if random.randint(0, 200) < 10:
        x = random.randint(10, 480) # Випадковий вибір між вертикальним і горизонтальним напрямом
        y = -10
        bullets.append(pygame.Rect(x, y, 20, 20))

    for b in bullets:
        pygame.draw.rect(window, (0, 0, 0), b)

    for b in bullets:
        b.y += 10
        if b.colliderect(player1):
            game = False

    if random.randint(0, 200) < 10:
        y = random.randint(10, 480)
        x = -10
        bullets3.append(pygame.Rect(x, y, 20, 20))            
            

    for b in bullets3:
        pygame.draw.rect(window, (0, 0, 0), b)          
            
            
            
    for b in bullets3:
        b.x += 10
        if b.colliderect(player1):            
            
            
            
            
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player1.x > 0:
        player1.x -= 3
    if keys[pygame.K_s] and player1.y < 550:
        player1.y += 3
    if keys[pygame.K_d] and player1.x < 550:
        player1.x += 3
    if keys[pygame.K_w] and player1.y > 0:
        player1.y -= 3
        if b.x > 600:  # Якщо пуля виходить за межі екрану справа
            bullets.remove(b)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    clock.tick(30)
    pygame.display.update()
