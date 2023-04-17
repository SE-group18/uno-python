import game_classes
import pygame
from pygame.locals import *
import display_funct
import json
import game_logic
import PY_UNO
from deck_gen import gen_rand_deck
import game_AI
import game_classes
import os
import game_story_setting

pygame.init()

game_font = pygame.font.Font('NanumGothic.ttf', 15)

#Defaul 설정
player_total = 0
screen_width, screen_height = 1600, 900
option = False
setting = False
title = True
sound = 5
mainsound = 5
subsound = 5
color_option = "off"
i = 0
full = False
s_playing = True
instorymode = True
cur_stage = 0
cleared1 = True
cleared2 = True
cleared3 = True
cleared4 = True

#불러오기
try:
    with open("config.txt", "r") as f:
        config = json.load(f)
    print(1)
    screen_width = config["screen_width"]
    screen_height = config["screen_height"]
    sound = config["sound"]
    mainsound = config["mainsound"]
    subsound = config["subsound"]
    color_option = config["color_option"]
    full = config["full"]

except:
    pass


# global screen vairable to be used globaly (as all parts of the game
# refrence the same screen)
global screen

# colors definitions for pygame
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)

# defining screen 16:9 native

scale_size = (screen_width, screen_height)
scale_card_size = 0

# scaling factors that are initially set the scale value of 1 (native to
# 1600x900 pixel resolution)
scale_x = 1
scale_y = 1

# defining the global pygame screen value to be used within PY-UNO
if full == False:
    screen = pygame.display.set_mode((screen_width, screen_height), HWSURFACE | DOUBLEBUF)
else:
    screen = pygame.display.set_mode((screen_width, screen_height), HWSURFACE | DOUBLEBUF | FULLSCREEN)
screen.fill(black)

# default card rectangle size and card size and default card pygame rectangle
card_width = screen_width/12.3
card_height = screen_height/4.9
def_rect = pygame.Rect(0, 0, card_width, card_height)

# defining the default facedown card value
face_down_card = game_classes.Card(
    "face_down", "small_cards/card_back.png", None)


def handle_resize(event):
    """
    Small function that is called when the PY-GAME window is resized.

    Functinon updates the scale_x and scale_y globals for easy resizing display
    functionality.

    O(1) runtime
    """
    # grabbing the newely resized windows size
    scale_size = event.dict['size']

    # save these scaling factors globally as they affect the global screen
    # rendering
    global scale_x
    global scale_y

    # grabbing new scaling factor values
    (x_o, y_o) = (screen_width, screen_height)
    (x_1, y_1) = scale_size
    # calculating new scaling factor values
    scale_x = (x_1 / x_o)
    scale_y = (y_1 / y_o)


