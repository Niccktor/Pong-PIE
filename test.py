import serial
arduino = serial.Serial('COM9', 9600)
while True:
    line = arduino.readline()
    print(line)
arduino.close()

line_color = pygame.Color('grey12')
time.sleep(2)
while True:
    # Keyboard event
    event_handler()
    # Animation
    if jeu_fini() == False:
        ball_movement()
    else:
        if score_1 == 10:
            score_1 = "win"
            score_2 = "lose"
        else:
            score_2 = "win"
            score_1 = "lose"
        """if event.key == pygame.K_r:
            score_1 = 0
            score_2 = 0"""
    player_movement()
    # Visuals
    render()
    clock.tick(60)


    def jeu_fini():
        if score_1 == 10 or score_2 == 10 or score_1 == "Win" or score_2 == "Win":
            return True
        return False