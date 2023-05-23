import game_classes
import pygame
from pygame.locals import *
import display_funct
import json
import game_logic
import PY_UNO
from deck_gen import gen_rand_deck
from deck_gen import generate_test_A
import deck_gen
import game_AI
import game_classes
import os
import game_story_setting
from datetime import datetime
import socket
import pickle
import threading
from sys import exit

pygame.init()

client_socket = ''
#Default 설정
player_total = 0
screen_width, screen_height = 1600, 900
option = False
setting = False
achieve_title = False
title = True
sound = 5
mainsound = 5
subsound = 5
color_option = "off"
i = 0
full = False # 해상도
s_playing = True # 스토리로비
instorymode = True #스토리모드 확인
cur_stage = 0 # 현재 스테이지
cleared1 = False
cleared2 = False
cleared3 = False
cleared4 = False

up = 1073741906
down = 1073741905
right = 1073741903
left =  1073741904
space = 32
esc = 27
current = 1 #키바꾸기
turn_turn = '1'

stack = 0
#불러오기

wildplayed = False

#업적 ing
first_victory = False
fair_sa = False
#cleared1, cleared2, cleared3, cleared4
turn10 = False
fair = 0
first_defeat = False
stroke5 = 0
cont3 = 0
cont3_true = False
unoother_played = False
unoother_what = False

#업적 달성
first_victory_achieve_check = 0
a_victory_achieve_check = 0
b_victory_achieve_check = 0
c_victory_achieve_check = 0
d_victory_achieve_check = 0
turn10_check = 0
fair_check = 0
unoother_check = 0
first_defeat_check =0
stroke5_check = 0
cont3_check = 0

#업적 날짜
first_victory_date = 0
a_victory_date = 0
b_victory_date = 0
c_victory_date = 0
d_victory_date = 0
turn10_date = 0
fair_date = 0
unoother_date = 0
first_defeat_date = 0
stroke5_date = 0
cont3_date = 0

try:
    with open("achievement.txt", "r") as fa:
        config_ach = json.load(fa)
    #업적 달성
    first_victory_achieve_check = config_ach["first_check"]
    a_victory_achieve_check = config_ach["a_check"]
    b_victory_achieve_check = config_ach["b_check"]
    c_victory_achieve_check = config_ach["c_check"]
    d_victory_achieve_check = config_ach["d_check"]
    turn10_check = config_ach["turn10_check"]
    fair_check = config_ach["fair_check"]
    unoother_check = config_ach["unoother_check"]
    first_defeat_check = config_ach["first_defeat_check"]
    stroke5_check = config_ach["stroke5_check"]
    cont3_check = config_ach["cont3_check"]

    #업적 날짜
    first_victory_date = config_ach["first_victory_date"]
    a_victory_date = config_ach["a_victory_date"]
    b_victory_date = config_ach["b_victory_date"]
    c_victory_date = config_ach["c_victory_date"]
    d_victory_date = config_ach["d_victory_date"]
    turn10_date = config_ach["turn10_date"]
    fair_date = config_ach["fair_date"]
    unoother_date = config_ach["unoother_date"]
    first_defeat_date = config_ach["first_defeat_date"]
    stroke5_date = config_ach["stroke5_date"]
    cont3_date = config_ach["cont3_date"]
    
except:
    print("achieve passed")
    pass

try:
    with open("config.txt", "r") as f:
        config = json.load(f)
    screen_width = config["screen_width"]
    screen_height = config["screen_height"]
    sound = config["sound"]
    mainsound = config["mainsound"]
    subsound = config["subsound"]
    color_option = config["color_option"]
    full = config["full"]
    cleared1 = config["cleared1"]
    cleared2 = config["cleared2"]
    cleared3 = config["cleared3"]
    cleared4 = config["cleared4"]
    up = config["up"]
    down = config["down"]
    right = config["right"]
    left = config["left"]
    space = config["space"]
    esc = config["esc"]
except:
    print("option passed")
    pass

if color_option == "on":
    deck_gen.col = 1
else:
    deck_gen.col = 0


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
    if board.turn_iterator==1:
        display_funct.screen.blit(turn_right_button,(display_funct.screen_width*1/100,display_funct.screen_height*5/7))
    elif board.turn_iterator==-1:
        display_funct.screen.blit(turn_left_button,(display_funct.screen_width*1/100,display_funct.screen_height*5/7))

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
    
    # 노란색 순서 표시 추가
    if turn_turn == player.name:
        card_disp = game_classes.Card(
            "red", "small_cards/yellow_" + player_num + ".png", None)
    else:
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
    
    # 노란색 순서 표시 추가
    if turn_turn == player.name:
        card_disp = game_classes.Card(
            "red", "small_cards/yellow_" + player_num + ".png", None)
    else:
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

    # placeholders for color slection graphics 색약모드 추가 4/17
    if deck_gen.col == 1:
        card_g = game_classes.Card("green", "small_cards_color/green_0.png", None)
        card_b = game_classes.Card("blue", "small_cards_color/blue_0.png", None)
        card_y = game_classes.Card("yellow", "small_cards_color/yellow_0.png", None)
        card_r = game_classes.Card("red", "small_cards_color/red_0.png", None)
    else:
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