def scale_card_blit(image, position, transform_ov=False):
    """
    Scaling blit function that uses the scale_x and scale_y globals for
    correctly transforming the image onto a resized screen.

    This function both scales the position of the image and the size of the
    image itself aswell.

    O(1) runtime (neglecting blit)
    """
    # scale the inputted card image to the global scale factors
    if transform_ov:  # transform override for half image transform
        image = pygame.transform.scale(
            image, (card_width // 2, card_height // 2))
    else:
        image = pygame.transform.scale(image, (card_width, card_height))
    # scale the images position with the global scale factors
    l = int(position.left * scale_x)
    t = int(position.top * scale_y)
    w = int(position.width * scale_x)
    h = int(position.height * scale_y)

    scale_pos = pygame.Rect(l, t, w, h)
    screen.blit(image, scale_pos)


def draw_top_stack_card(board):
    """
    Renders the top card of the card_stack on the board.

    O(1) runtime
    """
    if board.card_stack != []:
        top_card = board.card_stack[-1]
        top_card.rect = def_rect
        top_card.rect = top_card.rect.move(
            (screen_width - card_width) // 2 + (card_width//2)+(card_width//4),
            (screen_height - card_height) // 2)

        # blit top card of board onto center screen
        scale_card_blit(top_card.card_data, top_card.rect)


def draw_stack_card(board):
    stack_card = game_classes.Card(
        "red", "small_cards/card_back.png", None)
    stack_card.rect = stack_card.rect.move(
            (screen_width - card_width) // 2 - (card_width//2)-(card_width//4),
            (screen_height - card_height) // 2)
    scale_card_blit(stack_card.card_data, stack_card.rect)


def redraw_hand_visble(player, selected=None):
    """
    Redraws a players hand to be face up.

    O(n) runtime where n is the size of the players hand
    """
    # player playing indicator placeholder graphic
    player_num = str(player.name[7])
    card_disp = game_classes.Card(
        "red", "small_cards/red_" + player_num + ".png", None)
    card_disp.rect = card_disp.rect.move(0, screen_height - card_height)

    # dynamic card spacing
    player_handsize = len(player.hand)
    if player_handsize <= 9:
        iterating_fact = 100
    else:
        iterating_fact = (3 * (screen_width // 4)) // player_handsize

    # get a "middle" start postion for bliting cards
    start_pos = (screen_width - 100 * len(player.hand)) // 2
    if start_pos < 150:
        start_pos = 150

    card_index = 0
    for card in player.hand:  # O(n)
        card.rect = def_rect
        if card_index == selected:
            card.rect = card.rect.move(start_pos, screen_height*6/9)
        else:
            card.rect = card.rect.move(start_pos, screen_height*7/9)

        card.rect = card.rect.move(iterating_fact * card_index, 0)
        scale_card_blit(card.card_data, card.rect)

        card_index += 1

    # displaying the placeholder playing player number
    scale_card_blit(card_disp.card_data, card_disp.rect)


def redraw_hand_nonvisble(player, start_horz, start_vert=0):
    """
    Draws a players hand to be non-visible (face down cards).

    O(n) runtime where n is the size of the players hand
    """
    # placeholder player num graphics
    player_num = str(player.name[7])
    card_disp = game_classes.Card(
        "red", "small_cards/red_" + player_num + ".png", None)
    card_disp.rect = card_disp.rect.move(start_horz, start_vert)

    # dynamic card spacing
    player_handsize = len(player.hand)
    if player_handsize <= 7:
        iterating_fact = 80
    else:
        iterating_fact = 550 // player_handsize

    card_index = 0
    for card in player.hand:  # O(n)
        card.rect = def_rect
        card.rect = card.rect.move(start_horz, start_vert)
        card.rect = card.rect.move(iterating_fact * card_index, 0)
        scale_card_blit(face_down_card.card_data, card.rect)

        card_index += 1

    # displaying the placeholder player num graphics
    scale_card_blit(card_disp.card_data, card_disp.rect, True)


def redraw_hand_nonvisble_loop(players_temp):
    """
    Loop function that orders rendering players_temps hands facedown onto the
    screen. redraw_hand_nonvisble is used within this loop to actually do the
    rendering. This loop simply orders each hands location on the screen.

    O(m*n) runtime where m is the amount of players to be drawn and
    n is the size of the players hand. Since both of these sizes should be
    relatively small optimizing was considered negligible.
    """
    start_horz = 0
    start_vert = 0
    loop_iteration = 0
    # draw all active other hands in nice other places in the screen
    for player in players_temp:  # O(m*n)

        if len(player.hand) == 0:
            hand_size = card_width
        elif len(player.hand) > 7:
            hand_size = (80 * 7) + (card_width - 80)
        else:
            hand_size = (80 * len(player.hand)) + (card_width - 80)

        if loop_iteration == 1:
            start_horz = screen_width - hand_size

        elif loop_iteration > 1:
            start_vert = start_vert + card_height + 20
            start_horz = 0
            loop_iteration = 0

        redraw_hand_nonvisble(player, start_horz, start_vert)  # O(n)

        loop_iteration += 1


def redraw_screen(player_you, board, players_other):
    """
    Redraws the screen to its "normal" state.

    Renders the current players hand face up, the current card selected is
    raised, the most recentl played card on the board face up, and other
    players' hands face down.

    O(m*n) runtime where m is the amount of players to be drawn and
    n is the size of the players hand. Since both of these sizes should be
    relatively small optimizing was considered negligible.
    """
    # clear screen completely
    screen.fill(black)

    # draw personal players hand should only be O(n) as player_you should
    # only be one person. n is the number of cards in player_you's hand
    for player in player_you:
        (player_dat, selected) = player
        redraw_hand_visble(player_dat, selected)  # O(n)
    
    if(board.color=='r'):
        rectcolor=(255,0,0)
    elif(board.color=='g'):
        rectcolor=(0,255,0)
    elif(board.color=="b"):
        rectcolor=(0,0,255)
    elif(board.color=='y'):
        rectcolor=(255,255,0)
    else:
        rectcolor=(255,255,255)

    pygame.draw.rect(screen, blue, pygame.Rect(screen_width//1.4-screen_width//6, screen_height//1.55, screen_width//50, screen_height//30), 4)
    screen.fill(rectcolor, pygame.Rect(screen_width//1.4-screen_width//6 + 1, screen_height//1.55 + 1, screen_width//50 - 2, screen_height//30 - 2))

    # grab a list of all players excluding the currenly playing one
    players_temp = players_other[:]  # O(n)
    players_temp.remove(player_dat)  # O(n)

    # draw all players (excluding the currently playing player) hands facedown
    # an orderly fashion on the screen
    redraw_hand_nonvisble_loop(players_temp)  # O(m*n)

    # draw the top card on the board
    draw_top_stack_card(board)  # O(1)

    # draw stacked deck on the board
    draw_stack_card(board)

    # refreshing the screen
    pygame.display.flip()  # O(1)?


def redraw_screen_menu_color(selected=None):
    """
    Draws a simple color menu with placeholder graphics.

    Function clears the top half of the screen and clears display of nonvisible
    hands while it runs.

    O(1) runtime as the number of colors is 4 thus the for loop only runs
    4 times thus being negligible
    """
    # zero input catch
    if selected is None:
        selected = 0

    # clear screen
    pygame.draw.rect(
        screen, black, (0, 0, screen_width, int(600 * scale_y)), 0)

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - ((300 * 2 + card_width) // 2)

    # placeholders for color slection graphics
    card_g = game_classes.Card("green", "small_cards/green_0.png", None)
    card_b = game_classes.Card("blue", "small_cards/blue_0.png", None)
    card_y = game_classes.Card("yellow", "small_cards/yellow_0.png", None)
    card_r = game_classes.Card("red", "small_cards/red_0.png", None)

    color_array = [card_g, card_b, card_y, card_r]
    color_index = 0
    for card_c in color_array:  # O(4)
        card_c.rect = def_rect
        if color_index == selected:
            card_c.rect = card_c.rect.move(start_pos, 200)
        else:
            card_c.rect = card_c.rect.move(start_pos, 300)

        card_c.rect = card_c.rect.move(200 * color_index, 0)
        scale_card_blit(card_c.card_data, card_c.rect)

        color_index += 1

    # refresh the screen
    pygame.display.flip()


def redraw_screen_menu_target(players, selected=None):
    """
    Draws a simple menu with placeholder graphics (red number cards) that
    refrences a target player to use a card effect on. Thus function clears
    the top half of the screen and clears  display of nonvisible hands while it
    runs.

    O(n) runtime where n is the number of players that can be a proper target
    """

    # zero input catch
    if selected is None:
        selected = 0

    # clear screen (top half)
    pygame.draw.rect(
        screen, black, (0, 0, screen_width, int(600 * scale_y)), 0)

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - \
        (200 * (len(players) - 1) + card_width) // 2

    target_index = 0
    for player in players:  # O(n)
        player_num = str(player.name[7])
        card_disp = game_classes.Card(
            "red", "small_cards/red_" + player_num + ".png", None)
        card_disp.rect = def_rect

        if target_index == selected:
            card_disp.rect = card_disp.rect.move(start_pos, 200)
        else:
            card_disp.rect = card_disp.rect.move(start_pos, 300)

        card_disp.rect = card_disp.rect.move(200 * target_index, 0)
        scale_card_blit(card_disp.card_data, card_disp.rect)

        target_index += 1

    # refresh the screen
    pygame.display.flip()


def draw_winners(winners):
    """
    Function that draws the winners in win placement from left to right.
    Left being the first winner and right being last place.

    O(n) runtime where n is the size of the list winners
    """
    # clear screen (top half)
    screen.fill(black)
    for player in winners:
        if player.name == 'player_1':
            screen.blit(resultwin_button,(screen_width*328.5/1600,screen_height/9))
            display_funct.winplay.play()
            if display_funct.instorymode == True and display_funct.cur_stage == 1:
                display_funct.cleared1 = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 2:
                display_funct.cleared2 = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 3:
                display_funct.cleared3 = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 4:
                display_funct.cleared4 = True
        else:
            screen.blit(resultlose_button,(screen_width*328.5/1600,screen_height/9))
            display_funct.loseplay.play()
        break

    # get a "middle" start postion for bliting cards

    # refresh the screen
    pygame.display.flip()

################################################## ESC 화면 ############################################################
def esc_screen():
    selected_button = "resume"
    while display_funct.option == True:
        game_logic.elapsed_time = (pygame.time.get_ticks() - game_logic.start_ticks) / 1000
        green = (0,0,0)
        display_funct.screen.fill(green)
        display_funct.screen.blit(resume_button,(display_funct.screen_width*3/16,display_funct.screen_height*4/9))
        display_funct.screen.blit(title_button,(display_funct.screen_width*6/16,display_funct.screen_height*4/9))
        display_funct.screen.blit(setting_button,(display_funct.screen_width*9/16,display_funct.screen_height*4/9))
        display_funct.screen.blit(exit_button,(display_funct.screen_width*12/16,display_funct.screen_height*4/9))

        if selected_button == "resume":
            display_funct.screen.blit(resume_on_button,(display_funct.screen_width*3/16,display_funct.screen_height*4/9))
        elif selected_button == "title":
            display_funct.screen.blit(title_on_button,(display_funct.screen_width*6/16,display_funct.screen_height*4/9))
        elif selected_button == "setting":
            display_funct.screen.blit(setting_on_button,(display_funct.screen_width*9/16,display_funct.screen_height*4/9))
        elif selected_button == "exit":
            display_funct.screen.blit(exit_on_button,(display_funct.screen_width*12/16,display_funct.screen_height*4/9))
        
        if display_funct.title == True:
            title_screen()

        elif display_funct.setting == True:
            setting_screen()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if selected_button == "resume":
                        selected_button = "exit"
                    elif selected_button == "title":
                        selected_button = "resume"
                    elif selected_button == "setting":
                        selected_button = "title"
                    elif selected_button == "exit":
                        selected_button = "setting"

                elif event.key == pygame.K_RIGHT:
                    if selected_button == "resume":
                        selected_button = "title"
                    elif selected_button == "title":
                        selected_button = "setting"
                    elif selected_button == "setting":
                        selected_button = "exit"
                    elif selected_button == "exit":
                        selected_button = "resume"

                elif event.key == event.key == pygame.K_UP or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    if selected_button == "resume":
                        display_funct.i = 1
                        display_funct.option = False
                    elif selected_button == "title":
                        display_funct.title = True
                        display_funct.option = False
                        PY_UNO.main()
                        
                    elif selected_button == "setting":
                        display_funct.setting = True

                    elif selected_button == "exit":
                        pygame.display.quit()
                        pygame.quit()
                        exit()
                        

            pygame.display.update()
        
############################################### 옵션 화면 #############################################
def setting_screen():
    selected_option2 = "left"
    selected_option = "sound"
    selected_option3 = "left"
    while display_funct.setting:
        green = (0,0,0)
        screen.fill(green)
        screen.blit(option_1, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))

        screen.blit(optionminus_button,(display_funct.screen_width*887.5/1600,display_funct.screen_height*200/900))
        screen.blit(optionplus_button,(display_funct.screen_width*937.5/1600,display_funct.screen_height*200/900))
        screen.blit(optionminus_button,(display_funct.screen_width*887.5/1600,display_funct.screen_height*245/900))
        screen.blit(optionplus_button,(display_funct.screen_width*937.5/1600,display_funct.screen_height*245/900))
        screen.blit(optionminus_button,(display_funct.screen_width*887.5/1600,display_funct.screen_height*290/900))
        screen.blit(optionplus_button,(display_funct.screen_width*937.5/1600,display_funct.screen_height*290/900))

        screen.blit(small_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*370/900))
        screen.blit(med_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*440/900))
        screen.blit(full_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*510/900))

        screen.blit(reset_button, (display_funct.screen_width*607.5/1600,display_funct.screen_height*670/900))
        screen.blit(keyset_button, (display_funct.screen_width*812.5/1600,display_funct.screen_height*670/900))
        
        screen.blit(check_button, (display_funct.screen_width*775/1600,display_funct.screen_height*750/900))
        

        #사운드
        if selected_option == "sound" and selected_option3 == "left":
            screen.blit(optionminus_on_button, (display_funct.screen_width*887.5/1600,display_funct.screen_height*200/900))
        elif selected_option == "sound" and selected_option3 == "right":
            screen.blit(optionplus_on_button, (display_funct.screen_width*937.5/1600,display_funct.screen_height*200/900))
        elif selected_option == "mainsound" and selected_option3 == "left":
            screen.blit(optionminus_on_button, (display_funct.screen_width*887.5/1600,display_funct.screen_height*245/900))
        elif selected_option == "mainsound" and selected_option3 == "right":
            screen.blit(optionplus_on_button, (display_funct.screen_width*937.5/1600,display_funct.screen_height*245/900))
        elif selected_option == "subsound" and selected_option3 == "left":
            screen.blit(optionminus_on_button, (display_funct.screen_width*887.5/1600,display_funct.screen_height*290/900))
        elif selected_option == "subsound" and selected_option3 == "right":
            screen.blit(optionplus_on_button, (display_funct.screen_width*937.5/1600,display_funct.screen_height*290/900))
        
        #해상도
        if selected_option == "small":
            screen.blit(small_on_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*370/900))
        if selected_option == "med":
            screen.blit(med_on_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*440/900))
        if selected_option == "full":
            screen.blit(full_on_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*510/900))

        #색약모드
        if selected_option == "color" and display_funct.color_option == "on":
            screen.blit(checkon_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        elif selected_option == "color" and display_funct.color_option == "off":
            screen.blit(check_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        elif display_funct.color_option == "on":
            screen.blit(checkon_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        elif display_funct.color_option == "off":
            screen.blit(check_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        #keyset and resst
        if selected_option == 'set' and selected_option2 == "left":
            screen.blit(reset_on_button, (display_funct.screen_width*607.5/1600,display_funct.screen_height*670/900))
            
        elif selected_option == 'set' and selected_option2 == "right":
            screen.blit(keyset_on_button, (display_funct.screen_width*812.5/1600,display_funct.screen_height*670/900))   

        #Close
        if selected_option == "close":
            screen.blit(check_on_button, (display_funct.screen_width*775/1600,display_funct.screen_height*750/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_option == "sound":
                        pass
                    elif selected_option == "mainsound":
                        selected_option = "sound"
                    elif selected_option == "subsound":
                        selected_option = "mainsound"
                    elif selected_option == "small":
                        selected_option = "subsound"
                    elif selected_option == "med":
                        selected_option = "small"
                    elif selected_option == "full":
                        selected_option = "med"
                    elif selected_option == "color":
                        selected_option = "full"
                    elif selected_option == "set":
                        selected_option = "color"
                    elif selected_option == "close":
                        selected_option = "set"
                        
                elif event.key == pygame.K_DOWN:
                    if selected_option == "sound":
                        selected_option = "mainsound"
                    elif selected_option == "mainsound":
                        selected_option = "subsound"
                    elif selected_option == "subsound":
                        selected_option = "small"
                    elif selected_option == "small":
                        selected_option = "med"
                    elif selected_option == "med":
                        selected_option = "full"
                    elif selected_option == "full":
                        selected_option = "color"
                    elif selected_option == "color":
                        selected_option = "set"
                    elif selected_option == "set":
                        selected_option = "close"
                    elif selected_option == "close":
                        pass
                
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    if selected_option == "sound" and selected_option3 == "left":
                        selected_option3 = "right"
                    elif selected_option == "sound" and selected_option3 == "right":
                        selected_option3 = "left"

                    if selected_option == "mainsound" and selected_option3 == "left":
                        selected_option3 = "right"
                    elif selected_option == "mainsound" and selected_option3 == "right":
                        selected_option3 = "left"
                    if selected_option == "subsound" and selected_option3 == "left":
                        selected_option3 = "right"
                    elif selected_option == "subsound" and selected_option3 == "right":
                        selected_option3 = "left"

                    if selected_option == "set" and selected_option2 == "right":
                        selected_option2 = "left"
                    elif selected_option == "set" and selected_option2 == "left":
                        selected_option2 = "right"



                elif event.key == pygame.K_SPACE:
                    if selected_option == "sound" and selected_option3 == "left":
                        if display_funct.sound == 0:
                            pass
                        else:
                            display_funct.sound -= 1
                            pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                            config["sound"] = display_funct.sound

                    if selected_option == "sound" and selected_option3 == "right":
                        if display_funct.sound == 10:
                            pass
                        else:
                            display_funct.sound += 1
                            pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                            config["sound"] = display_funct.sound
                    if selected_option == "mainsound" and selected_option3 == "left":
                        if display_funct.mainsound == 0:
                            pass
                        else:
                            display_funct.mainsound -= 1
                            pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                            config["mainsound"] = display_funct.mainsound

                    if selected_option == "mainsound" and selected_option3 == "right":
                        if display_funct.mainsound == 10:
                            pass
                        else:
                            display_funct.mainsound += 1
                            pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                            config["mainsound"] = display_funct.mainsound

                    if selected_option == "subsound" and selected_option3 == "left":
                        if display_funct.subsound == 0:
                            pass
                        else:
                            display_funct.subsound -= 1
                            setsound()
                            menuplay.play()
                            config["subsound"] = display_funct.subsound

                    if selected_option == "subsound" and selected_option3 == "right":
                        if display_funct.subsound == 10:
                            pass
                        else:
                            display_funct.subsound += 1
                            setsound()
                            menuplay.play()
                            config["subsound"] = display_funct.subsound

                    if selected_option == "small":
                        width = 1280
                        height = 720
                        if display_funct.full == True:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            display_funct.full = False
                            config["screen_width"] = screen_width
                            config["screen_height"] = screen_height
                            config["full"] = False
                            
                        elif width == screen_width and height == screen_height:
                            pass
                        else:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            config["screen_width"] = screen_width
                            config["screen_height"] = screen_height
                            config["full"] = False
                    
                    if selected_option == "med":
                        width = 1600
                        height = 900
                        if display_funct.full == True:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            display_funct.full = False
                            config["screen_width"] = screen_width
                            config["screen_height"] = screen_height
                            config["full"] = False

                        elif width == screen_width and height == screen_height:
                            pass
                        else:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            config["screen_width"] = screen_width
                            config["screen_height"] = screen_height
                            config["full"] = False
                    
                    if selected_option == "full":
                        if display_funct.full == True:
                            pass
                        else:
                            pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
                            display_info = pygame.display.Info()
                            width = display_info.current_w
                            height = display_info.current_h
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            display_funct.full = True
                            config["screen_width"] = screen_width
                            config["screen_height"] = screen_height
                            config["full"] = True

                    if selected_option == "color":
                        if display_funct.color_option == "on":
                            display_funct.color_option = "off"
                            config["color_option"] = "off"
                        elif display_funct.color_option == "off":
                            display_funct.color_option = "on"
                            config["color_option"] = "on"

                    if selected_option == "set" and selected_option2 == "left":
                        display_funct.screen_width, display_funct.screen_height = 1280, 720
                        display_funct.sound_option = "on"
                        display_funct.color_option = "off"
                        display_funct.full = False
                        display_funct.sound = 5
                        display_funct.mainsound = 5
                        display_funct.subsound = 5
                        image_scale()
                        pygame.display.set_mode((screen_width,screen_height))
                        pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                        config["screen_width"] = screen_width
                        config["screen_height"] = screen_height
                        config["sound"] = 5
                        config["mainsound"] = 5
                        config["subsound"] = 5
                        config["color_option"] = "off"
                        config["full"] = False

                    elif selected_option == "close":
                        display_funct.setting = False
                    
                elif event.key == pygame.K_ESCAPE:
                    display_funct.setting = False
    
        with open("config.txt", "w") as f:
            json.dump(config, f)
        pygame.display.flip()



################################################ 키 세팅 ####################################################

def keyset_screen():
    keysetting = True
    current = 1
    while keysetting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


def change_key_screen():
    changing = True
    while changing:
        pass






















################################################# 시작 화면 ################################################
# 게임 루프
def title_screen():
    selected_button = "single"
    while display_funct.title: 
        screen.fill(black)
        # 버튼 생성
        screen.blit(titlesingle_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/3))
        screen.blit(titlestory_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/2))
        screen.blit(titleoption_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.5))
        screen.blit(titleexit_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.2))
        
        # 선택된 버튼
        if selected_button == "single":
            screen.blit(titlesingle_on_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/3))
        elif selected_button == "story":
            screen.blit(titlestory_on_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/2))
        elif selected_button == "option":
            screen.blit(titleoption_on_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.5))
        elif selected_button == "exit":
            screen.blit(titleexit_on_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 위쪽 방향키 클릭 시
                    if selected_button == "single":
                        selected_button = "exit"
                    elif selected_button == "story":
                        selected_button = "single"               
                    elif selected_button == "option":
                        selected_button = "story"
                    elif selected_button == "exit":
                        selected_button = "option"

                elif event.key == pygame.K_DOWN:
                    # 아래쪽 방향키 클릭 시
                    if selected_button == "single":
                        selected_button = "story"
                    elif selected_button == "story":
                        selected_button = "option"
                    elif selected_button == "option":
                        selected_button = "exit"
                    else:
                        selected_button = "single"
                elif event.key == event.key == event.key == pygame.K_SPACE: #우측키 스페이스 엔터
                    if selected_button == "single":
                        display_funct.title = False
                        display_funct.single_screen()
                    
                    elif selected_button == "story":
                        display_funct.title = False
                        display_funct.instorymode = True
                        display_funct.story_screen()

                    elif selected_button == "option":
                        # Options 버튼 클릭 시 실행할 코드
                        
                        display_funct.setting = True
                        display_funct.setting_screen()

                    elif selected_button == "exit":
                        # Quit 버튼 클릭 시 실행할 코드
                        pygame.quit()
                        exit()
                
                '''elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭시
                    if event.button == 1:
                        click_x, click_y = event.pos
                        
                        #Start 버튼
                        if  screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/2 <= click_y <= screen_height/2 + screen_height/12:
                            pass
                            #Option 버튼
                        elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                            screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:  
                            pass
                            
                                
                            #Quit 버튼
                        elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/1.2 <= click_y <= screen_height/1.2 + screen_height/12:
                            pygame.quit()
                            exit()'''

            pygame.display.flip()
################################## 싱글플레이 ################################################
def single_screen():
    selected_button1 = "ai"
    selected_button2 = "minus"
    i=1
    playing = True
    while playing:

        screen.fill(black)
        screen.blit(singleoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(singleplus_button, (display_funct.screen_width*827.5/1600,display_funct.screen_height*627.5/900))
        screen.blit(singleminus_button, (display_funct.screen_width*727.5/1600,display_funct.screen_height*627.5/900))
        screen.blit(singlestart_button, (screen_width*677.5/1600,screen_height*690/900))

        if selected_button1 == "ai" and selected_button2 == "plus":
            screen.blit(singleplus_on_button, (display_funct.screen_width*827.5/1600,display_funct.screen_height*627.5/900))
        elif selected_button1 =="ai" and selected_button2 == "minus":
            screen.blit(singleminus_on_button, (display_funct.screen_width*727.5/1600,display_funct.screen_height*627.5/900))

        elif selected_button1 == "start":
            screen.blit(singlestart_on_button, (screen_width*677.5/1600,screen_height*690/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 위쪽 방향키 클릭 시
                    if selected_button1 == "ai":
                        pass 
                    elif selected_button1 == "start":
                        selected_button1 = "ai"  
                elif event.key == pygame.K_DOWN:
                    if selected_button1 == "ai":
                        selected_button1 = "start"
                    elif selected_button1 == "start":
                        pass
                elif event.key == pygame.K_RIGHT:
                    if selected_button1 == "ai" and selected_button2 == "plus":
                        selected_button2 = "minus"
                    elif selected_button1 == "ai":
                        selected_button2 = "plus"
                    elif selected_button1 == "start":
                        pass
                elif event.key == pygame.K_LEFT:
                    if selected_button1 == "ai" and selected_button2 == "plus":
                        selected_button2 = "minus"
                    elif selected_button1 == "ai":
                        selected_button2 = "plus"
                    elif selected_button1 == "start":
                        pass

                elif event.key == pygame.K_SPACE:
                    if selected_button1 == "ai" and selected_button2 == "plus":
                        if i==5:
                            pass
                        else:
                            i += 1
                    elif selected_button1 == "ai":
                        if i==1:
                            pass
                        else:
                            i-=1
                    
                    elif selected_button1 == "start":
                        playing = False
                elif event.key == pygame.K_ESCAPE:
                    display_funct.title = True
                    PY_UNO.main()

        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*185/900))
        if i > 0:
            screen.blit(singleai1_button, (screen_width*677.5/1600,screen_height*255/900))
            if i> 1:    
                screen.blit(singleai2_button, (screen_width*677.5/1600,screen_height*325/900))
                if i>2:
                    screen.blit(singleai3_button, (screen_width*677.5/1600,screen_height*395/900))
                    if i>3:
                        screen.blit(singleai4_button, (screen_width*677.5/1600,screen_height*465/900))
                        if i>4:
                            screen.blit(singleai5_button, (screen_width*677.5/1600,screen_height*535/900))
        pygame.display.flip()

    board1 = game_classes.Board("board1")  

    # initilizing a deck to be used within the game (3 copies are added to
    # each other)
    deck1 = gen_rand_deck("deck1", 0)

    # defining a 7 player uno game
    player1 = game_classes.Player("player_1")
    player1.grab_cards(deck1, 7)

    playerAI_list = []

    for _ in range(i):
        playerAI = game_AI.make_AI_basic(deck1, "player_"+str(_+2)+"AI", 7)
        playerAI_list.append(playerAI)

    display_funct.redraw_hand_visble(player1, None)
    

    # enters into playing the game
    game_logic.game_loop(board1, deck1, [player1]+ playerAI_list)

#############################################스토리 로비 ##############################################################
def check_screen():
    starting = "yes"
    checking = True
    while checking:
        screen.blit(checkmap_button,(display_funct.screen_width*600/1600,display_funct.screen_height*300/900))
        screen.blit(checkon_button,(display_funct.screen_width*700/1600,display_funct.screen_height*500/900))
        screen.blit(check_button,(display_funct.screen_width*835/1600,display_funct.screen_height*500/900))
        if starting == "yes":
            screen.blit(checkon_on_button,(display_funct.screen_width*700/1600,display_funct.screen_height*500/900))
        elif starting == "no":
            screen.blit(check_on_button,(display_funct.screen_width*835/1600,display_funct.screen_height*500/900))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    if starting == "yes":
                        starting = "no"
                    else:
                        starting = "yes"

                elif event.key == pygame.K_SPACE:
                    if starting == "yes":
                        checking = False
                        display_funct.s_playing = False
                    else:
                        checking = False

        pygame.display.flip()
def story_screen():
    display_funct.s_playing = True
    if display_funct.cleared3 == True or display_funct.cleared4 == True:
        display_funct.cur_stage = 4
    elif display_funct.cleared2 == True:
        display_funct.cur_stage = 3
    elif display_funct.cleared1 == True:
        display_funct.cur_stage = 2
    else:
        display_funct.cur_stage = 1
    while display_funct.s_playing:
        screen.fill(black)
        screen.blit(singlelobby_button,(display_funct.screen_width*207.5/1600, display_funct.screen_height*50/900))   
        screen.blit(notcleared_button, (display_funct.screen_width*392.5/1600,display_funct.screen_height*640/900))
        screen.blit(notcleared_button, (display_funct.screen_width*967.5/1600,display_funct.screen_height*600/900))
        screen.blit(notcleared_button, (display_funct.screen_width*1152.5/1600,display_funct.screen_height*410/900))
        screen.blit(notcleared_button, (display_funct.screen_width*582.5/1600,display_funct.screen_height*230/900))

        if display_funct.cleared1 == True:
            screen.blit(cleared_button, (display_funct.screen_width*392.5/1600,display_funct.screen_height*640/900))
        if display_funct.cleared2 == True:
            screen.blit(cleared_button, (display_funct.screen_width*967.5/1600,display_funct.screen_height*600/900))
        if display_funct.cleared3 == True:
            screen.blit(cleared_button, (display_funct.screen_width*1152.5/1600,display_funct.screen_height*410/900))
        if display_funct.cleared4 == True:
            screen.blit(cleared_button, (display_funct.screen_width*582.5/1600,display_funct.screen_height*230/900))

        if display_funct.cur_stage == 1:
            screen.blit(cur_on_button, (display_funct.screen_width*392.5/1600,display_funct.screen_height*640/900))
            screen.blit(mapabouta_button, (display_funct.screen_width*1120/1600 ,display_funct.screen_height*80/900))
        elif display_funct.cur_stage == 2:
            screen.blit(cur_on_button, (display_funct.screen_width*967.5/1600,display_funct.screen_height*600/900))
            screen.blit(mapaboutb_button, (display_funct.screen_width*1120/1600 ,display_funct.screen_height*80/900))
        elif display_funct.cur_stage == 3:
            screen.blit(cur_on_button, (display_funct.screen_width*1152.5/1600,display_funct.screen_height*410/900))
            screen.blit(mapaboutc_button, (display_funct.screen_width*1120/1600 ,display_funct.screen_height*80/900))
        elif display_funct.cur_stage == 4:
            screen.blit(cur_on_button, (display_funct.screen_width*582.5/1600,display_funct.screen_height*230/900))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if display_funct.cur_stage == 1:
                        if display_funct.cleared1 == True:
                            display_funct.cur_stage = 2
                            menuplay.play()
                        else:
                            menuplay.play()
                    elif display_funct.cur_stage == 2:
                        if display_funct.cleared2 == True:
                            display_funct.cur_stage = 3
                            menuplay.play()
                        else:
                            menuplay.play()

                    elif display_funct.cur_stage == 3:
                        if display_funct.cleared3 == True:
                            display_funct.cur_stage = 4
                            menuplay.play()
                        else:
                            menuplay.play()
                    elif display_funct.cur_stage == 4:
                        menuplay.play()
                        pass
                elif event.key == pygame.K_LEFT:
                    if display_funct.cur_stage == 1:
                        menuplay.play()
                    elif display_funct.cur_stage == 2:
                        display_funct.cur_stage = 1
                        menuplay.play()
                    elif display_funct.cur_stage == 3:
                        display_funct.cur_stage = 2
                        menuplay.play()
                    elif display_funct.cur_stage == 4:
                        display_funct.cur_stage = 3
                        menuplay.play()
                
                elif event.key == pygame.K_SPACE:
                    check_screen()

                elif event.key == pygame.K_ESCAPE:
                    display_funct.s_playing=False
                    display_funct.title = True
                    PY_UNO.main()

        pygame.display.flip()
    ####################### 스테이지 시작##################

    if display_funct.title:
        pass

    else:
        if cur_stage == 1:
            board1 = game_classes.Board("board1") 

            deck1 = gen_rand_deck("deck1", 1)

            player1 = game_classes.Player("player_1")
            setting = game_story_setting.setting_A(deck1, player1)

            display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, setting)     


        elif cur_stage == 2:
            board1 = game_classes.Board("board1") 

            deck1 = gen_rand_deck("deck1", 1)

            player1 = game_classes.Player("player_1")
            setting = game_story_setting.setting_B(deck1, player1)

            display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, setting)

        elif cur_stage == 3:
            board1 = game_classes.Board("board1")  

            # initilizing a deck to be used within the game (3 copies are added to
            # each other)
            deck1 = gen_rand_deck("deck1", 0)

            # defining a 7 player uno game
            player1 = game_classes.Player("player_1")
            player1.grab_cards(deck1, 7)

            player_2AI = game_AI.make_AI_basic(deck1, "player_2AI",7)
            player_3AI = game_AI.make_AI_basic(deck1, "player_2AI",7)

            display_funct.redraw_hand_visble(player1, None)
            

            # enters into playing the game
            game_logic.game_loop_C(board1, deck1, [player1, player_2AI,player_3AI])
            
        # 스테이지 4수정
        elif cur_stage == 4:
            board1 = game_classes.Board("board1")
            deck1 = gen_rand_deck("deck_d", 0)
            player1 = game_classes.Player("player_1")
            player1.grab_cards(deck1, 7)
            player2AI = game_AI.make_AI_basic(deck1, "player_2AI", 7)
            display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, [player1, player2AI])

    






















################################### 이미지 파일 ###############################################
#타이틀
titlestart_image = pygame.image.load("image/titlestart.png")
titleoption_image = pygame.image.load("image/titleoption.png")
titleexit_image = pygame.image.load("image/titleexit.png")
titlesingle_image = pygame.image.load("image/titlesingle.png")
titlestory_image = pygame.image.load("image/titlestory.png")

#타이틀_ON
titlestart_on_image = pygame.image.load("image/titlestart_on.png")
titleoption_on_image = pygame.image.load("image/titleoption_on.png")
titleexit_on_image = pygame.image.load("image/titleexit_on.png")
titlesingle_on_image = pygame.image.load("image/titlesingle_on.png")
titlestory_on_image = pygame.image.load("image/titlestory_on.png")

#ESC
setting_image = pygame.image.load("image/setting.png")
title_image = pygame.image.load("image/title.png")
resume_image = pygame.image.load("image/resume.png")
exit_image = pygame.image.load("image/exit.png")

#ESC_ON
resume_on_image = pygame.image.load("image/resume_on.png")
title_on_image = pygame.image.load("image/title_on.png")
setting_on_image = pygame.image.load("image/setting_on.png")
exit_on_image = pygame.image.load("image/exit_on.png")

#옵션
option_image = pygame.image.load("image/option.png")
small_image = pygame.image.load("image/small.png")
med_image = pygame.image.load("image/med.png")
full_image = pygame.image.load("image/full.png")
check_image = pygame.image.load("image/check.png")
checkon_image = pygame.image.load("image/checkon.png")
optionplus_image = pygame.image.load("image/optionplus.png")
optionplus_on_image = pygame.image.load("image/optionplus_on.png")
optionminus_image = pygame.image.load("image/optionminus.png")
optionminus_on_image = pygame.image.load("image/optionminus_on.png")
reset_image = pygame.image.load("image/reset.png")
keyset_image = pygame.image.load("image/keyset.png")
keysetoption_image = pygame.image.load("image/keysetoption.png")

#옵션_ON
full_on_image = pygame.image.load("image/full_on.png")
check_on_image = pygame.image.load("image/check_on.png")
checkon_on_image = pygame.image.load("image/checkon_on.png")
small_on_image = pygame.image.load("image/small_on.png")
med_on_image = pygame.image.load("image/med_on.png")
reset_on_image = pygame.image.load("image/reset_on.png")
keyset_on_image = pygame.image.load("image/keyset_on.png")

#결과창
resultwin_image = pygame.image.load("image/winner.png")
resultlose_image = pygame.image.load("image/lose.png")

#싱글플레이
singleoption_image = pygame.image.load("image/singleoption.png")
singleplayer_image = pygame.image.load("image/player.png")
singleai1_image = pygame.image.load("image/ai1.png")
singleai2_image = pygame.image.load("image/ai2.png")
singleai3_image = pygame.image.load("image/ai3.png")
singleai4_image = pygame.image.load("image/ai4.png")
singleai5_image = pygame.image.load("image/ai5.png")
singleplus_image = pygame.image.load("image/plus.png")
singleplus_on_image = pygame.image.load("image/plus_on.png")
singleminus_image = pygame.image.load("image/minus.png")
singleminus_on_image = pygame.image.load("image/minus_on.png")

#싱글로비
singlelobby_image = pygame.image.load("image/singlelobby.png")
mapabouta_image = pygame.image.load("image/mapabouta.png")
mapaboutb_image = pygame.image.load("image/mapaboutb.png")
mapaboutc_image = pygame.image.load("image/mapaboutc.png")
cur_image = pygame.image.load("image/cur.png")
cur_on_image = pygame.image.load("image/cur_on.png")
cleared_image = pygame.image.load("image/cleared.png")
notcleared_image = pygame.image.load("image/notcleared.png")
checkmap_image = pygame.image.load("image/mapabout.png")

#해상도 파일
#타이틀
titlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleoption_button = pygame.transform.scale(titleoption_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleexit_button = pygame.transform.scale(titleexit_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlesingle_button = pygame.transform.scale(titlesingle_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlestory_button = pygame.transform.scale(titlestory_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

#타이틀_ON
titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlesingle_on_button = pygame.transform.scale(titlesingle_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlestory_on_button = pygame.transform.scale(titlestory_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))


#ESC
setting_button = pygame.transform.scale(setting_image, (display_funct.screen_width/16,display_funct.screen_height/9))
title_button = pygame.transform.scale(title_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
resume_button = pygame.transform.scale(resume_image, (display_funct.screen_width/16,display_funct.screen_height/9))
exit_button = pygame.transform.scale(exit_image, (display_funct.screen_width/16,display_funct.screen_height/9))

#ESC_ON
resume_on_button = pygame.transform.scale(resume_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
title_on_button = pygame.transform.scale(title_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
setting_on_button = pygame.transform.scale(setting_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
exit_on_button = pygame.transform.scale(exit_on_image, (display_funct.screen_width/16,display_funct.screen_height/9))

#옵션
option_1 = pygame.transform.scale(option_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
small_button = pygame.transform.scale(small_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
med_button = pygame.transform.scale(med_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
full_button = pygame.transform.scale(full_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
check_button = pygame.transform.scale(check_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
checkon_button = pygame.transform.scale(checkon_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
optionplus_button = pygame.transform.scale(optionplus_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
optionminus_button = pygame.transform.scale(optionminus_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
reset_button = pygame.transform.scale(reset_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
keyset_button = pygame.transform.scale(keyset_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
keysetoption_button = pygame.transform.scale(keysetoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))



#옵션_ON
full_on_button = pygame.transform.scale(full_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
check_on_button = pygame.transform.scale(check_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
checkon_on_button = pygame.transform.scale(checkon_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
small_on_button = pygame.transform.scale(small_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
med_on_button = pygame.transform.scale(med_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
optionplus_on_button = pygame.transform.scale(optionplus_on_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
optionminus_on_button = pygame.transform.scale(optionminus_on_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
reset_on_button = pygame.transform.scale(reset_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
keyset_on_button = pygame.transform.scale(keyset_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))

#결과창
resultwin_button = pygame.transform.scale(resultwin_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))
resultlose_button = pygame.transform.scale(resultlose_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))

#싱글플레이
singleoption_button = pygame.transform.scale(singleoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
singleplayer_button = pygame.transform.scale(singleplayer_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleai1_button = pygame.transform.scale(singleai1_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleai2_button = pygame.transform.scale(singleai2_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleai3_button = pygame.transform.scale(singleai3_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleai4_button = pygame.transform.scale(singleai4_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleai5_button = pygame.transform.scale(singleai5_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleplus_button = pygame.transform.scale(singleplus_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
singleplus_on_button = pygame.transform.scale(singleplus_on_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
singleminus_button = pygame.transform.scale(singleminus_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
singleminus_on_button = pygame.transform.scale(singleminus_on_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
singlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))

#스토리로비
singlelobby_button = pygame.transform.scale(singlelobby_image, (display_funct.screen_width*1185/1600,display_funct.screen_height*800/900))
mapabouta_button = pygame.transform.scale(mapabouta_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
mapaboutb_button = pygame.transform.scale(mapaboutb_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
mapaboutc_button = pygame.transform.scale(mapaboutc_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
cur_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
cur_on_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
cleared_button = pygame.transform.scale(cleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
notcleared_button = pygame.transform.scale(notcleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
checkmap_button = pygame.transform.scale(checkmap_image, (display_funct.screen_width*400/1600,display_funct.screen_height*300/900))

def image_scale():
    #타이틀
    display_funct.titlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_button = pygame.transform.scale(titleoption_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_button = pygame.transform.scale(titleexit_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlesingle_button = pygame.transform.scale(titlesingle_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlestory_button = pygame.transform.scale(titlestory_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

    #타이틀_ON
    display_funct.titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlesingle_on_button = pygame.transform.scale(titlesingle_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlestory_on_button = pygame.transform.scale(titlestory_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    
    #ESC
    display_funct.setting_button = pygame.transform.scale(setting_image, (display_funct.screen_width/16,display_funct.screen_height/9))
    display_funct.title_button = pygame.transform.scale(title_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
    display_funct.resume_button = pygame.transform.scale(resume_image, (display_funct.screen_width/16,display_funct.screen_height/9))
    display_funct.exit_button = pygame.transform.scale(exit_image, (display_funct.screen_width/16,display_funct.screen_height/9))
    
    
    #ESC_ON
    display_funct.resume_on_button = pygame.transform.scale(resume_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
    display_funct.title_on_button = pygame.transform.scale(title_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
    display_funct.setting_on_button = pygame.transform.scale(setting_on_image, (display_funct.screen_width/16,display_funct.screen_height/9)) 
    display_funct.exit_on_button = pygame.transform.scale(exit_on_image, (display_funct.screen_width/16,display_funct.screen_height/9))


    #옵션
    display_funct.option_1 = pygame.transform.scale(option_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
    display_funct.small_button = pygame.transform.scale(small_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.med_button = pygame.transform.scale(med_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.full_button = pygame.transform.scale(full_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.check_button = pygame.transform.scale(check_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.checkon_button = pygame.transform.scale(checkon_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.optionplus_button = pygame.transform.scale(optionplus_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
    display_funct.optionminus_button = pygame.transform.scale(optionminus_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))      
    display_funct.reset_button = pygame.transform.scale(reset_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.keyset_button = pygame.transform.scale(keyset_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))

    #옵션_ON
    display_funct.full_on_button = pygame.transform.scale(full_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.check_on_button = pygame.transform.scale(check_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.checkon_on_button = pygame.transform.scale(checkon_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.small_on_button = pygame.transform.scale(small_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.med_on_button = pygame.transform.scale(med_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.optionplus_on_button = pygame.transform.scale(optionplus_on_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
    display_funct.optionminus_on_button = pygame.transform.scale(optionminus_on_image, (display_funct.screen_width*50/1600,display_funct.screen_height*38/900))
    display_funct.reset_on_button = pygame.transform.scale(reset_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.keyset_on_button = pygame.transform.scale(keyset_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))

    #결과창
    display_funct.resultwin_button = pygame.transform.scale(resultwin_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))
    display_funct.resultlose_button = pygame.transform.scale(resultlose_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))

    #싱글플레이
    display_funct.singleoption_button = pygame.transform.scale(singleoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
    display_funct.singleplayer_button = pygame.transform.scale(singleplayer_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleai1_button = pygame.transform.scale(singleai1_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleai2_button = pygame.transform.scale(singleai2_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleai3_button = pygame.transform.scale(singleai3_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleai4_button = pygame.transform.scale(singleai4_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleai5_button = pygame.transform.scale(singleai5_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleplus_button = pygame.transform.scale(singleplus_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
    display_funct.singleplus_on_button = pygame.transform.scale(singleplus_on_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
    display_funct.singleminus_button = pygame.transform.scale(singleminus_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
    display_funct.singleminus_on_button = pygame.transform.scale(singleminus_on_image, (display_funct.screen_width*53/1600,display_funct.screen_height*40/900))
    display_funct.singlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singlelobby_button = pygame.transform.scale(singlelobby_image, (display_funct.screen_width*1185/1600,display_funct.screen_height*800/900))

    #스토리로비
    display_funct.singlelobby_button = pygame.transform.scale(singlelobby_image, (display_funct.screen_width*1185/1600,display_funct.screen_height*800/900))
    display_funct.mapabouta_button = pygame.transform.scale(mapabouta_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
    display_funct.mapaboutb_button = pygame.transform.scale(mapaboutb_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
    display_funct.mapaboutc_button = pygame.transform.scale(mapaboutc_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
    display_funct.cur_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.cur_on_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.cleared_button = pygame.transform.scale(cleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.notcleared_button = pygame.transform.scale(checkmap_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))

#######################################사운드#############################################
pygame.mixer.music.load("sound/background.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(mainsound*sound/100)

cardplay = pygame.mixer.Sound(os.getcwd()+"/sound/card.mp3")
menuplay = pygame.mixer.Sound(os.getcwd()+"/sound/menu.wav")
winplay = pygame.mixer.Sound(os.getcwd()+"/sound/win.wav")
loseplay = pygame.mixer.Sound(os.getcwd()+"/sound/lose.wav")
drawplay = pygame.mixer.Sound(os.getcwd()+"/sound/from_deck.wav")


menuplay.set_volume(subsound*sound/100)
cardplay.set_volume(subsound*sound/100)
winplay.set_volume(subsound*sound/100)
loseplay.set_volume(subsound*sound/100)
drawplay.set_volume(subsound*sound/100)

def setsound():
    cardplay.set_volume(display_funct.subsound*display_funct.sound/100)
    menuplay.set_volume(display_funct.subsound*display_funct.sound/100)
    winplay.set_volume(display_funct.subsound*display_funct.sound/100)
    loseplay.set_volume(display_funct.subsound*display_funct.sound/100)
    loseplay.set_volume(display_funct.subsound*display_funct.sound/100)