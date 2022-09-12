import time
import pygame
import random
import serial
import threading
import sys
import pygame_menu

#


# pyfirmata pour faire le lien entre Arduino et python
# https://pyfirmata.readthedocs.io/en/latest/
# https://arduinofactory.fr/pyfirmata/


def end():
    global kill_thread
    pygame.quit()
    kill_thread = True
    thread.join(timeout=5)
    sys.exit()


def arduino_thread():
    global moyenne
    global moyenne2
    global player_min_value
    global player_max_value

    player_min_value = 0
    player_max_value = 0
    moyenne2 = 0
    moyenne = 0
    value1 = 0
    i = 0

    while True:
        if kill_thread:
            break
        payload = arduino.readline().decode('UTF-8')
        if payload.startswith('a'):
            payload = payload[1:]
            payload = payload[0:num_len(payload)]
            if 1 < int(payload) < 200:
                moyenne = int(payload)
        elif payload.startswith('b'):
            payload = payload[1:]
            payload = payload[0:num_len(payload)]
            if 1 < int(payload) < 200:
                moyenne2 = int(payload)
            """
            Autre facon de faire (Valeurs moyenne sur I valeurs) --- réactif 
            i2 += 1
            
            if value2 > 400:
                value2 = moyenne2
            if i2 > 4:
                value2 = value2 / 4
                moyenne2 = value2
                value2 = 0
                i2 = 0"""


def num_len(string):
    i = 0
    while '0' <= string[i] <= '9':
        i += 1
    return i


def set_mode(mode, nb):
    global game_mode
    game_mode = nb


def init_player():
    global player
    global player_color_selected
    global player_color
    global player_speed
    global score_1
    global moyenne

    player = pygame.Rect(10, (height_screen / 2 - 70), 10, 140)
    player_color = pygame.Color(player_color_selected)
    player_speed = 0
    score_1 = 0
    moyenne = 0


def init_opponent():
    global opponent
    global opponent_color
    global opponent_speed
    global opponenet_score
    global moyenne2
    global opponent_color_selected

    opponent = pygame.Rect((width_screen - 20), (height_screen / 2 - 70), 10, 140)
    opponent_color = pygame.Color(opponent_color_selected)
    opponent_speed = 0
    opponenet_score = 0
    moyenne2 = 0


def init_ball():
    global ball_size
    global ball
    global ball_color
    global ball_speed_x
    global ball_speed_y
    global ball_get_hit

    ball_size = 40
    ball = pygame.Rect(width_screen / 2 - ball_size / 2, height_screen / 2 - ball_size / 2, ball_size, ball_size)
    ball_color = pygame.Color('blue')
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    ball_get_hit = False


def start_game():
    global play
    global game_fini

    play = True
    game_fini = False
    init_player()
    init_opponent()
    init_ball()
    if menu.enable():
        menu.disable()
    if option_menu.enable():
        option_menu.disable()


def set_top_value_player():
    print(str(moyenne2))
    option_menu.clear()
    draw_option_menu()


def set_color(color, player, nb):
    global opponent_color_selected
    global player_color_selected

    color = None
    match nb:
        case 0:
            color = 'darkblue'
        case 1:
            color = 'green'
        case 3:
            color = 'lawngreen'
        case 4:
            color = 'orange'
        case 5:
            color = 'yellow'
        case 6:
            color = 'red'
        case 7:
            color = 'blue'
        case _:
            color = 'green'
    if player == 1:
        player_color_selected = color
    elif player == 2:
        opponent_color_selected = color


def set_possition(player, type):
    global player_min_value
    global player_max_value
    global opponent_min_value
    global opponent_max_value

    if player == 'PLAYER':
        if type == 'TOP':
            player_min_value = moyenne
        elif type == 'BOTTOM':
            player_max_value = moyenne
    elif player == 'OPPONENT':
        if type == 'TOP':
            opponent_min_value = moyenne2
        elif type == 'BOTTOM':
            opponent_max_value = moyenne2
    draw_option_menu()


def set_difficulty(difficulty, nb):
    global IA_speed

    match nb:
        case 1:
            print('Easy')
            IA_speed = 7
        case 2:
            print('Meduim')
            IA_speed = 7.5
        case 3:
            print('Hard')
            IA_speed = 8
        case _:
            IA_speed = 9



