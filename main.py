import pygame
import sys
import random

pygame.init()
################ Variables #####################

gravity = 0.12 # add this gravity to bird_movement
bird_movement = 0 #bird movementis goint to move bird rectangle
#when bird movement goes down => bird surface will go to diff position of the screen
width = 576/2
height = 1024/2
pipe_height = [280 , 320, 360, 380]
game_active = True
game_font = pygame.font.Font('font.ttf',20)
score = 0
high_score = 0
game_over_surface = pygame.image.load("assets/message.png")
game_over_rect = game_over_surface.get_rect(center = (width / 2, height / 2))

################ Functions #####################

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450)) # show the floor , we always control (0,0) at the top left
    screen.blit(floor_surface, (floor_x_pos + width, 450)) # putting this floor on the right side of the surface
    #now both are beside each other

def create_pipe():
    """
    Create a new pair of pipes with random heights
    """
    # Define min and max heights for pipes based on the screen height
    min_pipe_height = height * 0.25  # Minimum height (25% of the screen height)
    max_pipe_height = height * 0.8   # Maximum height (80% of the screen height)

    
    # Adjust the gap height range to be between 120 and 180
    min_gap_height = 150
    max_gap_height = 260

    # Calculate random gap height within the specified range
    gap_height = random.randint(min_gap_height, max_gap_height)

    # Calculate top and bottom pipe heights
    bottom_pipe_height = random.randint(int(min_pipe_height), int(max_pipe_height - gap_height))
    top_pipe_height = height - bottom_pipe_height - gap_height

    # Create rectangles for pipes
    bottom_pipe = pipe_surface.get_rect(midtop=(width, height - bottom_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(width, height - bottom_pipe_height - gap_height))

    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 1.7
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= height:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False,True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * 5, 1)
    return new_bird

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (width/2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        high_score_surface = game_font.render(f'High score: {int(score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (width/2, 420))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


screen = pygame.display.set_mode((width, height)) #screen size
clock = pygame.time.Clock()
bg_surface = pygame.image.load("assets/background-day.png")
floor_surface = pygame.image.load("assets/base.png")
floor_x_pos = 0
bird_surface = pygame.image.load("assets/bluebird-midflap.png")
bird_rect = bird_surface.get_rect(center=(width / 4.5, height / 3)) # rect that has the width and height of the bird
#the center of the rect at this coord point
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
spawn_pipe = pygame.USEREVENT   # this is triggered by timer
pygame.time.set_timer(spawn_pipe, 2000)

############################   Game loop   ############################
while True:
    # image of player 1
    # background image 
    # it will display these if they is an img here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5 
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (width / 4.5, height / 3)
                bird_movement = 0
                score = 0

        if event.type == spawn_pipe and game_active:
            pipe_list.extend(create_pipe())


             
    screen.blit(bg_surface, (0, 0)) # show the background , we always control (0,0) at the top left
    ####################### Bird Movement ####################
    if game_active:
        bird_movement += gravity # 0.25 => 0.5 => 0.75 => and so on
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        # we should update x axis for the base
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
    
    ######################      Pipe      ####################
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score += 0.08
        score_display('main_game')
    else: 
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        


    floor_x_pos -= 0.5 
    draw_floor()
    if floor_x_pos <= - width:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)