def draw_winners(winners, turn_tot):
    """
    Function that draws the winners in win placement from left to right.
    Left being the first winner and right being last place.
 
    O(n) runtime where n is the size of the list winners
    """
    # clear screen (top half)
    title_font = pygame.font.SysFont('malgungothic', 50)
    screen.fill(black)
    for player in winners:
        if player.name == 'player_1' or player.name == 'player_1Host':
            screen.blit(resultwin_button,(screen_width*328.5/1600,screen_height/9))
            display_funct.winplay.play()
            if display_funct.instorymode == True and display_funct.cur_stage == 1:
                display_funct.fair = 0
                display_funct.cleared1 = True
                config["cleared1"] = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 2:
                display_funct.fair = 0
                display_funct.cleared2 = True
                config["cleared2"] = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 3:
                display_funct.fair = 0
                display_funct.cleared3 = True
                config["cleared3"] = True
            elif display_funct.instorymode == True and display_funct.cur_stage == 4:
                display_funct.fair = 0
                display_funct.cleared4 = True
                config["cleared4"] = True

            if display_funct.instorymode == False:
                if display_funct.fair == 0:
                    display_funct.fair_sa = True
                
                if display_funct.unoother_played == True:
                    display_funct.unoother_what = True
                

                display_funct.first_victory = True
                display_funct.stroke5 += 1
                
                if turn_tot/display_funct.player_total <= 10:
                    display_funct.turn10 = True

            with open("config.txt", "w") as f:
                json.dump(config, f)

        else:
            display_funct.unoother_played = True
            display_funct.fair = 0
            display_funct.stroke5 = 0
            display_funct.first_defeat = True
            display_funct.cont3_true = False
            whose_winner = title_font.render(winners[0].name+' Win!', True, (0, 0, 0))
            screen.blit(resultlose_button,(screen_width*328.5/1600,screen_height/9))
            screen.blit(whose_winner,(screen_width*580/1600,screen_height*500/900))
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
        screen.blit(titleachieve_button,(display_funct.screen_width*10/1600, display_funct.screen_height*800/900))

        if selected_button == "resume":
            display_funct.screen.blit(resume_on_button,(display_funct.screen_width*3/16,display_funct.screen_height*4/9))
        elif selected_button == "title":
            display_funct.screen.blit(title_on_button,(display_funct.screen_width*6/16,display_funct.screen_height*4/9))
        elif selected_button == "setting":
            display_funct.screen.blit(setting_on_button,(display_funct.screen_width*9/16,display_funct.screen_height*4/9))
        elif selected_button == "exit":
            display_funct.screen.blit(exit_on_button,(display_funct.screen_width*12/16,display_funct.screen_height*4/9))
        elif selected_button == 'achieve':
            screen.blit(titleachieve_on_button,(display_funct.screen_width*10/1600, display_funct.screen_height*800/900))

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
                if event.key == display_funct.left:
                    menuplay.play()
                    if selected_button == "resume":
                        selected_button = "exit"
                    elif selected_button == "title":
                        selected_button = "resume"
                    elif selected_button == "setting":
                        selected_button = "title"
                    elif selected_button == "exit":
                        selected_button = "setting"

                elif event.key == display_funct.right:
                    menuplay.play()
                    if selected_button == "resume":
                        selected_button = "title"
                    elif selected_button == "title":
                        selected_button = "setting"
                    elif selected_button == "setting":
                        selected_button = "exit"
                    elif selected_button == "exit":
                        selected_button = "resume"

                elif event.key == display_funct.down:
                    menuplay.play()
                    if selected_button == 'achieve':
                        pass
                    else:
                        temp = selected_button
                        selected_button = 'achieve'
                        
                
                elif event.key == display_funct.up:
                    menuplay.play()
                    if selected_button == 'achieve':
                        selected_button = temp

                elif event.key == display_funct.space:
                    menuplay.play()
                    if selected_button == "resume":
                        display_funct.i = 1
                        display_funct.option = False
                    elif selected_button == "title":
                        display_funct.title = True
                        display_funct.option = False
                        if display_funct.instorymode == False:
                            display_funct.stroke5 = 0
                        PY_UNO.main()
                        
                    elif selected_button == "setting":
                        display_funct.setting = True

                    elif selected_button == "exit":
                        pygame.display.quit()
                        pygame.quit()
                        exit()
                    elif selected_button == 'achieve':
                        display_funct.achieve_title = True
                        display_funct.achieve_screen()

        pygame.display.flip()
        
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
            deck_gen.col=0
            screen.blit(checkon_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        elif selected_option == "color" and display_funct.color_option == "off":
            deck_gen.col=0
            screen.blit(check_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
        elif display_funct.color_option == "on":
            screen.blit(checkon_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*590/900))
            deck_gen.col=1
            
        elif display_funct.color_option == "off":
            deck_gen.col=0
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
                if event.key == display_funct.up:
                    menuplay.play()
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
                        
                elif event.key == display_funct.down:
                    menuplay.play()
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
                
                elif event.key == display_funct.right or event.key == display_funct.left:
                    menuplay.play()
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



                elif event.key == display_funct.space:
                    menuplay.play()
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
                            deck_gen.col=0
                            display_funct.color_option = "off"
                            config["color_option"] = "off"
                            with open("config.txt", "w") as f:
                                json.dump(config, f)
                            PY_UNO.main()
                        elif display_funct.color_option == "off":
                            deck_gen.col=1
                            display_funct.color_option = "on"
                            config["color_option"] = "on"
                            with open("config.txt", "w") as f:
                                json.dump(config, f)
                            PY_UNO.main()

                    if selected_option == "set" and selected_option2 == "left":
                        display_funct.screen_width, display_funct.screen_height = 1280, 720
                        display_funct.sound_option = "on"
                        display_funct.color_option = "off"
                        display_funct.full = False
                        display_funct.sound = 5
                        display_funct.mainsound = 5
                        display_funct.subsound = 5
                        display_funct.up = 1073741906
                        display_funct.down = 1073741905
                        display_funct.right = 1073741903
                        display_funct.left =  1073741904
                        display_funct.space = 32
                        display_funct.esc = 27

                        image_scale()
                        pygame.display.set_mode((screen_width,screen_height))
                        pygame.mixer.music.set_volume(display_funct.mainsound*display_funct.sound/100)
                        setsound()
                        config["screen_width"] = screen_width
                        config["screen_height"] = screen_height
                        config["sound"] = 5
                        config["mainsound"] = 5
                        config["subsound"] = 5
                        config["color_option"] = "off"
                        config["full"] = False
                        config["up"] = 1073741906
                        config["down"] = 1073741905
                        config["right"] = 1073741903
                        config["left"] =  1073741904
                        config["space"] = 32
                        config["esc"] = 27
                    
                    elif selected_option == "set" and selected_option2 =="right":
                        keyset_screen()

                    elif selected_option == "close":
                        display_funct.setting = False
                        PY_UNO.main()
                    
                elif event.key == display_funct.esc:
                    menuplay.play()
                    display_funct.setting = False
                    PY_UNO.main()
    
            with open("config.txt", "w") as f:
                json.dump(config, f)
        display_funct.achieve_screen()
        pygame.display.flip()



################################################ 키 세팅 ####################################################

def keyset_screen():
    keysetting = True
    display_funct.current = 1
    key_font = pygame.font.SysFont('malgungothic', 20)
    while keysetting:
        screen.fill(black)
        screen.blit(keysetoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*175/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*275/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*375/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*475/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*575/900))
        screen.blit(check_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*675/900))

        if display_funct.current == 1:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*175/900))
        elif display_funct.current == 2:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*275/900))
        elif display_funct.current == 3:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*375/900))
        elif display_funct.current == 4:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*475/900))
        elif display_funct.current == 5:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*575/900))
        elif display_funct.current == 6:
            screen.blit(check_on_button, (display_funct.screen_width*882.5/1600,display_funct.screen_height*675/900))

        key = key_font.render(pygame.key.name(display_funct.up), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*175/900))
        key = key_font.render(pygame.key.name(display_funct.down), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*275/900))
        key = key_font.render(pygame.key.name(display_funct.right), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*375/900))
        key = key_font.render(pygame.key.name(display_funct.left), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*475/900))
        key = key_font.render(pygame.key.name(display_funct.space), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*575/900))
        key = key_font.render(pygame.key.name(display_funct.esc), True, (255, 255, 255))
        screen.blit(key, (display_funct.screen_width*782.5/1600,display_funct.screen_height*675/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.down:
                    menuplay.play()
                    if display_funct.current == 1:
                        display_funct.current = 2
                    elif display_funct.current == 2:  
                        display_funct.current = 3
                    elif display_funct.current == 3:
                        display_funct.current = 4
                    elif display_funct.current == 4:  
                        display_funct.current = 5
                    elif display_funct.current == 5:  
                        display_funct.current = 6
                elif event.key == display_funct.up:
                    menuplay.play()
                    if display_funct.current == 2:
                        display_funct.current = 1
                    elif display_funct.current == 3:  
                        display_funct.current = 2
                    elif display_funct.current == 4:
                        display_funct.current = 3
                    elif display_funct.current == 5:  
                        display_funct.current = 4
                    elif display_funct.current == 6:  
                        display_funct.current = 5
                
                elif event.key == display_funct.space:
                    menuplay.play()
                    if display_funct.current == 1: #윗키
                        change_key_screen()
                    elif display_funct.current == 2: #아래
                        change_key_screen()
                    elif display_funct.current == 3: #오른쪽
                        change_key_screen()
                    elif display_funct.current == 4:  #왼쪽
                        change_key_screen()
                    elif display_funct.current == 5:  #스페이스
                        change_key_screen()
                    elif display_funct.current == 6:  #ESC
                        change_key_screen()

                elif event.key == display_funct.esc:
                    menuplay.play()
                    keysetting = False
        display_funct.achieve_screen()
        pygame.display.flip()

def change_key_screen():
    changing = True
    keys = [display_funct.up,display_funct.down,display_funct.right,display_funct.left,display_funct.space,display_funct.esc]
    while changing:
        screen.blit(keysetting_button, (display_funct.screen_width*600/1600,display_funct.screen_height*300/900))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in keys:
                    pass
                else:
                    if display_funct.current == 1:
                        display_funct.up = event.key
                        config["up"] = display_funct.up
                        changing = False
                    elif display_funct.current == 2:
                        display_funct.down = event.key
                        config["down"] = display_funct.down
                        changing = False
                    elif display_funct.current == 3:
                        display_funct.right = event.key
                        config["right"] = display_funct.right
                        changing = False
                    elif display_funct.current == 4:
                        display_funct.left = event.key
                        config["left"] = display_funct.left
                        changing = False
                    elif display_funct.current == 5:
                        display_funct.space = event.key
                        config["space"] = display_funct.space
                        changing = False
                    elif display_funct.current == 6:
                        display_funct.esc = event.key
                        config["esc"] = display_funct.esc
                        changing = False
            with open("config.txt", "w") as f:
                json.dump(config, f)
        pygame.display.flip()

##################################################업적 화면#####################################################
def achieve_screen():
    title_font = pygame.font.SysFont('malgungothic', 20)
    text_font = pygame.font.SysFont('malgungothic', 14)
    page_font = pygame.font.SysFont('malgungothic', 30)
    page = 1
    selected_button = 'next'
    while display_funct.achieve_title:
        green = (0,0,0)
        screen.fill(green)
        screen.blit(achieveoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))

        if page == 1:
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*90/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*220/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*350/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*480/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*610/900))
            screen.blit(card_icon_button2, (display_funct.screen_width*615.25/1600,display_funct.screen_height*105/900))
            screen.blit(card_icon_button2, (display_funct.screen_width*615.25/1600,display_funct.screen_height*235/900))
            screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*365/900))
            screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*495/900))
            screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))

        elif page == 2:
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*90/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*220/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*350/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*480/900))
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*610/900))
            screen.blit(card_icon_button3, (display_funct.screen_width*615.25/1600,display_funct.screen_height*105/900))
            screen.blit(card_icon_button6, (display_funct.screen_width*615.25/1600,display_funct.screen_height*235/900))
            screen.blit(card_icon_button5, (display_funct.screen_width*615.25/1600,display_funct.screen_height*365/900))
            screen.blit(card_icon_button4, (display_funct.screen_width*615.25/1600,display_funct.screen_height*495/900))
            screen.blit(card_icon_button7, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))

        elif page == 3:
            screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*90/900))
            screen.blit(card_icon_button8, (display_funct.screen_width*615.25/1600,display_funct.screen_height*105/900))

        if page == 1:
            screen.blit(check_button, ((display_funct.screen_width*850/1600,display_funct.screen_height*750/900)))
        elif page == 2:
            screen.blit(check_button, ((display_funct.screen_width*850/1600,display_funct.screen_height*750/900)))
            screen.blit(check_button, ((display_funct.screen_width*685/1600,display_funct.screen_height*750/900)))
        elif page == 3:
            screen.blit(check_button, ((display_funct.screen_width*685/1600,display_funct.screen_height*750/900)))

        if selected_button == 'next':
            screen.blit(check_on_button, ((display_funct.screen_width*850/1600,display_funct.screen_height*750/900)))
        elif selected_button == 'back':
            screen.blit(check_on_button, ((display_funct.screen_width*685/1600,display_funct.screen_height*750/900)))
        

        ######### 페이지 1 업적
        if page == 1:
            achieve_card = title_font.render('첫 승리', True, (0, 0, 0))
            achieve_card_text = text_font.render('-싱글 플레이 승리', True, (0, 0, 0))
            achieve_card_date = text_font.render(str(first_victory_date), True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*105/900))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*135/900))
            if first_victory_date != 0:
                screen.blit(achieve_card_date, (display_funct.screen_width*720/1600, display_funct.screen_height*160/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*95/900))

            achieve_card = title_font.render('입문자', True, (0, 0, 0))
            achieve_card_text = text_font.render('-A 지역 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*235/900))
            a_date = text_font.render(str(a_victory_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*265/900))
            if a_victory_date != 0:
                screen.blit(a_date, (display_funct.screen_width*720/1600, display_funct.screen_height*290/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*225/900))

            achieve_card = title_font.render('초보자', True, (0, 0, 0))
            achieve_card_text = text_font.render('-B 지역 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*365/900))
            b_date = text_font.render(str(a_victory_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*395/900))
            if b_victory_date != 0:
                screen.blit(b_date, (display_funct.screen_width*720/1600, display_funct.screen_height*420/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*355/900))

            achieve_card = title_font.render('중급자', True, (0, 0, 0))
            achieve_card_text = text_font.render('-C 지역 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*495/900))
            c_date = text_font.render(str(a_victory_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*525/900))
            if c_victory_date != 0:
                screen.blit(c_date, (display_funct.screen_width*720/1600, display_funct.screen_height*550/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*485/900))

            achieve_card = title_font.render('상급자', True, (0, 0, 0))
            achieve_card_text = text_font.render('-D 지역 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
            d_date = text_font.render(str(a_victory_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
            if d_victory_date != 0:
                screen.blit(d_date, (display_funct.screen_width*720/1600, display_funct.screen_height*680/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*615/900))

        elif page == 2:
            achieve_card = title_font.render('전력질주', True, (0, 0, 0))
            achieve_card_text = text_font.render('-싱글 플레이 10턴 안에 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*105/900))
            achieve_card_date = text_font.render(str(turn10_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*135/900))
            if turn10_date != 0:
                screen.blit(achieve_card_date, (display_funct.screen_width*720/1600, display_funct.screen_height*160/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*95/900))

            achieve_card = title_font.render('페어 플레이', True, (0, 0, 0))
            achieve_card_text = text_font.render('-기술카드 없이 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*235/900))
            a_date = text_font.render(str(fair_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*265/900))
            if fair_date != 0:
                screen.blit(a_date, (display_funct.screen_width*720/1600, display_funct.screen_height*290/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*225/900))

            achieve_card = title_font.render('배수진', True, (0, 0, 0))
            achieve_card_text = text_font.render('-다른 플레이어 UNO 후 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*365/900))
            b_date = text_font.render(str(unoother_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*395/900))
            if unoother_date != 0:
                screen.blit(b_date, (display_funct.screen_width*720/1600, display_funct.screen_height*420/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*355/900))

            achieve_card = title_font.render('이제 시작', True, (0, 0, 0))
            achieve_card_text = text_font.render('-싱글플레이 패배', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*495/900))
            c_date = text_font.render(str(first_defeat_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*525/900))
            if first_defeat_date != 0:
                screen.blit(c_date, (display_funct.screen_width*720/1600, display_funct.screen_height*550/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*485/900))

            achieve_card = title_font.render('실력자', True, (0, 0, 0))
            achieve_card_text = text_font.render('-싱글플레이 5연승', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
            d_date = text_font.render(str(stroke5_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
            if stroke5_date != 0:
                screen.blit(d_date, (display_funct.screen_width*720/1600, display_funct.screen_height*680/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*615/900))
                
        elif page == 3:
            achieve_card = title_font.render('포 카드', True, (0, 0, 0))
            achieve_card_text = text_font.render('-한 턴에 4장 내고 승리', True, (0, 0, 0))
            screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*105/900))
            achieve_card_date = text_font.render(str(turn10_date), True, (0, 0, 0))
            screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*135/900))
            if cont3_date != 0:
                screen.blit(achieve_card_date, (display_funct.screen_width*720/1600, display_funct.screen_height*160/900))
                screen.blit(cur_on_button, (display_funct.screen_width*935/1600, display_funct.screen_height*95/900))

        page_text = page_font.render(str(page), True, (255,255, 255))
        screen.blit(page_text, (display_funct.screen_width*790/1600, display_funct.screen_height*745/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.space:
                    menuplay.play()
                    if selected_button == 'next':
                        page += 1
                        if page == 3:
                            selected_button = 'back'
                    elif selected_button == 'back':
                        page -= 1
                        if page == 1:
                            selected_button = 'next'

                elif event.key == display_funct.right:
                    menuplay.play()
                    if page == 2 and selected_button == 'back':
                        selected_button = 'next'
                    elif page == 2 and selected_button == 'next':
                        selected_button = 'back'

                elif event.key == display_funct.left:
                    menuplay.play()
                    if page == 2 and selected_button == 'back':
                        selected_button = 'next'
                    elif page == 2 and selected_button == 'next':
                        selected_button = 'back'

                elif event.key == display_funct.esc:
                    menuplay.play()
                    display_funct.achieve_title = False

        achieve_check()
        pygame.display.flip()


def achieve_check():
    '''
    싱글플레이 대전 승리 업적           변수 싱글 로비     1개

    스토리모드 지역별 클리어 업적       변수 싱글 스토리   4개

    싱글플레이 10턴안에 승리            싱글 로비         1개

    기술카드를 사용하지 않고 승리 1개

    다른 플레이어가 uno를 선언한 뒤에 승리 1개

    카드 100장 내기 1개

    첫 패배 시 1개

    싱글플레이 5연승 1개

    한턴에 카드 3장내기 1개
    
    디스플레이 뛰우기
    '''
    if display_funct.first_victory == True and display_funct.first_victory_achieve_check == 0:     #첫 승리
        achieve = "first_victory"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.first_victory_date = current_date
        config_ach["first_victory_date"] = first_victory_date
        achieve_popup(achieve)
    
    elif display_funct.cleared1 == True and display_funct.a_victory_achieve_check == 0:       #A지역 승리
        achieve = "a_victory"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.a_victory_date = current_date
        config_ach["a_victory_date"] = a_victory_date
        achieve_popup(achieve)

    elif display_funct.cleared2 == True and display_funct.b_victory_achieve_check == 0:       #B지역 승리
        achieve = "b_victory"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.b_victory_date = current_date
        config_ach["b_victory_date"] = b_victory_date
        achieve_popup(achieve)

    elif display_funct.cleared3 == True and display_funct.c_victory_achieve_check == 0:       #C지역 승리
        achieve = "c_victory"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.c_victory_date = current_date
        config_ach["c_victory_date"] = c_victory_date
        achieve_popup(achieve)

    elif display_funct.cleared4 == True and display_funct.d_victory_achieve_check == 0:       #D지역 승리
        achieve = "d_victory"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.d_victory_date = current_date
        config_ach["d_victory_date"] = d_victory_date
        achieve_popup(achieve)

    elif display_funct.turn10 == True and display_funct.turn10_check == 0:       #10턴 승리
        achieve = "turn10"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.turn10_date = current_date
        config_ach["turn10_date"] = turn10_date
        achieve_popup(achieve)

    elif display_funct.fair_sa == True and display_funct.fair_check == 0:       #10턴 승리
        achieve = "fair"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.fair_date = current_date
        config_ach["fair_date"] = fair_date
        achieve_popup(achieve)

    elif display_funct.first_defeat == True and display_funct.first_defeat_check == 0:       #10턴 승리
        achieve = "first_defeat"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.first_defeat_date = current_date
        config_ach["first_defeat_date"] = first_defeat_date
        achieve_popup(achieve)

    elif display_funct.stroke5 >= 5 and display_funct.stroke5_check == 0:       #10턴 승리
        achieve = "stroke5"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.stroke5_date = current_date
        config_ach["stroke5_date"] = stroke5_date
        achieve_popup(achieve)

    elif display_funct.cont3_true == True and display_funct.cont3_check == 0:       #10턴 승리
        achieve = "cont3"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.cont3_date = current_date
        config_ach["cont3_date"] = cont3_date
        achieve_popup(achieve)
    
    elif display_funct.unoother_what == True and display_funct.unoother_check == 0:       #10턴 승리
        achieve = "unoother"
        current_date = datetime.now().strftime("%Y-%m-%d")
        display_funct.unoother_date = current_date
        config_ach["unoother_date"] = display_funct.unoother_date
        achieve_popup(achieve)

def achieve_popup(what):
    title_font = pygame.font.SysFont('malgungothic', 20)
    text_font = pygame.font.SysFont('malgungothic', 16)

    screen.blit(achieve_text_button,(display_funct.screen_width*600.25/1600,display_funct.screen_height*610/900))
    if what == "first_victory":
        screen.blit(card_icon_button2, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('첫 승리', True, (0, 0, 0))
        achieve_card_text = text_font.render('-싱글 플레이 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.first_victory_achieve_check = 1
            config_ach["first_check"] = 1
            display_funct.stack = 0

    elif what == "a_victory":
        screen.blit(card_icon_button2, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('입문자', True, (0, 0, 0))
        achieve_card_text = text_font.render('-A 지역 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.a_victory_achieve_check = 1
            config_ach["a_check"] = 1
            display_funct.stack = 0
    
    elif what == "b_victory":
        screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('초보자', True, (0, 0, 0))
        achieve_card_text = text_font.render('-B 지역 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.b_victory_achieve_check = 1
            config_ach["b_check"] = 1
            display_funct.stack = 0

    elif what == "c_victory":
        screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('중급자', True, (0, 0, 0))
        achieve_card_text = text_font.render('-C 지역 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.c_victory_achieve_check = 1
            config_ach["c_check"] = 1
            display_funct.stack = 0

    elif what == "d_victory":
        display_funct.stack += 1
        screen.blit(card_icon_button1, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        achieve_card = title_font.render('상급자', True, (0, 0, 0))
        achieve_card_text = text_font.render('-D 지역 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.d_victory_achieve_check = 1
            config_ach["d_check"] = 1
            display_funct.stack = 0
    
    elif what == "turn10":
        screen.blit(card_icon_button3, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('전력질주', True, (0, 0, 0))
        achieve_card_text = text_font.render('-싱글플레이 10턴 안에 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.turn10_check = 1
            config_ach["turn10_check"] = 1
            display_funct.stack = 0
    elif what == "fair":
        screen.blit(card_icon_button6, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('페어 플레이', True, (0, 0, 0))
        achieve_card_text = text_font.render('-기술카드 없이 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.fair_check = 1
            config_ach["fair_check"] = 1
            display_funct.stack = 0
    elif what == "first_defeat":
        screen.blit(card_icon_button4, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('이제 시작', True, (0, 0, 0))
        achieve_card_text = text_font.render('-싱글플레이 첫 패배', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.first_defeat_check = 1
            config_ach["first_defeat_check"] = 1
            display_funct.stack = 0

    elif what == "stroke5":
        screen.blit(card_icon_button7, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('실력자', True, (0, 0, 0))
        achieve_card_text = text_font.render('-싱글플레이 5연승', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.stroke5_check = 1
            config_ach["stroke5_check"] = 1
            display_funct.stack = 0

    elif what == "cont3":
        screen.blit(card_icon_button8, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('포 카드', True, (0, 0, 0))
        achieve_card_text = text_font.render('-한 턴에 4장 내고 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.cont3_check = 1
            config_ach["cont3_check"] = 1
            display_funct.stack = 0
    
    elif what == "unoother":
        screen.blit(card_icon_button5, (display_funct.screen_width*615.25/1600,display_funct.screen_height*625/900))
        display_funct.stack += 1
        achieve_card = title_font.render('배수진', True, (0, 0, 0))
        achieve_card_text = text_font.render('-다른 플레이어 UNO 후 승리', True, (0, 0, 0))
        screen.blit(achieve_card, (display_funct.screen_width*720/1600, display_funct.screen_height*625/900))
        screen.blit(achieve_card_text, (display_funct.screen_width*720/1600, display_funct.screen_height*655/900))
        if display_funct.stack > 500:
            display_funct.unoother_check = 1
            config_ach["unoother_check"] = 1
            display_funct.stack = 0
            

    with open("achievement.txt", "w") as fa:
        json.dump(config_ach, fa)








################################################# 시작 화면 ################################################
# 게임 루프
def title_single():
    selected_single = 'single'
    title_sing = True
    while title_sing:
        screen.blit(titlesingle_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*225/900))
        screen.blit(titlestory_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*375/900))
        if selected_single == 'single':
            screen.blit(titlesingle_on_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*225/900))
        elif selected_single == 'story':
            screen.blit(titlestory_on_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*375/900))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.up:
                    menuplay.play()
                    if selected_single == 'single':
                        selected_single = 'story'
                    else:
                        selected_single = 'single'

                elif event.key == display_funct.down:
                    menuplay.play()
                    if selected_single == 'single':
                        selected_single = 'story'
                    else:
                        selected_single = 'single'

                elif event.key == display_funct.space:
                    menuplay.play()
                    if selected_single == 'single':
                        title_sing = False
                        display_funct.single_screen()

                    elif selected_single == 'story':
                        title_sing = False
                        display_funct.instorymode = True
                        display_funct.story_screen()

                elif event.key == display_funct.esc or event.key == display_funct.left:
                    menuplay.play()
                    title_sing = False
                    display_funct.title = True
            elif event.type ==MOUSEBUTTONDOWN:
                menuplay.play()
                if event.button == 1:
                    click_x, click_y = event.pos
                    # 멀티 플레이 부분
               
                    #싱글플레이
                if screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/3 <= click_y <= screen_height/3 + screen_height/12:  
                    title_sing = False
                    display_funct.title = True
                    #Option 버튼
                elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:  
                    title_sing = False
                    display_funct.setting = True
                    display_funct.setting_screen()
                        
                    #Quit 버튼
                elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                screen_height/1.2 <= click_y <= screen_height/1.2 + screen_height/12:
                    pygame.quit()
                    exit()
                    #업적 버튼
                elif screen_width*10/1600 <= click_x <= screen_width*10/1600 + screen_width*26/320 and \
                    screen_height*800/900<=click_y <= screen_height*800/900 + screen_height/9:
                        title_sing = False
                        display_funct.title = True
                        display_funct.achieve_title = True
                        display_funct.achieve_screen()
                        
                elif screen_width*1000/1600 <= click_x <= screen_width*1000/1600 + screen_width*7/32 and \
                screen_height*225/900 <= click_y<= screen_height*225/900+screen_height/9:
                    title_sing = False
                    display_funct.single_screen()
                elif screen_width*1000/1600 <= click_x <= screen_width*1000/1600 + screen_width*7/32 and \
                screen_height*375/900 <= click_y<= screen_height*375/900+screen_height/9:
                    title_sing = False
                    display_funct.instorymode = True
                    display_funct.story_screen()



           
        achieve_check()
        pygame.display.flip()

def title_multi():
    selected_multi = 'host'
    title_mul = True
    pass_font = pygame.font.SysFont('malgungothic', 20)
    while title_mul:
        screen.blit(titlehost_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*375/900))
        screen.blit(titleclient_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*525/900))

        if selected_multi == 'host':
            screen.blit(titlehost_on_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*375/900))

        elif selected_multi == 'client':
            screen.blit(titleclient_on_button,(display_funct.screen_width*1000/1600, display_funct.screen_height*525/900))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.up:
                    menuplay.play()
                    if selected_multi == 'host':
                        selected_multi = 'client'
                    else:
                        selected_multi = 'host'

                elif event.key == display_funct.down:
                    menuplay.play()
                    if selected_multi == 'host':
                        selected_multi = 'client'
                    else:
                        selected_multi = 'host'

                elif event.key == display_funct.space:
                    menuplay.play()
                    if selected_multi == 'host':
                        done = False
                        password = ''
                        input_pw = pass_font.render("Input Password", True, (255, 255, 255))
                        while not done:
                            password_1 = pass_font.render(password, True, (255, 255, 255))
                            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,150,60])
                            screen.blit(input_pw,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                            screen.blit(password_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.space:
                                        if len(password) != 4:
                                            pass
                                        else:
                                            ######### 서버 만들어져야되는
                                            title_mul = False
                                            host_ip = socket.gethostbyname(socket.gethostname())
                                            display_funct.host_screen(password, host_ip)

                                    elif event.key == display_funct.esc:
                                        menuplay.play()
                                        done = True
                                        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,180,60])
                                    
                                    elif event.key == pygame.K_BACKSPACE:
                                        password = password[:-1]

                                    else:
                                        if len(password) > 3:
                                            pass
                                        else:
                                            password += event.unicode
                            pygame.display.flip()

                    elif selected_multi == 'client':
                        done = False
                        ip = ''
                        input_ip = pass_font.render("Input IP", True, (255, 255, 255))
                        password = ''
                        input_pw = pass_font.render("Input Password", True, (255, 255, 255))
                        step = 0
                        while not done:
                            ip_1 = pass_font.render(ip, True, (255, 255, 255))
                            password_1 = pass_font.render(password, True, (255, 255, 255))
                            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,300,60])
                            if step == 0:
                                screen.blit(input_ip,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                                screen.blit(ip_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))

                            elif step == 1:
                                screen.blit(input_pw,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                                screen.blit(password_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))
                                
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.esc:
                                        menuplay.play()
                                        done = True
                                        step = 0
                                        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*270/900,360,80])
                                    
                                    elif event.key == pygame.K_BACKSPACE:
                                        if step == 0:
                                            ip = ip[:-1]
                                        elif step == 1:
                                            password = password[:-1]
                                            
                                    elif event.key == display_funct.space:
                                        if step == 0:
                                            if ip == '':
                                                pass
                                            else:
                                                ########################클라이언트
                                                SERVER_HOST = ip  # 서버 IP 주소
                                                SERVER_PORT = 5555  # 서버 포트 번호

                                                try:
                                                    display_funct.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                    display_funct.client_socket.connect((SERVER_HOST, SERVER_PORT))
                                                    
                                                    step = 1
                                                except:
                                                    step = 0
                                                    pass
                                                

                                        elif step == 1:
                                            if len(password) != 4:
                                                pass
                                            else:
                                                ####### 클라이언트 접속 확인 IP 확인 후 패스워드 확인하게 만듬
                                                #display_funct.host_screen(password, ip)
                                                #패스워드를 보내고 안맞으면 킥
                                                display_funct.client_socket.sendall(password.encode())
                                                message = client_socket.recv(1024)
                                                if (message.decode() == 'close'):
                                                    client_socket.close()
                                                    pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*270/900,360,80])
                                                    pw_error = pass_font.render("Password Error", True, (255, 255, 255))
                                                    screen.blit(pw_error,(display_funct.screen_width*1020/1600,display_funct.screen_height*270/900))
                                                    step=0
                                                    password = ''
                                                elif (message.decode() == 'full'):
                                                    client_socket.close()
                                                    pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*270/900,360,80])
                                                    full_1 = pass_font.render("Room is fulled", True, (255, 255, 255))
                                                    screen.blit(full_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*270/900))
                                                    step=0
                                                else:
                                                    title_mul = False
                                                    display_funct.client_screen(ip,password)
                                    else:
                                        if step == 0:
                                            if len(ip) > 20:
                                                pass
                                            else:
                                                ip += event.unicode
                                        elif step == 1:
                                            if len(password) >3:
                                                pass
                                            else:
                                                password += event.unicode
                                    

                            pygame.display.flip()

                elif event.key == display_funct.esc or event.key == display_funct.left:
                    menuplay.play()
                    title_mul = False
                    display_funct.title = True
           
            elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭시
                if event.button == 1:
                    click_x, click_y = event.pos
                    
                    #멀티 플레이 버튼
                    if  screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/2 <= click_y <= screen_height/2 + screen_height/12:
                        title_mul = False
                        display_funct.title = True
                        #Option 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:  
                        display_funct.setting = True
                        display_funct.setting_screen()
                            
                        #Quit 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/1.2 <= click_y <= screen_height/1.2 + screen_height/12:
                        pygame.quit()
                        exit()
                    #업적버튼
                    elif screen_width*10/1600 <= click_x <= screen_width*10/1600 + screen_width*26/320 and \
                    screen_height*800/900<=click_y <= screen_height*800/900 + screen_height/9:
                        title_mul = False
                        display_funct.achieve_title = True
                        display_funct.achieve_screen()
                    elif screen_width*1000/1600 <= click_x <= screen_width*1000/1600 + screen_width*7/32 and \
                    screen_height*375/955 <=click_y <= screen_height*375/955+screen_height/9:
                        done = False
                        password = ''
                        input_pw = pass_font.render("Input Password", True, (255, 255, 255))
                        while not done:
                            password_1 = pass_font.render(password, True, (255, 255, 255))
                            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,150,60])
                            screen.blit(input_pw,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                            screen.blit(password_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.space:
                                        if len(password) != 4:
                                            pass
                                        else:
                                            ######### 서버 만들어져야되는
                                            title_mul = False
                                            host_ip = socket.gethostbyname(socket.gethostname())
                                            display_funct.host_screen(password, host_ip)

                                    elif event.key == display_funct.esc:
                                        done = True
                                        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,150,60])
                                    
                                    elif event.key == pygame.K_BACKSPACE:
                                        password = password[:-1]

                                    else:
                                        if len(password) > 3:
                                            pass
                                        else:
                                            password += event.unicode
                            pygame.display.flip()
                    #client 버튼
                    elif screen_width*1000/1600 <= click_x <= screen_width*1000/1600 + screen_width*7/32 and \
                    screen_height*525/900 <=click_y <= screen_height*525/900+screen_height/9:
                        done = False
                        ip = ''
                        input_ip = pass_font.render("Input IP", True, (255, 255, 255))
                        password = ''
                        input_pw = pass_font.render("Input Password", True, (255, 255, 255))
                        step = 0
                        while not done:
                            ip_1 = pass_font.render(ip, True, (255, 255, 255))
                            password_1 = pass_font.render(password, True, (255, 255, 255))
                            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,300,60])
                            if step == 0:
                                screen.blit(input_ip,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                                screen.blit(ip_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))

                            elif step == 1:
                                screen.blit(input_pw,(display_funct.screen_width*1020/1600,display_funct.screen_height*300/900))
                                screen.blit(password_1,(display_funct.screen_width*1020/1600,display_funct.screen_height*330/900))
                                
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.esc:
                                        done = True
                                        step = 0
                                        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1020/1600,display_funct.screen_height*300/900,300,60])
                                    
                                    elif event.key == pygame.K_BACKSPACE:
                                        if step == 0:
                                            ip = ip[:-1]
                                        elif step == 1:
                                            password = password[:-1]
                                            
                                    elif event.key == display_funct.space:
                                        if step == 0:
                                            if ip == '':
                                                pass
                                            else:
                                                ########################클라이언트
                                                SERVER_HOST = ip  # 서버 IP 주소
                                                SERVER_PORT = 5555  # 서버 포트 번호

                                                try:
                                                    display_funct.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                    display_funct.client_socket.connect((SERVER_HOST, SERVER_PORT))
                                                    #여기서 받았을 서버가
                                                    step = 1
                                                except:
                                                    step = 0
                                                    pass
                                                

                                        elif step == 1:
                                            if len(password) != 4:
                                                pass
                                            else:
                                                title_mul = False
                                                ####### 클라이언트 접속 확인 IP 확인 후 패스워드 확인하게 만듬
                                                #display_funct.host_screen(password, ip)
                                                #패스워드를 보내고 안맞으면 킥
                                                display_funct.client_socket.sendall(password.encode())
                                                message = client_socket.recv(1024)
                                                if (message.decode() == 'close'):
                                                    client_socket.close()
                                                    PY_UNO.main()
                                                else:
                                                    display_funct.client_screen(ip,password)
                                    else:
                                        if step == 0:
                                            if len(ip) > 20:
                                                pass
                                            else:
                                                ip += event.unicode
                                        elif step == 1:
                                            if len(password) >3:
                                                pass
                                            else:
                                                password += event.unicode
                                    

                            pygame.display.flip()
                        print("client 버튼")    

        achieve_check()
        pygame.display.flip()
        
def title_screen():
    font = pygame.font.SysFont('malgungothic', 72)
    selected_button = "single"
    while display_funct.title: 
        text = font.render('UNO!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2.1, screen_height // 5))
        screen.fill(black)
        screen.blit(text, text_rect)
        # 버튼 생성
        screen.blit(titlesingle_button,(display_funct.screen_width*625/1600, display_funct.screen_height/3))
        screen.blit(titlemulti_button,(display_funct.screen_width*625/1600, display_funct.screen_height/2))
        screen.blit(titleoption_button,(display_funct.screen_width*625/1600, display_funct.screen_height/1.5))
        screen.blit(titleexit_button,(display_funct.screen_width*625/1600, display_funct.screen_height/1.2))
        screen.blit(titleachieve_button,(display_funct.screen_width*10/1600, display_funct.screen_height*800/900))

        # 선택된 버튼
        if selected_button == "single":
            screen.blit(titlesingle_on_button,(display_funct.screen_width*625/1600, display_funct.screen_height/3))
        elif selected_button == "story":
            screen.blit(titlemulti_on_button,(display_funct.screen_width*625/1600, display_funct.screen_height/2))
        elif selected_button == "option":
            screen.blit(titleoption_on_button,(display_funct.screen_width*625/1600, display_funct.screen_height/1.5))
        elif selected_button == "exit":
            screen.blit(titleexit_on_button,(display_funct.screen_width*625/1600, display_funct.screen_height/1.2))
        elif selected_button == 'achieve':
            screen.blit(titleachieve_on_button,(display_funct.screen_width*10/1600, display_funct.screen_height*800/900))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.up:
                    menuplay.play()
                    # 위쪽 방향키 클릭 시
                    if selected_button == "single":
                        selected_button = "exit"
                    elif selected_button == "story":
                        selected_button = "single"               
                    elif selected_button == "option":
                        selected_button = "story"
                    elif selected_button == "exit":
                        selected_button = "option"

                elif event.key == display_funct.down:
                    menuplay.play()
                    # 아래쪽 방향키 클릭 시
                    if selected_button == "single":
                        selected_button = "story"
                    elif selected_button == "story":
                        selected_button = "option"
                    elif selected_button == "option":
                        selected_button = "exit"
                    else:
                        selected_button = "single"
                elif event.key == display_funct.space: #우측키 스페이스 엔터
                    menuplay.play()
                    if selected_button == "single":
                        display_funct.title = False
                        display_funct.title_single()
                    
                    elif selected_button == "story":
                        display_funct.title = False
                        display_funct.title_multi()
                        #multi 추가 해야됨

                    elif selected_button == "option":
                        # Options 버튼 클릭 시 실행할 코드
                        
                        display_funct.setting = True
                        display_funct.setting_screen()

                    elif selected_button == "exit":
                        # Quit 버튼 클릭 시 실행할 코드
                        pygame.quit()
                        exit()
                    elif selected_button == 'achieve':
                        display_funct.achieve_title = True
                        display_funct.achieve_screen()

                elif event.key == display_funct.left:
                    menuplay.play()
                    if selected_button == 'achieve':
                        pass
                    else:
                        temp = selected_button
                        selected_button = 'achieve'
                
                elif event.key == display_funct.right:
                    menuplay.play()
                    if selected_button == 'achieve':
                        selected_button = temp

            elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭시
                if event.button == 1:
                    click_x, click_y = event.pos
                    #멀티 플레이 버튼
                    if  screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/2 <= click_y <= screen_height/2 + screen_height/12: 
                        display_funct.title = False
                        display_funct.title_multi()
                    #싱글플레이
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/3 <= click_y <= screen_height/3 + screen_height/12:  
                        display_funct.title = False
                        display_funct.title_single()
                        #Option 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:  
                        display_funct.setting = True
                        display_funct.setting_screen()
                            
                        #Quit 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/1.2 <= click_y <= screen_height/1.2 + screen_height/12:
                        pygame.quit()
                        exit()
                    
                    elif screen_width*10/1600 <= click_x <= screen_width*10/1600 + screen_width*26/320 and \
                    screen_height*800/900<=click_y <= screen_height*800/900 + screen_height/9:
                        display_funct.achieve_title = True
                        display_funct.achieve_screen()
        achieve_check()
        pygame.display.flip()

################################## 싱글플레이 ################################################
def single_screen():
    selected_button1 = "ai1"
    selected_ai2 = "no"
    selected_ai3 = "no"
    selected_ai4 = "no"
    selected_ai5 = "no"
    selected_ai6 = "no"
    player_font = pygame.font.SysFont('malgungothic', 25)
    i=0
    playing = True
    player1_name = "Player1"
    while playing:
        screen.fill(black)
        screen.blit(singleoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*185/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*255/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*325/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*395/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*465/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*535/900))
        screen.blit(singlestart_button, (screen_width*677.5/1600,screen_height*690/900))

        selected_ais = [selected_ai2,selected_ai3,selected_ai4,selected_ai5,selected_ai6]
        i = 0

        for a in selected_ais:
            if a != "no":
                i+=1
        
        player1 = player_font.render(player1_name, True, (255, 255, 255))
        area = player_font.render('AI', True, (255, 255, 255))
        area_a = player_font.render('AI_A', True, (255, 255, 255))

        
        if selected_button1 == "ai1":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*185/900))
        elif selected_button1 == "ai2":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*255/900))
        elif selected_button1 == "ai3":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*325/900))
        elif selected_button1 == "ai4":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*395/900))
        elif selected_button1 == "ai5":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*465/900))
        elif selected_button1 == "ai6":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*535/900))

        elif selected_button1 == "start":
            screen.blit(singlestart_on_button, (screen_width*677.5/1600,screen_height*690/900))

        screen.blit(player1, (display_funct.screen_width*755/1600, display_funct.screen_height*200/900))
        if selected_ai2 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*270/900))
        elif selected_ai2 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*770/1600, display_funct.screen_height*270/900))
        
        if selected_ai3 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*340/900))
        elif selected_ai3 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*770/1600, display_funct.screen_height*340/900))
        
        if selected_ai4 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*410/900))
        elif selected_ai4 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*770/1600, display_funct.screen_height*410/900))
        
        if selected_ai5 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*480/900))
        elif selected_ai5 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*770/1600, display_funct.screen_height*480/900))
        
        if selected_ai6 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*550/900))
        elif selected_ai6 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*770/1600, display_funct.screen_height*550/900))
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.up:
                    menuplay.play()
                    # 위쪽 방향키 클릭 시

                    if selected_button1 == "ai1":
                        pass 
                    elif selected_button1 == "ai2":
                        selected_button1 = "ai1"
                    elif selected_button1 == "ai3":
                        selected_button1 = "ai2"
                    elif selected_button1 == "ai4":
                        selected_button1 = "ai3"
                    elif selected_button1 == "ai5":
                        selected_button1 = "ai4"
                    elif selected_button1 == "ai6":
                        selected_button1 = "ai5"
                    elif selected_button1 == "start":
                        selected_button1 = "ai6"

                elif event.key == display_funct.down:
                    menuplay.play()
                    if selected_button1 == "ai1":
                        selected_button1 = "ai2"
                    elif selected_button1 == "ai2":
                        selected_button1 = "ai3"
                    elif selected_button1 == "ai3":
                        selected_button1 = "ai4"
                    elif selected_button1 == "ai4":
                        selected_button1 = "ai5"
                    elif selected_button1 == "ai5":
                        selected_button1 = "ai6"
                    elif selected_button1 == "ai6":
                        selected_button1 = "start"
                    elif selected_button1 == "start":
                        pass

                elif event.key == display_funct.space:
                    menuplay.play()
                    if selected_button1 == "ai1":
                        done = False
                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.space:
                                        done = True
                                    elif event.key == pygame.K_BACKSPACE:
                                        player1_name = player1_name[:-1]
                                    else:
                                        if len(player1_name) > 6:
                                            pass
                                        else:
                                            player1_name += event.unicode
                            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*185/900))
                            player1 = player_font.render(player1_name, True, (255, 255, 255))
                            screen.blit(player1, (display_funct.screen_width*755/1600, display_funct.screen_height*200/900))
                            pygame.display.flip()
                                        
                    elif selected_button1 == "ai2":
                        if selected_ai2 == "no": 
                            selected_ai2 = "area"
                        elif selected_ai2 == "area":
                            selected_ai2 = "area_a"
                        elif selected_ai2 == "area_a":
                            selected_ai2 = "no"

                    elif selected_button1 == "ai3":
                        if selected_ai3 == "no":
                            selected_ai3 = "area"
                        elif selected_ai3 == "area":
                            selected_ai3 = "area_a"
                        elif selected_ai3 == "area_a":
                            selected_ai3 = "no"

                    elif selected_button1 == "ai4":
                        if selected_ai4 == "no":
                            selected_ai4 = "area"
                        elif selected_ai4 == "area":
                            selected_ai4 = "area_a"
                        elif selected_ai4 == "area_a":
                            selected_ai4 = "no"

                    elif selected_button1 == "ai5":
                        if selected_ai5 == "no":
                            selected_ai5 = "area"
                        elif selected_ai5 == "area":
                            selected_ai5 = "area_a"
                        elif selected_ai5 == "area_a":
                            selected_ai5 = "no"

                    elif selected_button1 == "ai6":
                        if selected_ai6 == "no":
                            selected_ai6 = "area"
                        elif selected_ai6 == "area":
                            selected_ai6 = "area_a"
                        elif selected_ai6 == "area_a":
                            selected_ai6 = "no"

                    elif selected_button1 == "start":
                        if i == 0:
                            pass
                        else:
                            playing = False

                elif event.key == display_funct.esc:
                    menuplay.play()
                    display_funct.title = True
                    PY_UNO.main()


        pygame.display.flip()

    board1 = game_classes.Board("board1")  

    # initilizing a deck to be used within the game (3 copies are added to
    # each other)
    deck1 = gen_rand_deck("deck1", 0)

    for a in deck1.deck:
        print(a.name)
    # defining a 7 player uno game
    player1 = game_classes.Player("player_1")
    player1.grab_cards(deck1, 5)
    playerAI_list = []

    i=2
    for a in selected_ais:

        if a == "no":
            pass

        elif a == "area":
            playerAI = game_AI.make_AI_basic(deck1, "player_"+str(i)+"AI", 7)
            i+=1
            playerAI_list.append(playerAI)

        elif a == "area_a":
            playerAI = game_AI.make_AI_A(deck1, "player_"+str(i)+"AI", 7)
            i+=1
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
                if event.key == display_funct.right or event.key == display_funct.left:
                    menuplay.play()
                    if starting == "yes":
                        starting = "no"
                    else:
                        starting = "yes"

                elif event.key == display_funct.space:
                    menuplay.play()
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
            screen.blit(mapaboutd_button, (display_funct.screen_width*1120/1600 ,display_funct.screen_height*80/900))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.right:
                    menuplay.play()
                    if display_funct.cur_stage == 1:
                        if display_funct.cleared1 == True:
                            display_funct.cur_stage = 2

                    elif display_funct.cur_stage == 2:
                        if display_funct.cleared2 == True:
                            display_funct.cur_stage = 3


                    elif display_funct.cur_stage == 3:
                        if display_funct.cleared3 == True:
                            display_funct.cur_stage = 4

                    elif display_funct.cur_stage == 4:
                        menuplay.play()
                        pass
                elif event.key == display_funct.left:
                    menuplay.play()

                    if display_funct.cur_stage == 2:
                        display_funct.cur_stage = 1
                    elif display_funct.cur_stage == 3:
                        display_funct.cur_stage = 2
                    elif display_funct.cur_stage == 4:
                        display_funct.cur_stage = 3

                
                elif event.key == display_funct.space:
                    menuplay.play()
                    check_screen()

                elif event.key == display_funct.esc:
                    menuplay.play()
                    display_funct.s_playing=False
                    display_funct.title = True
                    PY_UNO.main()

        achieve_check()
        pygame.display.flip()

    ####################### 스테이지 시작##################

    if display_funct.title:
        pass

    else:
        if display_funct.cur_stage == 1:
            board1 = game_classes.Board("board1") 

            deck1 = gen_rand_deck("deck1", 1)

            player1 = game_classes.Player("player_1")
            
            # 60:40 테스트용 출력
            test_player = game_classes.Player("test_player")
            test_deck = generate_test_A("test")
            game_story_setting.test_setting(test_deck, test_player)

            setting = game_story_setting.setting_A(deck1, player1)

            #display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, setting)   

        elif display_funct.cur_stage == 2:
            board1 = game_classes.Board("board1") 

            deck1 = gen_rand_deck("deck1", 1)

            player1 = game_classes.Player("player_1")
            setting = game_story_setting.setting_B(deck1, player1)

            display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, setting)

        elif display_funct.cur_stage == 3:
            board1 = game_classes.Board("board1")  

            # initilizing a deck to be used within the game (3 copies are added to
            # each other)
            deck1 = gen_rand_deck("deck1", 0)

            # defining a 7 player uno game
            player1 = game_classes.Player("player_1")
            player1.grab_cards(deck1, 7)

            player_2AI = game_AI.make_AI_basic(deck1, "player_2AI",7)
            player_3AI = game_AI.make_AI_basic(deck1, "player_3AI",7)

            display_funct.redraw_hand_visble(player1, None)
            

            # enters into playing the game
            game_logic.game_loop_C(board1, deck1, [player1, player_2AI,player_3AI])
            

        elif display_funct.cur_stage == 4:
            board1 = game_classes.Board("board1")
            deck1 = gen_rand_deck("deck_d", 0)
            player1 = game_classes.Player("player_1")
            player1.grab_cards(deck1, 7)
            player2AI = game_AI.make_AI_basic(deck1, "player_2AI", 7)
            display_funct.redraw_hand_visble(player1, None)
            game_logic.game_loop(board1, deck1, [player1, player2AI])
    
