import pygame
import sys
import random


def game_floor():
    screen.blit(floor_base, (floor_x_pos,450))
    screen.blit(floor_base, (floor_x_pos + 288,450))


def check_collision(pipes):
    # collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    # check floor is not hit
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        hit_sound.play()
        return False
    return True


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-150))
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)


pygame.init()
clock = pygame.time.Clock()

# variables
gravity = 0.125
bird_movement = 0
screen = pygame.display.set_mode((288, 512))

background = pygame.image.load("assets/background-day.png").convert()
bird = pygame.image.load("assets/yellowbird-midflap.png").convert()
bird_rect = bird.get_rect(center=(50,258))

floor_base = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

message = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = message.get_rect(center=(144,258))

# building pipes
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1800)

jump_sound = pygame.mixer.Sound('audio/jump.wav')
hit_sound = pygame.mixer.Sound('audio/hit.wav')

game_active = True
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                jump_sound.play()
            if event.key == pygame.K_SPACE and game_active== False:
                bird_rect.center = (50,225)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())


    screen.blit(background, (0,0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        # draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # check for collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)

    # create floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)