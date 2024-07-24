import pygame
import random
import math
import os

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# Set up screen dimensions
screen_width = 1000
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders, Developed by Shery")
pygame.display.update()

# Set up the game clock
clock = pygame.time.Clock()

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
green = (0, 255, 0)
fps = 60

# Load and scale background images
space_bg = pygame.image.load('images/space_bg.png')
space_bg = pygame.transform.scale(space_bg, (screen_width, screen_height)).convert_alpha()
gameover_img = pygame.image.load('images/gameover.jpg')
gameover_img = pygame.transform.scale(gameover_img, (screen_width, screen_height)).convert_alpha()

# Load and scale player image
player_img = pygame.image.load('images/space.png')
player_img = pygame.transform.scale(player_img, (100, 100)).convert_alpha()

# Function to draw player at given coordinates
def player(x, y):
    screen.blit(player_img, (x, y))

# Initialize enemy variables
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

# Load and scale enemy images, set their initial positions and movement
for i in range(num_of_enemies):
    enemy_surface = pygame.image.load('images/enemy.png')
    enemy_surface = pygame.transform.scale(enemy_surface, (80, 80)).convert_alpha()
    enemy_img.append(enemy_surface)
    enemy_x.append(random.randint(0, screen_width - 64))
    enemy_y.append(random.randint(5, 150))
    enemy_x_change.append(6)
    enemy_y_change.append(40)

# Function to draw enemy at given coordinates
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Load and scale bullet image
bullet_img = pygame.image.load('images/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (50, 50)).convert_alpha()
bullet_x = 0
bullet_y = screen_height - 100
bullet_y_change = 30
bullet_state = "ready"  # "ready" means you can't see the bullet on the screen

# Function to fire bullet from given coordinates
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 25, y - 25))

# Initialize score
score = 0

# Function to check collision between bullet and enemy
def is_collision(entity_x, entity_y, bullet_x, bullet_y, distance_threshold):
    distance = math.sqrt((math.pow(entity_x - bullet_x, 2)) + (math.pow(entity_y - bullet_y, 2)))
    return distance < distance_threshold

# Set up font for displaying text
font = pygame.font.SysFont(None, 45)

# Function to display text on screen
def screenText(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

# Welcome screen
def welcome():
    exit_game = False
    pygame.mixer.music.load('music/welcome.mp3')
    pygame.mixer.music.play(-1)  # Loop the welcome music
    while not exit_game:
        screen.fill(blue)
        screen.blit(space_bg, (0, 0))
        screenText("Welcome to Space Invaders", white, screen_width / 2 - 200, screen_height / 2 - 30)
        screenText("Press Space Bar To Play", white, screen_width / 2 - 200, screen_height / 2 + 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()  # Stop the welcome music
                    pygame.mixer.music.load('music/back.mp3')
                    pygame.mixer.music.play(-1)  # Loop the background music
                    gameLoop()
        pygame.display.update()
        clock.tick(fps)

# Main game loop
def gameLoop():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    # Read the highscore
    with open("highscore.txt", "r") as f:
        highscore = f.read()
        highscore = int(highscore)
    global bullet_x, bullet_y, bullet_state, score
    player_x = screen_width / 2
    player_y = screen_height - 100
    player_x_change = 0

    running = True
    game_over = False
    while running:
        screen.fill(black)
        screen.blit(space_bg, (0, 0))
        
        if game_over:
            # Writing the highscore
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            # What happens when the game is over
            screen.fill(black)
            screen.blit(gameover_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
            pygame.display.update()
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -5
                if event.key == pygame.K_RIGHT:
                    player_x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bullet_state == "ready":  # Left mouse button
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= screen_width - 100:
            player_x = screen_width - 100

        for i in range(num_of_enemies):
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 4
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= screen_width - 100:
                enemy_x_change[i] = -4
                enemy_y[i] += enemy_y_change[i]

            if is_collision(enemy_x[i], enemy_y[i], player_x, player_y, 50):
                pygame.mixer.music.load('music/gameover.mp3')
                pygame.mixer.music.play()
                game_over = True

            enemy(enemy_x[i], enemy_y[i], i)

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = "ready"
        for i in range(num_of_enemies):
            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y, 37):
                bullet_y = player_y
                bullet_state = "ready"
                score += 10
                if score > highscore:
                    highscore = score
                enemy_x[i] = random.randint(0, screen_width - 64)
                enemy_y[i] = random.randint(50, 150)
        
        player(player_x, player_y)
        screenText(f"Score: {score}", white, 5, 5)
        screenText(f"Highscore: {highscore}", white, screen_width - 400, 5)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

# Start the game
welcome()
