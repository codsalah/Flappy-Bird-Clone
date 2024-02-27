import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((576, 1024)) #screen size
clock = pygame.time.Clock()


while True:
    # image of player 1
    # background image 
    # it will display these if theyre here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    pygame.display.update()
    clock.tick(90)