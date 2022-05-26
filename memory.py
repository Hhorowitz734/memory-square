# MODULES
import pygame
import math
from random import randint
pygame.mixer.init()
pygame.font.init()


# VARIABLES
screen_width = 600
screen_height = 600
tile_size = 200
total_tiles = int((screen_height * screen_width) / (tile_size ** 2))
rows = int((screen_height / tile_size))
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Memory Game")
score = 0
tile = pygame.image.load("tile.png")
tile = pygame.transform.scale(tile, (tile_size, tile_size))
right = pygame.image.load("right.png")
right = pygame.transform.scale(right, (tile_size, tile_size))
ms_wait = 500
guessing = False
score = 0
right_tiles = []
ding = pygame.mixer.Sound("ding.wav")
# font = pygame.font.SysFont(None, 24)


# CHECKS IF A MOUSE IS OVER A RECTANGLE
def is_over(rect, pos):
    return True if rect.collidepoint(pos[0], pos[1]) else False

# DRAWS THE GRID THAT CREATES THE GAME
def draw_grid():
    for line in range(0, rows):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# SETS UP THE SCREEN FOR GUESSING
def setup_guessing():
    global guessing_index
    guessing_index = [] # List to be used for storing where the guessed tiles will be
    global rects
    rects = []
    for j in range(int(3 + score)):
        randomval = randint(0, total_tiles) 
        while randomval in guessing_index: #Searches for duplicates and makes code rerun in any found
            randomval = randint(0, total_tiles)
        guessing_index.append(randomval)
    print(guessing_index)
    for i in range(int(len(guessing_index))):
        ypos = math.floor(guessing_index[i] / (total_tiles / rows)) * (screen_height / rows)
        xpos = (guessing_index[i] % (total_tiles / rows)) * (screen_height / rows)
        rects.append(pygame.Rect(xpos, ypos, tile_size, tile_size))
        screen.blit(tile, (xpos,ypos))
        pygame.display.update()
    print(rects)
    pygame.time.delay(ms_wait)
    global guessing
    guessing = True

# CHECKS IF GUESS IS CORRECT AND ADDS SQUARE TO CORRECT TILES
def check_guess():
    global right_tiles
    global score
    for i in range(int(len(rects))):
        pos = pygame.mouse.get_pos() 
        if is_over(rects[i], pos): 
            right_tiles.append(rects[i])
            rects.pop(i)
            pygame.mixer.Sound.play(ding)
            pygame.mixer.music.stop()
            break
        else: 
            pass # Add functionality here that ends game and allows user to restart
    if len(rects) == 0:
        global tile_size, tile, right, rows, total_tiles, ms_wait
        right_tiles = []
        score += 1
        tile_size -= 1
        while (screen_height * screen_width) % (tile_size ** 2) != 0:
            tile_size -= 1
        rows = int((screen_height / tile_size))
        ms_wait += 300
        total_tiles = int((screen_height * screen_width) / (tile_size ** 2))
        tile = pygame.transform.scale(tile, (tile_size, tile_size))
        right = pygame.transform.scale(right, (tile_size, tile_size))
        screen.fill((0,0,0))
        draw_grid()
        setup_guessing()

# DISPLAYS GREEN ON CORRECT TILES
def display_right():
    for x in range(len(right_tiles)):
        pygame.draw.rect(screen, (124, 252, 0), right_tiles[x])


running = True
while running:
    screen.fill((0,0,0))
    draw_grid()
    display_right()
    # img = font.render(f"Score: {score}", True, (255, 255, 255))
    # screen.blit(img, (20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                setup_guessing()
        if event.type == pygame.MOUSEBUTTONUP:
            if guessing:
                check_guess()

    pygame.display.update()
    
