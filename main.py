# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# Imports
import pygame as pg
import random

# display variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_RGB = (60,40,10)
SCREEN_CAPTION = 'Animal Invaders'
GAME_ICON_PATH = 'icons/png/001-panda.png'
PLAYER_ICON_PATH = 'icons/png/002-lion.png'
ENEMY_A_ICON_PATH = 'icons/png/008-sloth.png'


# game variables
# random.seed = 0

PLAYERX_START_HEIGHT = .2
PLAYERX_SIZE = 64
PLAYERX_SPEED = 3

ENEMY_A_START_HEIGHT = .8
ENEMY_A_SIZE = 64
ENEMY_A_X_BUFFER = 50
ENEMY_A_SPEED = 5
ENEMY_A_Y_SPEED = 20


# initialize the game
pg.init()

# create display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(SCREEN_CAPTION)
pg.display.set_icon(pg.image.load(GAME_ICON_PATH))


# Init player
player_img = pg.transform.scale(pg.image.load(PLAYER_ICON_PATH),
                               (PLAYERX_SIZE, PLAYERX_SIZE))
playerX = (SCREEN_WIDTH - PLAYERX_SIZE) / 2
playerY = SCREEN_HEIGHT * (1 - PLAYERX_START_HEIGHT)
playerdX = 0

def player(x, y):
    screen.blit(player_img, (x, y))


# Init enemy A
enemy_a_img = pg.transform.scale(pg.image.load(ENEMY_A_ICON_PATH),
                               (ENEMY_A_SIZE, ENEMY_A_SIZE))
enemy_a_X = (SCREEN_WIDTH - ENEMY_A_SIZE) / 2 + random.randint(-200, 200)
enemy_a_Y = SCREEN_HEIGHT * (1 - ENEMY_A_START_HEIGHT) + random.randint(-10, 200)
enemy_a_dX = ENEMY_A_SPEED
enemy_a_dY = 0

def enemy_a(x, y):
    screen.blit(enemy_a_img, (x, y))


# game loop
running = True
while running:

    # Respond to events
    for event in pg.event.get():

        # Check if keystroke
        if event.type == pg.KEYDOWN:
            print(event.key)

            # Move left / right
            if event.key == pg.K_LEFT:
                playerdX = -PLAYERX_SPEED
            if event.key == pg.K_RIGHT:
                playerdX = PLAYERX_SPEED

        # Stop moving
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                playerdX = 0


        # Quit game
        if event.type == pg.QUIT:
            running = False

    # continuously

    # Make screen fill, drawn first (R,G,B)
    screen.fill(SCREEN_RGB)

    # Update player position
    playerX += playerdX
    if playerX < 0:
        playerX = 0
    elif playerX > (SCREEN_WIDTH - PLAYERX_SIZE):
        playerX = SCREEN_WIDTH - PLAYERX_SIZE

    # Update enemy A position
    enemy_a_X += enemy_a_dX
    enemy_a_Y += enemy_a_dY
    if enemy_a_X <= ENEMY_A_X_BUFFER:
        enemy_a_X = ENEMY_A_X_BUFFER
        enemy_a_dX = -enemy_a_dX
        enemy_a_dY = ENEMY_A_Y_SPEED
    elif enemy_a_X >= (SCREEN_WIDTH - ENEMY_A_SIZE - ENEMY_A_X_BUFFER):
        enemy_a_X = SCREEN_WIDTH - ENEMY_A_SIZE - ENEMY_A_X_BUFFER
        enemy_a_dX = -enemy_a_dX
        enemy_a_dY = ENEMY_A_Y_SPEED
    else:
        enemy_a_dY = 0

    # update player
    player(playerX, playerY)
    enemy_a(enemy_a_X, enemy_a_Y)

    # update display
    pg.display.update()
