import game_classes
import pygame
from pygame.locals import *
import display_funct

pygame.init()

option = False
setting = False
title = True
sound_option = "on"
color_option = "off"
i = 0
full = False

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
size_o = screen_width, screen_height = 1600, 900
scale_size = size_o
scale_card_size = 0

# scaling factors that are initially set the scale value of 1 (native to
# 1600x900 pixel resolution)
scale_x = 1
scale_y = 1

# defining the global pygame screen value to be used within PY-UNO
screen = pygame.display.set_mode(size_o, HWSURFACE | DOUBLEBUF)
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
    (x_o, y_o) = size_o
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
            (screen_width - card_width) // 2,
            (screen_height - card_height) // 2)

        # blit top card of board onto center screen
        scale_card_blit(top_card.card_data, top_card.rect)


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

    # grab a list of all players excluding the currenly playing one
    players_temp = players_other[:]  # O(n)
    players_temp.remove(player_dat)  # O(n)

    # draw all players (excluding the currently playing player) hands facedown
    # an orderly fashion on the screen
    redraw_hand_nonvisble_loop(players_temp)  # O(m*n)

    # draw the top card on the board
    draw_top_stack_card(board)  # O(1)

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

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - \
        (200 * (len(winners) - 1) + card_width) // 2

    target_index = 0
    for player in winners:  # O(n)
        player_num = str(player.name[7])
        card_disp = game_classes.Card(
            "red", "small_cards/green_" + player_num + ".png", None)
        card_disp.rect = def_rect
        card_disp.rect = card_disp.rect.move(start_pos, 300)
        card_disp.rect = card_disp.rect.move(200 * target_index, 0)
        scale_card_blit(card_disp.card_data, card_disp.rect)

        target_index += 1

    # refresh the screen
    pygame.display.flip()

################################################## ESC 화면 ############################################################
def esc_screen():
    selected_button = "resume"
    while display_funct.option == True:
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
                        
                    elif selected_button == "setting":
                        display_funct.setting = True

                    elif selected_button == "exit":
                        pygame.display.quit()
                        pygame.quit()
                        exit()
                        

            pygame.display.update()
        
############################################### 옵션 화면 #############################################
def setting_screen():
    selected_option = "sound"
    while display_funct.setting == True:
        green = (0,0,0)
        screen.fill(green)
        screen.blit(option_1, (display_funct.screen_width*1095/3200,display_funct.screen_height*50/900))
        screen.blit(small_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*370/900))
        screen.blit(med_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*440/900))
        screen.blit(full_button, (display_funct.screen_width*1605/3200,display_funct.screen_height*510/900))
        screen.blit(check_button, (display_funct.screen_width*775/1600,display_funct.screen_height*690/900))

        #사운드
        if selected_option == "sound" and display_funct.sound_option == "on":
            screen.blit(checkon_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*290/900))
        elif selected_option == "sound" and display_funct.sound_option == "off":
            screen.blit(check_on_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*290/900))
        elif display_funct.sound_option == "on":
            screen.blit(checkon_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*290/900))
        elif display_funct.sound_option == "off":
            screen.blit(check_button, (display_funct.screen_width*1695/3200,display_funct.screen_height*290/900))
        
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

        #Close
        if selected_option == "close":
            screen.blit(check_on_button, (display_funct.screen_width*775/1600,display_funct.screen_height*690/900))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_option == "sound":
                        pass
                    elif selected_option == "small":
                        selected_option = "sound"
                    elif selected_option == "med":
                        selected_option = "small"
                    elif selected_option == "full":
                        selected_option = "med"
                    elif selected_option == "color":
                        selected_option = "full"
                    elif selected_option == "close":
                        selected_option = "color"
                        
                elif event.key == pygame.K_DOWN:
                    if selected_option == "sound":
                        selected_option = "small"
                    elif selected_option == "small":
                        selected_option = "med"
                    elif selected_option == "med":
                        selected_option = "full"
                    elif selected_option == "full":
                        selected_option = "color"
                    elif selected_option == "color":
                        selected_option = "close"
                    elif selected_option == "close":
                        pass

                elif event.key == pygame.K_SPACE:
                    if selected_option == "sound":
                        if display_funct.sound_option == "on":
                            display_funct.sound_option = "off"
                        elif display_funct.sound_option == "off":
                            display_funct.sound_option = "on"

                    if selected_option == "small":
                        width = 1280
                        height = 720
                        if display_funct.full == True:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            display_funct.full = False
                        elif width == screen_width and height == screen_height:
                            pass
                        else:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                    
                    if selected_option == "med":
                        width = 1600
                        height = 900
                        if display_funct.full == True:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                            display_funct.full = False
                        elif width == screen_width and height == screen_height:
                            pass
                        else:
                            display_funct.screen_width = width 
                            display_funct.screen_height = height 
                            image_scale()
                            pygame.display.set_mode((screen_width,screen_height))
                    
                    if selected_option == "full":                             
                        pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
                        display_info = pygame.display.Info()
                        width = display_info.current_w
                        height = display_info.current_h
                        display_funct.screen_width = width 
                        display_funct.screen_height = height 
                        image_scale()
                        display_funct.full = True

                    if selected_option == "color":
                        if display_funct.color_option == "on":
                            display_funct.color_option = "off"
                        elif display_funct.color_option == "off":
                            display_funct.color_option = "on"


                    elif selected_option == "close":
                        display_funct.setting = False
        pygame.display.flip()