def wait(time):
    done = False
    stack_wait = 0
    while not done:
        stack_wait += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if stack_wait > time:
            done = True
            print("out")
        

###################################### 멀티 방 #############################################

Accept_return = []
check_password = 0
client_nick = ''
stack_3 = 0
server_socket = 0

def Accept(server_socket):
    print("Thread Accept Start")
    while True:
        client_socket, addr = server_socket.accept()
        print("break")
        Accept_return.append(client_socket)
        Accept_return.append(addr)

def Receive(client_socket):
    print("Thread Receive Start")
    data = client_socket.recv(4096)
    display_funct.check_password = data.decode()

def Message_Receive(client_socket):
    try:
        print("Thread Message Receive Start")
        nick = client_socket.recv(4096)
        display_funct.client_nick = nick.decode()
        print(nick.decode())
        display_funct.stack_3 = 0
        
    except:
        pass

def host_screen(password,host_ip):
    selected_button1 = "ai1"
    selected_ai1 = "Player1"
    selected_ai2 = "no"
    selected_ai3 = "no"
    selected_ai4 = "no"
    selected_ai5 = 0

    player_font = pygame.font.SysFont('malgungothic', 25)
    i=0
    playing = True
    player1_name = "Player1"

    ip = player_font.render("IP: " + str(host_ip), True, (255, 255, 255))
    pw = player_font.render("Password: " + str(password), True, (255, 255, 255))

    HOST = host_ip
    PORT = 5555  # 포트 번호 (임의의 값으로 설정)

    display_funct.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    display_funct.server_socket.bind((HOST, PORT))
    display_funct.server_socket.listen()
    
    t = threading.Thread(target=Accept, args=(display_funct.server_socket,))

    t.start()
    print('서버가 시작되었습니다. 클라이언트의 연결을 기다리는 중...')
    
    stack_1 = 0
    stack_2 = 0
    
   
    chat = ''
    while playing:
        try:
            if len(Accept_return) != 0:
                if stack_1 == 0:
                    display_funct.client_socket, addr = Accept_return
                    s = threading.Thread(target=Receive, args=(display_funct.client_socket,))
                    s.start()
                    display_funct.Accept_return = []
                    chat = 'Client Accepted'

            if display_funct.check_password != 0:
                i = 0
                for a in selected_ais:
                    if a == "no":
                        i += 1

                if check_password != password:
                    message = "close"
                    client_socket.sendall(message.encode())
                    display_funct.check_password = 0
                    chat = 'Client Password Error'
                    
                
                elif i == 0:
                    message = "full"
                    client_socket.sendall(message.encode())
                    display_funct.check_password = 0
                    chat = 'Client No room'
                else:
                    message = "ok"
                    client_socket.sendall(message.encode())
                    display_funct.check_password = 0
                    stack_2=1
                    chat = 'Client Joined'
                
            selected_ais = [selected_ai1,selected_ai2,selected_ai3,selected_ai4, selected_button1, selected_ai5]
            if stack_2 == 1:
                for a in range(len(selected_ais)):
                    if "client" not in selected_ais:
                        if selected_ais[a] == "no":
                            selected_ais[a] = "client"
                            if a==1:
                                selected_ai2 = "client"
                            elif a==2:
                                selected_ai3 = "client"
                            elif a==3:
                                selected_ai4 = "client"
                            break
                serialized_data = pickle.dumps(selected_ais)
                display_funct.client_socket.sendall(serialized_data)
            
                if display_funct.stack_3 == 0:
                    display_funct.stack_3 = 1
                    m = threading.Thread(target=Message_Receive, args=(display_funct.client_socket,))
                    m.start()

        except socket.error as e:
            display_funct.client_socket = ''
            stack_2 = 0
            chat = 'Client Exit'
            print("Socket error",e)
            for a in range(len(selected_ais)):
                if selected_ais[a] == "client":
                    selected_ais[a] = "no"
                    if a==1:
                        selected_ai2 = "no"
                    elif a==2:
                        selected_ai3 = "no"
                    elif a==3:
                        selected_ai4 = "no"
            if selected_ai5 == "kick":
                chat = "Client kicked"

            selected_ai5 = 0
            display_funct.stack_3 = 0
        
        screen.fill(black)
        
        screen.blit(achieveoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(ip, (screen_width*590/1600,screen_height*80/900))
        screen.blit(pw, (screen_width*590/1600,screen_height*115/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*185/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*305/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*425/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*545/900))
        screen.blit(singlestart_button, (screen_width*677.5/1600,screen_height*690/900))

        screen.blit(achieve_text_button, (screen_width*1100/1600,screen_height*400/900))
        chatting = player_font.render(chat, True, (0, 0, 0))
        screen.blit(chatting, (screen_width*1120/1600,screen_height*420/900))

        i = 0

        for a in selected_ais:
            if a == "area" or a == "client":
                i+=1
        
        player1 = player_font.render(selected_ai1, True, (255, 255, 255))
        area = player_font.render('AI', True, (255, 255, 255))
        area_a = player_font.render('Closed', True, (255, 255, 255))
        client_name = player_font.render(display_funct.client_nick, True, (255, 255, 255))
        
        if selected_button1 == "ai1":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*185/900))
        elif selected_button1 == "ai2":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*305/900))
        elif selected_button1 == "ai3":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*425/900))
        elif selected_button1 == "ai4":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*545/900))
        elif selected_button1 == "start":
            screen.blit(singlestart_on_button, (screen_width*677.5/1600,screen_height*690/900))

        screen.blit(player1, (display_funct.screen_width*755/1600, display_funct.screen_height*200/900))
        if selected_ai2 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*320/900))
        elif selected_ai2 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*320/900))
        elif selected_ai2 == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*320/900))
        
        if selected_ai3 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*440/900))
        elif selected_ai3 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*440/900))
        elif selected_ai3 == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*440/900))

        if selected_ai4 == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*560/900))
        elif selected_ai4 == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*560/900))
        elif selected_ai4 == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*560/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.up:
                    # 위쪽 방향키 클릭 시

                    if selected_button1 == "ai1":
                        pass 
                    elif selected_button1 == "ai2":
                        selected_button1 = "ai1"
                    elif selected_button1 == "ai3":
                        selected_button1 = "ai2"
                    elif selected_button1 == "ai4":
                        selected_button1 = "ai3"
                    elif selected_button1 == "start":
                        selected_button1 = "ai4"

                elif event.key == display_funct.down:
                    if selected_button1 == "ai1":
                        selected_button1 = "ai2"
                    elif selected_button1 == "ai2":
                        selected_button1 = "ai3"
                    elif selected_button1 == "ai3":
                        selected_button1 = "ai4"
                    elif selected_button1 == "ai4":
                        selected_button1 = "start"
                    elif selected_button1 == "start":
                        pass
                
                elif event.key == display_funct.space:
                    if selected_button1 == "ai1":
                        done = False
                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.space:
                                        done = True
                                    elif event.key == pygame.K_BACKSPACE:
                                        selected_ai1 = selected_ai1[:-1]
                                    else:
                                        if len(selected_ai1) > 6:
                                            pass
                                        else:
                                            selected_ai1 += event.unicode
                            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*185/900))
                            player1 = player_font.render(selected_ai1, True, (255, 255, 255))
                            screen.blit(player1, (display_funct.screen_width*755/1600, display_funct.screen_height*200/900))
                            pygame.display.flip()
                                        
                    elif selected_button1 == "ai2":
                        if selected_ai2 == "client":
                            selected_ai5 = "kick"
                        elif selected_ai2 == "no":
                            selected_ai2 = "area"
                        elif selected_ai2 == "area":
                            selected_ai2 = "area_a"
                        elif selected_ai2 == "area_a":
                            selected_ai2 = "no"

                    elif selected_button1 == "ai3":
                        if selected_ai3 == "client":
                            selected_ai5 = "kick"
                        elif selected_ai3 == "no":
                            selected_ai3 = "area"
                        elif selected_ai3 == "area":
                            selected_ai3 = "area_a"
                        elif selected_ai3 == "area_a":
                            selected_ai3 = "no"

                    elif selected_button1 == "ai4":
                        if selected_ai4 == "client":
                            selected_ai5 = "kick"
                        elif selected_ai4 == "no":
                            selected_ai4 = "area"
                        elif selected_ai4 == "area":
                            selected_ai4 = "area_a"
                        elif selected_ai4 == "area_a":
                            selected_ai4 = "no"

                    elif selected_button1 == "start":
                        if i == 0:
                            pass
                        else:
                            playing = False

                elif event.key == display_funct.esc:
                    display_funct.server_socket.close()
                    display_funct.title = True
                    PY_UNO.main()

    
        pygame.display.flip()

    pygame.time.delay(100)
    selected_ais[5] = 'start'
    serialized_data = pickle.dumps(selected_ais)
    display_funct.client_socket.sendall(serialized_data)
    pygame.time.delay(100)

    board1 = game_classes.Board("board1")  

    # initilizing a deck to be used within the game (3 copies are added to
    # each other)
    deck1 = gen_rand_deck("deck1", 0)

    # defining a 7 player uno game
    player1 = game_classes.Player("player_1Host")
    player1.grab_cards(deck1, 5)
    playerAI_list = []
    
    i=2
    for a in selected_ais:

        if a == "no":
            pass

        elif a == "area":
            playerAI = game_AI.make_AI_basic(deck1, "player_"+str(i)+"AI", 7)
            i+=1
            playerAI_list.append(playerAI)
        elif a == "client":
            playerAI = game_AI.make_Client(deck1 ,"player_"+str(i)+"Client")
            i+=1
            playerAI_list.append(playerAI)


    display_funct.redraw_hand_visble(player1, None)

    # enters into playing the game
    game_logic.game_loop_host(board1, deck1, [player1]+ playerAI_list)
    