def draw_option_menu():
    global option_menu

    if menu.is_enabled():
        menu.clear()
        menu.close()
    if option_menu.is_enabled() == False:
        option_menu.enable()
        option_menu.clear()
    else:
        option_menu.clear()

    option_menu.add.button('Player :', None)
    option_menu.add.selector('Color : ', [('green', 1, 1), ('blue', 1, 7), ('darkblue', 1, 0), ('lawngreen', 1, 3),
                                          ('orange', 1, 4), ('yellow', 1, 5), ('red', 1, 6)], onchange=set_color)
    option_menu.add.button('Bottom value : ' + str(player_min_value), set_possition, 'PLAYER', 'TOP')
    option_menu.add.button('Top value : ' + str(player_max_value), set_possition, 'PLAYER', 'BOTTOM')
    option_menu.add.button('', None)
    option_menu.add.button('Opponent :', None)
    option_menu.add.selector('Difficulty :', [('Easy', 1), ('Meduim', 2), ('Hard', 3)], onchange=set_difficulty)
    option_menu.add.selector('Color : ', [('red', 2, 6), ('blue', 2, 7), ('darkblue', 2, 0), ('green', 2, 1), ('lawngreen', 2, 3), ('orange', 2, 4), ('yellow', 2, 5)], onchange=set_color)
    option_menu.add.button('Bottom value : ' + str(opponent_min_value), set_possition, 'OPPONENT', 'TOP')
    option_menu.add.button('Top value : ' + str(opponent_max_value), set_possition, 'OPPONENT', 'BOTTOM')
    option_menu.add.button('Retour', draw_menu)
    option_menu.mainloop(screen)


def draw_menu():
    global menu
    if option_menu.is_enabled():
        option_menu.clear()
        option_menu.close()
    if menu.is_enabled() == False:
        menu.enable()
        menu.clear()

    menu.add.selector('Mode : ', [('1 Player', 1), ('2 Players', 2)], onchange=set_mode)
    menu.add.button('Play', start_game)
    menu.add.button('Option', draw_option_menu)
    menu.add.button('Quit', end)
    menu.mainloop(screen)


def event_handler():
    global player_speed
    global opponent_speed
    global play

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            arduino.close()
            thread.join()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu.clear()
                menu.enable()
                play = False
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_DOWN:
                player_speed = 7
            if event.key == pygame.K_z:
                opponent_speed = -7
            if event.key == pygame.K_s:
                opponent_speed = 7
        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            # player_speed = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                opponent_speed = 0


def ball_movement():
    global ball_speed_x
    global ball_speed_y
    global score_1
    global opponenet_score
    global ball_get_hit
    global game_fini

    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= height_screen:
        ball_speed_y *= -1
        wall_sound.play(0)
    if ball.left <= 0 or ball.right >= width_screen:
        if random.randint(1, 100) != 100:
            la_chatte.play(0)
        else:
            score_sound.play(0)
        if ball.left <= 0:
            opponenet_score += 1
            if (opponenet_score >= 7):
                game_fini = True

        else:
            score_1 += 1
            if score_1 >= 7:
                game_fini = True


        ball_restart()
    if (ball.colliderect(opponent) or ball.colliderect(player)) and ball_get_hit == False:
        ball_get_hit = True
        ball_speed_x *= random.randint(101, 105) / 100 * -1
        ball_speed_y *= random.randint(101, 105) / 100 #1.05
        paddle_sound.play(0)
        print("Ball speed x : ", ball_speed_x, "ball speed y : ", ball_speed_y)
    elif ball_get_hit:
        ball_get_hit = False

def player_movement():
    if player_min_value <= moyenne <= player_max_value:
        player.y = (height_screen / (player_min_value - player_max_value)) * (moyenne - player_max_value)

    if game_mode == 1:  # opponent IA suit la balle a une vitesse donnée
        if opponent.centery < ball.centery:
            opponent.centery += IA_speed
        elif opponent.centery > ball.centery:
            opponent.centery -= IA_speed
    else:
        if opponent_min_value <= moyenne2 <= opponent_max_value:
            opponent.y = (height_screen / (opponent_min_value - opponent_max_value)) * (moyenne2 - opponent_max_value)
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height_screen:
        player.bottom = height_screen

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height_screen:
        opponent.bottom = height_screen