################################################# 시작 화면 ################################################
# 게임 루프
def title_screen():
    selected_button = "start"
    while display_funct.title: 
        if display_funct.setting == True:
            setting_screen() #그전 버튼 안없어지는 현상 발생
            continue

        else:
            screen.fill(black)
            # 버튼 생성
            screen.blit(titlestart_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/2))
            screen.blit(titleoption_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.5))
            screen.blit(titleexit_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/1.2))
            
            # 선택된 버튼
            if selected_button == "start":
                screen.blit(titlestart_on_button,(display_funct.screen_width//2-display_funct.screen_width/8, display_funct.screen_height/2))
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
                        if selected_button == "start":
                            selected_button = "exit"
                                                
                        elif selected_button == "option":
                            selected_button = "start"
                        elif selected_button == "exit":
                            selected_button = "option"

                    elif event.key == pygame.K_DOWN:
                        # 아래쪽 방향키 클릭 시
                        if selected_button == "start":
                            selected_button = "option"
                        elif selected_button == "option":
                            selected_button = "exit"
                        else:
                            selected_button = "start"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE: #우측키 스페이스 엔터
                        if selected_button == "start":
                            display_funct.title = False

                        elif selected_button == "option":
                            # Options 버튼 클릭 시 실행할 코드
                            display_funct.setting = True

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


    

################################### 이미지 파일 ###############################################
#타이틀
titlestart_image = pygame.image.load("titlestart.png")
titleoption_image = pygame.image.load("titleoption.png")
titleexit_image = pygame.image.load("titleexit.png")

#타이틀_ON
titlestart_on_image = pygame.image.load("titlestart_on.png")
titleoption_on_image = pygame.image.load("titleoption_on.png")
titleexit_on_image = pygame.image.load("titleexit_on.png")

#ESC
setting_image = pygame.image.load("setting.png")
title_image = pygame.image.load("title.png")
resume_image = pygame.image.load("resume.png")
exit_image = pygame.image.load("exit.png")

#ESC_ON
resume_on_image = pygame.image.load("resume_on.png")
title_on_image = pygame.image.load("title_on.png")
setting_on_image = pygame.image.load("setting_on.png")
exit_on_image = pygame.image.load("exit_on.png")

#옵션
option_image = pygame.image.load("option.png")
soundon_image = pygame.image.load("soundon.png")
small_image = pygame.image.load("small.png")
med_image = pygame.image.load("med.png")
full_image = pygame.image.load("full.png")
check_image = pygame.image.load("check.png")
checkon_image = pygame.image.load("checkon.png")

#옵션_ON
soundon_on_image = pygame.image.load("soundon_on.png")
full_on_image = pygame.image.load("full_on.png")
check_on_image = pygame.image.load("check_on.png")
checkon_on_image = pygame.image.load("checkon_on.png")
small_on_image = pygame.image.load("small_on.png")
med_on_image = pygame.image.load("med_on.png")



#해상도 파일
#타이틀
titlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleoption_button = pygame.transform.scale(titleoption_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleexit_button = pygame.transform.scale(titleexit_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

#타이틀_ON
titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))


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
soundon_button = pygame.transform.scale(soundon_image, (display_funct.screen_width/32,display_funct.screen_height/18))
small_button = pygame.transform.scale(small_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
med_button = pygame.transform.scale(med_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
full_button = pygame.transform.scale(full_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
check_button = pygame.transform.scale(check_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
checkon_button = pygame.transform.scale(checkon_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))


#옵션_ON
soundon_on_button = pygame.transform.scale(soundon_on_image, (display_funct.screen_width/32,display_funct.screen_height/18))
full_on_button = pygame.transform.scale(full_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
check_on_button = pygame.transform.scale(check_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
checkon_on_button = pygame.transform.scale(checkon_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
small_on_button = pygame.transform.scale(small_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
med_on_button = pygame.transform.scale(med_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))



def image_scale():
    #타이틀
    display_funct.titlestart_button = pygame.transform.scale(titlestart_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_button = pygame.transform.scale(titleoption_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_button = pygame.transform.scale(titleexit_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

    #타이틀_ON
    display_funct.titlestart_on_button = pygame.transform.scale(titlestart_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleoption_on_button = pygame.transform.scale(titleoption_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))
    display_funct.titleexit_on_button = pygame.transform.scale(titleexit_on_image, (display_funct.screen_width*7/32,display_funct.screen_height/9))

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
    

    #옵션_ON
    display_funct.soundon_on_button = pygame.transform.scale(soundon_on_image, (display_funct.screen_width/32,display_funct.screen_height/18))
    display_funct.soundon_button = pygame.transform.scale(soundon_image, (display_funct.screen_width/32,display_funct.screen_height/18))
    display_funct.full_on_button = pygame.transform.scale(full_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.check_on_button = pygame.transform.scale(check_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.checkon_on_button = pygame.transform.scale(checkon_on_image, (display_funct.screen_width*13/320,display_funct.screen_height/18))
    display_funct.small_on_button = pygame.transform.scale(small_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))
    display_funct.med_on_button = pygame.transform.scale(med_on_image, (display_funct.screen_width*7/64,display_funct.screen_height/18))