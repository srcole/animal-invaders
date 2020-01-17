# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Choose fonts: https://www.dafont.com/

# Imports
import pygame as pg
import random
import math

# display variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_RGB = (60,40,10)
SCREEN_CAPTION = 'Animal Invaders'
SCORE_TEXT_X = 10
SCORE_TEXT_Y = 10

GAME_ICON_PATH = 'icons/png/001-panda.png'
BG_PATH = 'icons/me/kleines.jpg'
PLAYER_ICON_PATH = 'icons/png/002-lion.png'
ENEMY_A_ICON_PATH = 'icons/png/008-sloth.png'
BULLET_ICON_PATH = 'icons/png/015-hamster.png'


# game variables
random.seed = 0

PLAYER_START_HEIGHT = .2
PLAYER_SIZE = 64
PLAYER_SPEED = 3

N_ENEMIES = 6
ENEMY_A_START_HEIGHT = .8
ENEMY_A_SIZE = 32
ENEMY_A_X_BUFFER = 50
ENEMY_A_SPEED = 5
ENEMY_A_Y_SPEED = 20
ENEMY_A_ACCEL_PER_LINE = 1.5

BULLET_Y_SPEED = -10
BULLET_SIZE = 32



# initialize the game
pg.init()

# create display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pg.transform.scale(
    pg.image.load(BG_PATH), (SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(SCREEN_CAPTION)
pg.display.set_icon(pg.image.load(GAME_ICON_PATH))

# make sound
pg.mixer.music.load('icons/me/background.wav')
pg.mixer.music.play(-1)


# Init player
player_img = pg.transform.scale(pg.image.load(PLAYER_ICON_PATH),
                               (PLAYER_SIZE, PLAYER_SIZE))
playerX = (SCREEN_WIDTH - PLAYER_SIZE) / 2
playerY = SCREEN_HEIGHT * (1 - PLAYER_START_HEIGHT)
playerdX = 0

def player(x, y):
    screen.blit(player_img, (x, y))


# Init enemies
enemys_a_img = pg.transform.scale(pg.image.load(ENEMY_A_ICON_PATH),
                               (ENEMY_A_SIZE, ENEMY_A_SIZE))
enemys_a_X = [((SCREEN_WIDTH - ENEMY_A_SIZE) / 2) + 40*i for i in range(N_ENEMIES)]
enemys_a_Y = [SCREEN_HEIGHT * (1 - ENEMY_A_START_HEIGHT) + random.randint(-10, 200)] * N_ENEMIES
enemy_a_dX = ENEMY_A_SPEED
enemy_a_dY = 0

def enemy_a(xs, ys):
    for (x,y) in zip(xs, ys):
        screen.blit(enemys_a_img, (x, y))


# Init bullet
bullet_img = pg.transform.scale(pg.image.load(BULLET_ICON_PATH),
                               (BULLET_SIZE, BULLET_SIZE))
bullet_X, bullet_Y = playerX, playerY
bullet_state = 'ready'

def fire_bullet(x, y):
    global bullet_state
    screen.blit(bullet_img, (x, y))
    bullet_state = 'fired'

    bullet_sound = pg.mixer.Sound('icons/me/laser.wav')
    bullet_sound.play()

def update_bullet():
    global bullet_X, bullet_Y, bullet_state
    if bullet_state == 'fired':
        screen.blit(bullet_img, (bullet_X, bullet_Y))


# Determine if bullet hit enemy
def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt((enemy_X-bullet_X)**2 + (enemy_Y-bullet_Y)**2)
    if distance < 27:
        bullet_sound = pg.mixer.Sound('icons/me/explosion.wav')
        bullet_sound.play()
        return True
    else:
        return False


# introduce score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
def show_score():
    global SCORE_TEXT_X, SCORE_TEXT_Y
    score = font.render('Score: {}'.format(score_value), True, (255, 255, 255))
    screen.blit(score, (SCORE_TEXT_X, SCORE_TEXT_Y))

# init game over text
over_font = pg.font.Font('freesansbold.ttf', 64)
def print_over():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    score = font.render('GAME OVA, SUCKA', True, (255, 255, 255))
    screen.blit(score, (200, 200))


# game loop
running = True
playing = True
while running:
    if playing:

        # Respond to events
        for event in pg.event.get():

            # Check if keystroke
            if event.type == pg.KEYDOWN:

                # Move left / right
                if event.key == pg.K_LEFT:
                    playerdX = -PLAYER_SPEED
                if event.key == pg.K_RIGHT:
                    playerdX = PLAYER_SPEED

                # Fire bullet
                if event.key == pg.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_X = playerX
                        bullet_Y = playerY + (PLAYER_SIZE / 2) + 10
                        fire_bullet(bullet_X, bullet_Y)

            # Stop moving
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    playerdX = 0


            # Quit game
            if event.type == pg.QUIT:
                running = False

        # continuously

        # Make screen fill, drawn first (R,G,B)
        # screen.fill(SCREEN_RGB)
        screen.blit(background, (0,0))

        # Update player position
        playerX += playerdX
        if playerX < 0:
            playerX = 0
        elif playerX > (SCREEN_WIDTH - PLAYER_SIZE):
            playerX = SCREEN_WIDTH - PLAYER_SIZE

        # Reverse x direction if one enemy hits the edge
        enemys_a_min_X = min(enemys_a_X)
        if min(enemys_a_X) <= ENEMY_A_X_BUFFER:
            enemy_a_dX = -ENEMY_A_ACCEL_PER_LINE * enemy_a_dX
            enemy_a_dY = ENEMY_A_Y_SPEED
        elif max(enemys_a_X) >= (SCREEN_WIDTH - ENEMY_A_SIZE - ENEMY_A_X_BUFFER):
            enemy_a_dX = -ENEMY_A_ACCEL_PER_LINE * enemy_a_dX
            enemy_a_dY = ENEMY_A_Y_SPEED
        else:
            enemy_a_dY = 0

        # Update enemy A position
        enemys_a_X = [x + enemy_a_dX for x in enemys_a_X]
        enemys_a_Y = [y + enemy_a_dY for y in enemys_a_Y]

        # update bullet position
        enemies_dying = []
        if bullet_state == 'fired':
            bullet_Y += BULLET_Y_SPEED

            # Report a collision if one occurred
            for i_enemy in range(len(enemys_a_X)):
                bullet_hit = isCollision(enemys_a_X[i_enemy], enemys_a_Y[i_enemy], bullet_X, bullet_Y)
                if bullet_hit:
                    score_value += 1
                    enemies_dying.append(i_enemy)

        # Remove dead enemies and reset bullet
        for i_enemy in enemies_dying:
            enemys_a_X.pop(i_enemy)
            enemys_a_Y.pop(i_enemy)
            bullet_state = 'ready'

        # Reset bullet if out of screen
        if bullet_Y <= 0:
            bullet_state = 'ready'


        # If all enemies are dead, then restart
        if len(enemys_a_X) == 0:
            enemys_a_X = [((SCREEN_WIDTH - ENEMY_A_SIZE) / 2) + 40 * i for i in range(N_ENEMIES)]
            enemys_a_Y = [SCREEN_HEIGHT * (1 - ENEMY_A_START_HEIGHT) + random.randint(-10, 200)] * N_ENEMIES

        # If any enemies are at the player line, then end game
        if max(enemys_a_Y) >= (1 - PLAYER_START_HEIGHT) * SCREEN_HEIGHT - ENEMY_A_SIZE:
            # End game
            print_over()
            playing = False

        else:
            # Continue game
            # update blits
            player(playerX, playerY)
            enemy_a(enemys_a_X, enemys_a_Y)
            update_bullet()
            show_score()

        # update display
        pg.display.update()

    else:
        # Respond to events
        for event in pg.event.get():

            # Check if keystroke
            if event.type == pg.KEYDOWN:

                # Move left / right
                if event.key == pg.K_LEFT:
                    playerdX = -PLAYER_SPEED
                if event.key == pg.K_RIGHT:
                    playerdX = PLAYER_SPEED

                # Fire bullet
                if event.key == pg.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_X = playerX
                        bullet_Y = playerY + (PLAYER_SIZE / 2) + 10
                        fire_bullet(bullet_X, bullet_Y)

            # Stop moving
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    playerdX = 0


            # Quit game
            if event.type == pg.QUIT:
                running = False

        # continuously

        # Make screen fill, drawn first (R,G,B)
        # screen.fill(SCREEN_RGB)
        screen.blit(background, (0,0))

        print_over()
        show_score()
        pg.display.update()