def ball_restart():
    global ball_speed_x
    global ball_speed_y

    ball.center = (width_screen / 2, height_screen / 2)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    while pygame.mixer.get_busy():
        event_handler()
        player_movement()
        render()
        clock.tick(60)


def render():
    # Fill background
    screen.fill(background_color)

    # Affichage Score
    if game_fini == False:
        opponenet_score_img = font.render(str(opponenet_score), True, pygame.Color(opponent_color))
        score_1_img = font.render(str(score_1), True, pygame.Color(player_color))

        screen.blit(opponenet_score_img, ((width_screen / 4 * 3) - opponenet_score_img.get_width() / 2, 20))
        screen.blit(score_1_img, (width_screen / 4 - score_1_img.get_width() / 2, 20))

    # Affichage Joueurs 1 et 2
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, opponent_color, opponent)

    # Affichage milieu terrain
    pygame.draw.aaline(screen, line_color, [width_screen / 2, 0], [width_screen / 2, height_screen])
    pygame.draw.ellipse(screen, ball_color, ball)
    if game_fini:
        if opponenet_score > score_1:
            result = font2.render('Opponent  Victory', True, pygame.Color(opponent_color))
        else:
            result = font2.render('Player Victory', True, pygame.Color(opponent_color))
        screen.blit(result, (width_screen  / 2 - result.get_width() / 2, (height_screen / 4 - result.get_height() / 2)))

    # Update screen
    pygame.display.flip()


try :
    kill_thread = False
    arduino = serial.Serial('COM9', 9600)
    thread = threading.Thread(target=arduino_thread)
    thread.start()
except :
    print('Arduino probelme')
    sys.exit()
"""
arduino = PyMata("COM9")
arduino.sonar_config(8, 7)
data = arduino.get_sonar_data()
port = 'COM9'
HIGH = True
LOW = False
kill_thread = False
arduino = pyfirmata.Arduino(port)
ECHO_pin = arduino.get_pin('d:7:i')
TRIG_pin = arduino.get_pin('d:8:o')
# LED_pin = arduino.get_pin('d:8:o')
x = threading.Thread(target=Arduino_thread)
x.start()
#https://github.com/tino/pyFirmata/pull/45/files/c476236847cd8bb655c0fb645a1ce69b28d0e2d2
ECHO_pin = arduino.get_pin('d:7:o')
TRIG_pin = arduino.get_pin('d:8:i')

TRIG_pin.write(HIGH)
time.sleep(20/1000)
TRIG_pin.write(LOW)
dist = ECHO_pin.ping()
"""
# Générer la fenêtre
pygame.init()
clock = pygame.time.Clock()
width_screen = 1245
height_screen = 934
screen = pygame.display.set_mode((width_screen, height_screen))
pygame.display.set_caption("PIE 2022 Pong")
background_color = pygame.Color('grey43')
play = False
game_fini = False

# Initialisation  des menus
option_menu = pygame_menu.Menu('Options', width_screen, height_screen, theme=pygame_menu.themes.THEME_DARK)
menu = pygame_menu.Menu('Welcome on Wiipong', width_screen, height_screen, theme=pygame_menu.themes.THEME_DARK)

# Init gamemode
game_mode = 1

# Style du text
font = pygame.font.SysFont(None, 400)
font2 = pygame.font.SysFont(None, 100)

# Sound Effect load
paddle_sound = pygame.mixer.Sound(r'Sound\paddle.wav')
wall_sound = pygame.mixer.Sound(r'sound\wall.wav')
score_sound = pygame.mixer.Sound(r'sound\score.wav')
la_chatte = pygame.mixer.Sound(r'sound\chatte.wav')

player_min_value = 10
player_max_value = 200
opponent_min_value = 10
opponent_max_value = 200
ball_get_hit = False
IA_speed = 3

player_color_selected = 'green'
opponent_color_selected = 'red'

# line
line_color = pygame.Color('grey12')
time.sleep(2)

while True:

    # Keyboard event
    # Animation
    if play:
        event_handler()
        if game_fini == False:
            ball_movement()
        player_movement()
        render()
    else:
        draw_menu()
    clock.tick(60)
    # Visuals
