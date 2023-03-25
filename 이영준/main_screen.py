<<<<<<< HEAD
import pygame
pygame.init()

# 버튼에 사용할 색상 지정
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)

# 화면 크기 및 제목 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")
screen.fill((128,255,0))

# 배경 이미지 불러오기
"""
background = pygame. image.load("test.png");
screen.blit(background,(0,0));
"""

# 버튼 텍스트에 사용할 폰트 설정
font = pygame.font.Font(None, screen_height//12)


# 버튼 생성 함수
def create_button(x, y, width, height, text):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.x, button_rect.y = x, y

    pygame.draw.rect(button_surface, BUTTON_COLOR, (0, 0, width, height), 2)

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

# 버튼 색변경
def change_color(index1,index2):
    pygame.draw.rect(screen, BUTTON_COLOR, selected_button_list[index1], 2)
    pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, selected_button_list[index2], 2)


# 게임 루프
while True:
   
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
                elif selected_button == options_button:
                    # Options 버튼 클릭 시 실행할 코드
                    print("Options")
                elif selected_button == quit_button:
                    # Quit 버튼 클릭 시 실행할 코드
                    pygame.quit()
                    exit()
        
        elif event.type == pygame.MOUSEBUTTONUP: #마우스 클릭시  
            if event.button == 1:
                click_x, click_y = event.pos
                
                #Start 버튼
                if  screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                screen_height/2 <= click_y <= screen_height/2 + screen_height/12:
                    print('START')
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
    
                   

        
        
    
    

=======
import pygame
pygame.init()

# 버튼에 사용할 색상 지정
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)

# 화면 크기 및 제목 설정
screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# 배경 이미지 불러오기
"""
background = pygame. image.load("test.png");
screen.blit(background,(0,0));
"""

# 버튼 텍스트에 사용할 폰트 설정
font = pygame.font.Font(None, screen_height//12)


# 버튼 생성 함수
def create_button(x, y, width, height, text):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.x, button_rect.y = x, y

    pygame.draw.rect(button_surface, BUTTON_COLOR, (0, 0, width, height), 1)

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

# 버튼 색변경
def change_color(index1,index2):
    pygame.draw.rect(screen, BUTTON_COLOR, selected_button_list[index1], 1)
    pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, selected_button_list[index2], 1)


# 게임 루프
while True:
    
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
    
                   

        
        
    
    

>>>>>>> 7b35cba4065a828f7826011cd71b856b59a5eb68
    pygame.display.update()