def client_screen(host_ip,password):
    playing = True
    player_font = pygame.font.SysFont('malgungothic', 25)
    selected_button1 = "ai1"
    ip = player_font.render("IP: " + str(host_ip), True, (255, 255, 255))
    pw = player_font.render("Password: " + str(password), True, (255, 255, 255))
    client_nick = 'Client'
    display_funct.client_socket.send(client_nick.encode())
    while playing:
        screen.fill(black)
        screen.blit(achieveoption_button, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(ip, (screen_width*590/1600,screen_height*80/900))
        screen.blit(pw, (screen_width*590/1600,screen_height*115/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*185/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*305/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*425/900))
        screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*545/900))
        screen.blit(singlestart_button, (screen_width*677.5/1600,screen_height*690/900))
    
        datas = display_funct.client_socket.recv(4096)
        try:
            selected_ais = pickle.loads(datas)
        except:
            pass
        if selected_ais[5] == 'start':
            display_funct.client_socket.send("Okay".encode())
            playing = False
            game_logic.game_loop_client()
        if selected_ais[5] == 'kick':
            playing = False
            display_funct.title = True
            display_funct.client_socket.close()
            PY_UNO.main()

        player = []
        for i in range(len(selected_ais)-2):
            player.append(selected_ais[i])

        selected_button1 = selected_ais[4]

        if selected_button1 == "ai1":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*185/900))
        elif selected_button1 == "ai2":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*305/900))
        elif selected_button1 == "ai3":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*425/900))
        elif selected_button1 == "ai4":
            screen.blit(singleplayer_on_button, (screen_width*677.5/1600,screen_height*545/900))
        elif selected_button1 == "start":
            screen.blit(singlestart_on_button, (screen_width*677.5/1600,screen_height*690/900))

        player1 = player_font.render(str(player[0]), True, (255, 255, 255))
        area = player_font.render('AI', True, (255, 255, 255))
        area_a = player_font.render('Closed', True, (255, 255, 255))
        client_name = player_font.render(client_nick, True, (255, 255, 255))

        screen.blit(player1, (display_funct.screen_width*755/1600, display_funct.screen_height*200/900))
        if player[1] == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*320/900))
        elif player[1] == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*320/900))
        elif player[1] == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*320/900))

        if player[2] == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*440/900))
        elif player[2] == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*440/900))
        elif player[2] == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*440/900))

        if player[3] == "area":
            screen.blit(area, (display_funct.screen_width*785/1600, display_funct.screen_height*560/900))
        elif player[3] == "area_a":
            screen.blit(area_a, (display_funct.screen_width*750/1600, display_funct.screen_height*560/900))
        elif player[3] == "client":
            screen.blit(client_name, (display_funct.screen_width*750/1600, display_funct.screen_height*560/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == display_funct.esc:
                    display_funct.title = True
                    display_funct.client_socket.close()
                    PY_UNO.main()
                elif event.key == display_funct.space:
                    done = False
                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == display_funct.space:
                                    done = True
                                elif event.key == pygame.K_BACKSPACE:
                                    client_nick = client_nick[:-1]
                                    if client_nick == '':
                                        fake_nick = ' '
                                        display_funct.client_socket.send(fake_nick.encode())
                                    else:
                                        display_funct.client_socket.send(client_nick.encode())
                                else:
                                    if len(client_nick) > 6:
                                        pass
                                    else:
                                        client_nick += event.unicode
                                        display_funct.client_socket.send(client_nick.encode())

                        player1 = player_font.render(client_nick, True, (255, 255, 255))
                        if player[1] == "client":
                            screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*305/900))
                            screen.blit(player1, (display_funct.screen_width*750/1600, display_funct.screen_height*320/900))
                        elif player[2] == "client":
                            screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*425/900))
                            screen.blit(player1, (display_funct.screen_width*750/1600, display_funct.screen_height*440/900))
                        elif player[3] == "client":
                            screen.blit(singleplayer_button, (screen_width*677.5/1600,screen_height*545/900))
                            screen.blit(player1, (display_funct.screen_width*750/1600, display_funct.screen_height*560/900))
                        pygame.display.flip()
        pygame.display.flip()

