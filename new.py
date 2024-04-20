import pygame
import random
pygame.init()
font = pygame.font.Font(None,24)
text = font.render ("Текст", True,(0,0,0))




window = pygame.display.set_mode((1366, 700))
back_color = (0, 255, 0)




player = pygame.Rect(300, 225, 100, 200 )
player1 = pygame.Rect(500, 225, 100, 200 )
player2 = pygame.Rect(700, 225, 100, 200 )
player3 = pygame.Rect(900, 225, 100, 200 )





game = True
clock = pygame.time.Clock()

while game:
    
    window.fill(back_color)
    window.blit(text,(40,40))
    pygame.draw.rect(window, (0, 0, 225), player)
    pygame.draw.rect(window, (0, 0, 225), player1)
    pygame.draw.rect(window, (0, 0, 225), player2)
    pygame.draw.rect(window, (0, 0, 225), player3)
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(10)
        elif event.type == pygame.KEYDOWN:
            print(20)
    
    
    
    clock.tick(30)
    pygame.display.update() 