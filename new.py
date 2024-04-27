import pygame
import random
pygame.init()
font = pygame.font.Font(None,24)
text = font.render ("Текст", True,(0,0,0))



score = 0
window = pygame.display.set_mode((1366, 700))
back_color = (0, 255, 0)

players = [pygame.Rect(300, 225, 100, 200 ),
           pygame.Rect(500, 225, 100, 200 ),
           pygame.Rect(700, 225, 100, 200 ),
           pygame.Rect(900, 225, 100, 200 )]

text_on_area = random.choice(players)
start_time = pygame.time.get_ticks()
 


game = True
clock = pygame.time.Clock()

while game:
    window.fill(back_color)
    window.blit(text,(40,40))

    
    for pl in players:
        pygame.draw.rect(window, (0, 0, 225), pl)
    
    

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    if elapsed_time > 1000:
        text_on_area = random.choice(players)
        start_time = pygame.time.get_ticks()
    window.blit(text,(text_on_area.x,text_on_area.y))
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            y,x = event.pos
            if text_on_area.collidepoint(x,y):
                score += 1
                print (score)
        elif event.type == pygame.KEYDOWN:
            print(20)
    
    
    
    clock.tick(30)
    pygame.display.update() 