def redraw_screen_client(player_you, board, players_other):
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
















################################### 이미지 파일 ###############################################
#타이틀
titlestart_image = pygame.image.load("image/titlestart.png")
titleoption_image = pygame.image.load("image/titleoption.png")
titleexit_image = pygame.image.load("image/titleexit.png")
titlesingle_image = pygame.image.load("image/titlesingle.png")
titlestory_image = pygame.image.load("image/titlestory.png")
titlemulti_image = pygame.image.load("image/titlemulti.png")
titleachieve_image = pygame.image.load("image/titleachieve.png")
titlehost_image = pygame.image.load("image/host.png")
titleclient_image = pygame.image.load("image/client.png")

#타이틀_ON
titlestart_on_image = pygame.image.load("image/titlestart_on.png")
titleoption_on_image = pygame.image.load("image/titleoption_on.png")
titleexit_on_image = pygame.image.load("image/titleexit_on.png")
titlesingle_on_image = pygame.image.load("image/titlesingle_on.png")
titlestory_on_image = pygame.image.load("image/titlestory_on.png")
titlemulti_on_image = pygame.image.load("image/titlemulti_on.png")
titleachieve_on_image = pygame.image.load("image/titleachieve_on.png")
titlehost_on_image = pygame.image.load("image/host_on.png")
titleclient_on_image = pygame.image.load("image/client_on.png")

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
keysetting_image = pygame.image.load("image/keysetting.png")


