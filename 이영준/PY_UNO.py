from deck_gen import gen_rand_deck
import display_funct
import game_AI
import game_classes
import game_logic
import pygame
pygame.init()

"""
-이영준- 
main화면 연동 : mainscreen 변수를 true false로 변경함으로써
화면이 바뀌도록 만들어 놓음

만약 option 화면을 따로 만든다면 위와 같이 if문으로 화면을 전환하는것도
괜찮다고 생각합니다.
"""

mainscreen=True

# 버튼에 사용할 색상 지정
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)


screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")


font = pygame.font.Font(None, screen_height//12)
# 버튼 생성 함수
def create_button(x, y, width, height, text):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.x, button_rect.y = x, y

    pygame.draw.rect(button_surface, (100,100,100), (0, 0, width, height), 1)

    text_surface = font.render(text, True, (123, 123, 123))
    text_rect = text_surface.get_rect(center=button_rect.center)
    button_surface.blit(text_surface, text_rect)

    screen.blit(button_surface, button_rect)  # 버튼 surface를 화면 surface에 blit
    screen.blit(text_surface, text_rect)

    return button_rect  # 버튼 rect를 반환


# 버튼 생성
start_button = create_button(screen_width//2-screen_width/8, screen_height/2, screen_width/4, screen_height/12, "Start Game")
options_button = create_button(screen_width//2-screen_width/8, screen_height/1.5, screen_width/4, screen_height/12, "Options")
quit_button = create_button(screen_width//2-screen_width/8, screen_height/1.2, screen_width/4, screen_height/12, "Quit")

# 선택된 버튼
selected_button_list = [start_button,options_button,quit_button]
selected_button = start_button

def change_color(index1,index2):
    pygame.draw.rect(screen, BUTTON_COLOR, selected_button_list[index1], 1)
    pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, selected_button_list[index2], 1)


# loop for allowing multiple games to be restarted
while True:

    if mainscreen==True:
        for event in pygame.event.get():

    

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 위쪽 방향키 클릭 시
                    if selected_button == start_button:
                        selected_button = quit_button
                        change_color(0,-1)
                                            
                    elif selected_button == options_button:
                        selected_button = start_button
                        change_color(1,0)
                    else:
                        selected_button = options_button
                        change_color(2,1)
                elif event.key == pygame.K_DOWN:
                    # 아래쪽 방향키 클릭 시
                    if selected_button == start_button:
                        selected_button = options_button
                        change_color(0,1)
                    elif selected_button == options_button:
                        selected_button = quit_button
                        change_color(1,2)
                    else:
                        selected_button = start_button
                        change_color(2,0)
                elif event.key == pygame.K_RETURN:
                    # 엔터키 클릭 시
                    if selected_button == start_button:
                        # Start Game 버튼 클릭 시 실행할 코드
                        print("Start Game")
                        mainscreen=False
                    elif selected_button == options_button:
                        # Options 버튼 클릭 시 실행할 코드
                        print("Options")
                    elif selected_button == quit_button:
                        # Quit 버튼 클릭 시 실행할 코드
                        pygame.quit()
                        exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭시
                if event.button == 1:
                    click_x, click_y = event.pos
                    
                    #Start 버튼
                    if  screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/2 <= click_y <= screen_height/2 + screen_height/12:
                        print('START')
                        mainscreen=False
                        pass
                        #Option 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:  
                        print('OPTION')
                        pass
                        
                            
                        #Quit 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/1.2 <= click_y <= screen_height/1.2 + screen_height/12:
                        print('QUIT')
                        pygame.quit()
                        exit()
        
                   

        
        
    
    

        pygame.display.update()


    else:

        # initilizing the board to be used within the game
        board1 = game_classes.Board("board1")

        # initilizing a deck to be used within the game (3 copies are added to
        # each other)
        deck1 = gen_rand_deck("deck1", 0)

        # defining a 7 player uno game
        player1 = game_classes.Player("player_1")
        player1.grab_cards(deck1, 7)

        player2AI = game_AI.make_AI_basic(deck1, "player_2AI", 7)
        player3AI = game_AI.make_AI_basic(deck1, "player_3AI", 7)
        player4AI = game_AI.make_AI_basic(deck1, "player_4AI", 7)
        player5AI = game_AI.make_AI_basic(deck1, "player_5AI", 7)
        player6AI = game_AI.make_AI_basic(deck1, "player_6AI", 7)
        player7AI = game_AI.make_AI_basic(deck1, "player_7AI", 7)

        display_funct.redraw_hand_visble(player1, None)


        # enters into playing the game
        game_logic.game_loop(board1, deck1, [player1, player2AI, player3AI, player4AI,
                            player5AI, player6AI, player7AI])
