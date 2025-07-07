import pygame
import random
import os
import sys



pygame.init()

w = 800
h = 600

screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Flappy bird")
# Clock and FPS
clock = pygame.time.Clock()
FPS = 60
#color
blue = (0,0,255)
light_blue = (100,100,200)
light_red = (255,100,100)
red = (255,0,0)
white = (255,255,255)
yellow = (255, 255, 102)
green = (0,255,0)
black = (0,0,0)
red1 = (255, 73, 73)
# Game variables
gravity = 0.5
bird_y = h // 2
bird_x = 50
bird_velocity = 0
jump_strength = -10
pipe_speed = 5
pipe_gap = 190 
pipe_width = 100
score = 0
game_over = False
pipe_list = []
font = pygame.font.SysFont('comicsansms', 36)

# Function to get correct resource path
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

img_bird = pygame.image.load(resource_path('bird.png')).convert_alpha()
bird = pygame.transform.smoothscale(img_bird, (50,129/184*50))
img_pipe = pygame.image.load(resource_path('pipe.png')).convert_alpha()
pipe_ = pygame.transform.smoothscale(img_pipe, (pipe_width, 846/218*pipe_width))
img_pipe_reverse = pygame.image.load(resource_path('pipe_reverse.png')).convert_alpha()
pipe_reverse = pygame.transform.smoothscale(img_pipe_reverse, (pipe_width, 846/218*pipe_width))
bg_img = pygame.image.load(resource_path('bg.png')).convert()
bg = pygame.transform.smoothscale(bg_img, (800,600))

def create_pipe():
    pipe_height = random.randint(150, h - pipe_gap - 150)
    pipe_list.append({'x': w, 'top': pipe_height, 'bottom': pipe_height + pipe_gap})
    
def move_pipe():
    global pipe_list, score
    for pipe in pipe_list:
        pipe['x'] -= pipe_speed
        if pipe['x'] == bird_x:
            score += 1
    pipe_list = [pipe for pipe in pipe_list if pipe['x'] + pipe_width > 0]

def draw_pipes():
    for pipe in pipe_list: 
        # pygame.draw.rect(screen, green, (pipe['x'], 0, pipe_width, pipe['top']))
        screen.blit(pipe_reverse, (pipe['x'], pipe['top'] - 846/218*pipe_width ))
        # pygame.draw.rect(screen, green, (pipe['x'], pipe['bottom'], pipe_width, h - pipe['bottom']))
        screen.blit(pipe_, (pipe['x'], pipe['bottom']))

def check_collision():
    global game_over
    for pipe in pipe_list:
        if bird_x + 25 >= pipe['x'] and bird_x - 25 <= pipe['x'] + pipe_width and (bird_y - 22 < pipe['top'] or bird_y > pipe['bottom'] - 25):
            game_over = True
        if bird_y - 22 < 0 or bird_y + 25 > h:
            game_over = True
            
def reset_game(): 
    global bird_y, bird_velocity, pipe_list, score, game_over
    bird_y = h // 2
    bird_velocity = 0
    pipe_list = []
    score = 0
    game_over = False
    create_pipe()
def show_intro():
    """Display the intro screen until the user presses SPACE or clicks."""
    intro = True
    while intro:
        screen.fill(white)
        screen.blit(bg, (0, 0))

        title_text = font.render("FLAPPY BIRD", True, red)
        screen.blit(title_text, (w // 2 - title_text.get_width() // 2, h // 4))

        start_text = font.render("Press SPACE or CLICK to start", True, black)
        screen.blit(start_text, (w // 2 - start_text.get_width() // 2, h // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro = False
show_intro()

def game_loop():
    global bird_y, bird_velocity, game_over
    create_pipe()
    running = True
    while running : 
        screen.blit(bg, (0,0 ))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    bird_velocity = jump_strength
                elif event.button == 3:
                    reset_game()
            if event.type == pygame.KEYDOWN and not game_over :
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                reset_game()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                    reset_game()

                if event.key == pygame.K_ESCAPE:
                    running = False
        if not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity
            
            move_pipe()
            if pipe_list[-1]['x'] < w//2:
                create_pipe()
            check_collision()
        
        # pygame.draw.rect(screen, yellow, (bird_x, bird_y, 30,30))
        img_rect = bird.get_rect(center = (bird_x, bird_y))
        screen.blit(bird, img_rect)
        draw_pipes()

        score_text = font.render(f'Score: {score}', True, black)
        screen.blit(score_text, (10,10))
        if game_over:
            game_over_text = font.render('Game over! Press r/space or click to restart', True, red)
            screen.blit(game_over_text, (w//2 - game_over_text.get_width() // 2, h//2))
        pygame.display.flip()
        clock.tick(FPS) 
    pygame.quit()
    sys.exit()
    
game_loop()