#옵션_ON
full_on_image = pygame.image.load("image/full_on.png")
check_on_image = pygame.image.load("image/check_on.png")
checkon_on_image = pygame.image.load("image/checkon_on.png")
small_on_image = pygame.image.load("image/small_on.png")
med_on_image = pygame.image.load("image/med_on.png")
reset_on_image = pygame.image.load("image/reset_on.png")
keyset_on_image = pygame.image.load("image/keyset_on.png")

#업적
achieve_image = pygame.image.load("image/achieveoption.png")
achieve_text = pygame.image.load("image/achieve_text.png")
card_icon_image1 = pygame.image.load("image/icon_1.png")
card_icon_image2 = pygame.image.load("image/icon_2.png")
card_icon_image3 = pygame.image.load("image/icon_3.png")
card_icon_image4 = pygame.image.load("image/icon_4.png")
card_icon_image5 = pygame.image.load("image/icon_5.png")
card_icon_image6 = pygame.image.load("image/icon_6.png")
card_icon_image7 = pygame.image.load("image/icon_7.png")
card_icon_image8 = pygame.image.load("image/icon_8.png")

#결과창
resultwin_image = pygame.image.load("image/winner.png")
resultlose_image = pygame.image.load("image/lose.png")

#싱글플레이
singleoption_image = pygame.image.load("image/singleoption.png")
singleplayer_image = pygame.image.load("image/play.png")
singleplayer_on_image = pygame.image.load("image/play_on.png")
singleai1_image = pygame.image.load("image/ai1.png")
singleai2_image = pygame.image.load("image/ai2.png")
singleai3_image = pygame.image.load("image/ai3.png")
singleai4_image = pygame.image.load("image/ai4.png")
singleai5_image = pygame.image.load("image/ai5.png")
singleplus_image = pygame.image.load("image/plus.png")
singleplus_on_image = pygame.image.load("image/plus_on.png")
singleminus_image = pygame.image.load("image/minus.png")
singleminus_on_image = pygame.image.load("image/minus_on.png")

uno_image = pygame.image.load("image/uno.png")
uno_on_image = pygame.image.load("image/uno_on.png")

#싱글로비
singlelobby_image = pygame.image.load("image/singlelobby.png")
mapabouta_image = pygame.image.load("image/mapabouta.png")
mapaboutb_image = pygame.image.load("image/mapaboutb.png")
mapaboutc_image = pygame.image.load("image/mapaboutc.png")
mapaboutd_image = pygame.image.load("image/mapaboutd.png")
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
titlemulti_button = pygame.transform.scale(titlemulti_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleachieve_button = pygame.transform.scale(titleachieve_image, (display_funct.screen_width*26/320,display_funct.screen_height/9))
titlehost_button = pygame.transform.scale(titlehost_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleclient_button = pygame.transform.scale(titleclient_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

#타이틀_ON
titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlesingle_on_button = pygame.transform.scale(titlesingle_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlestory_on_button = pygame.transform.scale(titlestory_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titlemulti_on_button = pygame.transform.scale(titlemulti_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleachieve_on_button = pygame.transform.scale(titleachieve_on_image, (display_funct.screen_width*26/320,display_funct.screen_height/9))
titlehost_on_button = pygame.transform.scale(titlehost_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleclient_on_button = pygame.transform.scale(titleclient_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

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
keysetting_button = pygame.transform.scale(keysetting_image, (display_funct.screen_width*400/1600,display_funct.screen_height*300/900))

#업적
achieveoption_button = pygame.transform.scale(achieve_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
achieve_text_button = pygame.transform.scale(achieve_text, (display_funct.screen_width*400/1600,display_funct.screen_height*120/900))
card_icon_button1 = pygame.transform.scale(card_icon_image1, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button2 = pygame.transform.scale(card_icon_image2, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button3 = pygame.transform.scale(card_icon_image3, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button4 = pygame.transform.scale(card_icon_image4, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button5 = pygame.transform.scale(card_icon_image5, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button6 = pygame.transform.scale(card_icon_image6, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button7 = pygame.transform.scale(card_icon_image7, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
card_icon_button8 = pygame.transform.scale(card_icon_image8, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))

#결과창
resultwin_button = pygame.transform.scale(resultwin_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))
resultlose_button = pygame.transform.scale(resultlose_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))

#싱글플레이
singleoption_button = pygame.transform.scale(singleoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
singleplayer_button = pygame.transform.scale(singleplayer_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
singleplayer_on_button = pygame.transform.scale(singleplayer_on_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
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

uno_button = pygame.transform.scale(uno_image, (display_funct.screen_width*64/1600,display_funct.screen_height*120/900))
uno_on_button = pygame.transform.scale(uno_on_image, (display_funct.screen_width*64/1600,display_funct.screen_height*120/900))

#스토리로비
singlelobby_button = pygame.transform.scale(singlelobby_image, (display_funct.screen_width*1185/1600,display_funct.screen_height*800/900))
mapabouta_button = pygame.transform.scale(mapabouta_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
mapaboutb_button = pygame.transform.scale(mapaboutb_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
mapaboutc_button = pygame.transform.scale(mapaboutc_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
mapaboutd_button = pygame.transform.scale(mapaboutd_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
cur_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
cur_on_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
cleared_button = pygame.transform.scale(cleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
notcleared_button = pygame.transform.scale(notcleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
checkmap_button = pygame.transform.scale(checkmap_image, (display_funct.screen_width*400/1600,display_funct.screen_height*300/900))

#대충 턴 보여주는거
turn_right = pygame.image.load("image/turn_1.png")
turn_left = pygame.image.load("image/turn_2.png")
turn_right_button = pygame.transform.scale(turn_right, (display_funct.screen_width*130/1600,display_funct.screen_height*30/900))
turn_left_button = pygame.transform.scale(turn_left, (display_funct.screen_width*130/1600,display_funct.screen_height*30/900))

def image_scale():
    #타이틀
    display_funct.titlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_button = pygame.transform.scale(titleoption_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_button = pygame.transform.scale(titleexit_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlesingle_button = pygame.transform.scale(titlesingle_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlestory_button = pygame.transform.scale(titlestory_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlemulti_button = pygame.transform.scale(titlemulti_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleachieve_button = pygame.transform.scale(titleachieve_image, (display_funct.screen_width*26/320,display_funct.screen_height/9))
    display_funct.titlehost_button = pygame.transform.scale(titlehost_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleclient_button = pygame.transform.scale(titleclient_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

    #타이틀_ON
    display_funct.titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlesingle_on_button = pygame.transform.scale(titlesingle_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlestory_on_button = pygame.transform.scale(titlestory_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titlemulti_on_button = pygame.transform.scale(titlemulti_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleachieve_on_button = pygame.transform.scale(titleachieve_on_image, (display_funct.screen_width*26/320,display_funct.screen_height/9))
    display_funct.titlehost_on_button = pygame.transform.scale(titlehost_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleclient_on_button = pygame.transform.scale(titleclient_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

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
    display_funct.keysetoption_button = pygame.transform.scale(keysetoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
    display_funct.keysetting_button = pygame.transform.scale(keysetting_image, (display_funct.screen_width*400/1600,display_funct.screen_height*300/900))

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

    #업적
    display_funct.achieveoption_button = pygame.transform.scale(achieve_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
    display_funct.achieve_text_button = pygame.transform.scale(achieve_text, (display_funct.screen_width*400/1600,display_funct.screen_height*120/900))
    display_funct.card_icon_button1 = pygame.transform.scale(card_icon_image1, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button2 = pygame.transform.scale(card_icon_image2, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button3 = pygame.transform.scale(card_icon_image3, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button4 = pygame.transform.scale(card_icon_image4, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button5 = pygame.transform.scale(card_icon_image5, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button6 = pygame.transform.scale(card_icon_image6, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button7 = pygame.transform.scale(card_icon_image7, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))
    display_funct.card_icon_button8 = pygame.transform.scale(card_icon_image8, (display_funct.screen_width*90/1600,display_funct.screen_height*90/900))

    #결과창
    display_funct.resultwin_button = pygame.transform.scale(resultwin_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))
    display_funct.resultlose_button = pygame.transform.scale(resultlose_image, (display_funct.screen_width*943/1600,display_funct.screen_height*7/9))

    #싱글플레이
    display_funct.singleoption_button = pygame.transform.scale(singleoption_image, (display_funct.screen_width*505/1600,display_funct.screen_height*800/900))
    display_funct.singleplayer_button = pygame.transform.scale(singleplayer_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
    display_funct.singleplayer_on_button = pygame.transform.scale(singleplayer_on_image, (display_funct.screen_width*245/1600,display_funct.screen_height*70/900))
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
    display_funct.mapaboutd_button = pygame.transform.scale(mapaboutd_image, (display_funct.screen_width*300/1600,display_funct.screen_height*225/900))
    display_funct.cur_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.cur_on_button = pygame.transform.scale(cur_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.cleared_button = pygame.transform.scale(cleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.notcleared_button = pygame.transform.scale(notcleared_image, (display_funct.screen_width*40/1600,display_funct.screen_height*40/900))
    display_funct.checkmap_button = pygame.transform.scale(checkmap_image, (display_funct.screen_width*400/1600,display_funct.screen_height*300/900))

    display_funct.uno_button = pygame.transform.scale(uno_image, (display_funct.screen_width*64/1600,display_funct.screen_height*120/900))
    display_funct.uno_on_button = pygame.transform.scale(uno_on_image, (display_funct.screen_width*64/1600,display_funct.screen_height*120/900))

    display_funct.card_width = screen_width/12.3
    display_funct.card_height = screen_height/4.9

    display_funct.turn_right_button = pygame.transform.scale(turn_right, (display_funct.screen_width*130/1600,display_funct.screen_height*30/900))
    display_funct.turn_left_button = pygame.transform.scale(turn_left, (display_funct.screen_width*130/1600,display_funct.screen_height*30/900))

#######################################사운드#############################################
pygame.mixer.music.load("sound/background.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(mainsound*sound/100)

cardplay = pygame.mixer.Sound(os.getcwd()+"/sound/card.mp3")
menuplay = pygame.mixer.Sound(os.getcwd()+"/sound/menu.wav")
winplay = pygame.mixer.Sound(os.getcwd()+"/sound/win.wav")
loseplay = pygame.mixer.Sound(os.getcwd()+"/sound/lose.wav")
drawplay = pygame.mixer.Sound(os.getcwd()+"/sound/from_deck.wav")


menuplay.set_volume(subsound*sound/200)
cardplay.set_volume(subsound*sound/100)
winplay.set_volume(subsound*sound/100)
loseplay.set_volume(subsound*sound/100)
drawplay.set_volume(subsound*sound/100)
  
def setsound():
    cardplay.set_volume(display_funct.subsound*display_funct.sound/100)
    menuplay.set_volume(display_funct.subsound*display_funct.sound/250)
    winplay.set_volume(display_funct.subsound*display_funct.sound/100)
    loseplay.set_volume(display_funct.subsound*display_funct.sound/100)
    loseplay.set_volume(display_funct.subsound*display_funct.sound/100)
