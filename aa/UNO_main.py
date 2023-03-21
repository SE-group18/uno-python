import pygame
import button

pygame.init()

# 버튼에 사용할 색상 지정
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)

# 버튼 두께
BUTTON_THICK=10

# 화면 크기 및 제목 설정
screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# 배경 이미지 불러오기
"""
background = pygame. image.load("test.png");
screen.blit(background,(0,0));
"""

start_img = pygame.image.load('start.png').convert_alpha()
option_img = pygame.image.load('option.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()


# 버튼 텍스트에 사용할 폰트 설정
font = pygame.font.Font(None, screen_height//12)


# 버튼 생성 함수
def create_button(x, y, width, height, text, bool):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.x, button_rect.y = x, y

    if bool==True:
        pygame.draw.rect(button_surface, BUTTON_SELECTED_COLOR, (0, 0, width, height), BUTTON_THICK)
    else:
        pygame.draw.rect(button_surface, BUTTON_COLOR, (0, 0, width, height), BUTTON_THICK)

    text_surface = font.render(text, True, (123, 123, 123))
    text_rect = text_surface.get_rect(center=button_rect.center)
    button_surface.blit(text_surface, text_rect)

    screen.blit(button_surface, button_rect)  # 버튼 surface를 화면 surface에 blit
    screen.blit(text_surface, text_rect)
    return button_rect  # 버튼 rect를 반환
    

start_button = button.Button(screen_width//2-screen_width/8, screen_height/2,start_img, screen_width/1100)
options_button = button.Button(screen_width//2-screen_width/8, screen_height/1.5, option_img, screen_width/1100)
quit_button = button.Button(screen_width//2-screen_width/8, screen_height/1.2, exit_img, screen_width/1100)

# 선택된 버튼
selected_button_list = [start_button,options_button,quit_button]
selected_button = start_button

# 버튼 색변경
def change_color(index1,index2):
    pygame.draw.rect(screen, BUTTON_COLOR, selected_button_list[index1], BUTTON_THICK)
    pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, selected_button_list[index2], BUTTON_THICK)
        


# 게임 루프
while True:
    screen.fill(BUTTON_COLOR)

    if start_button.draw(screen):
        print("START")
    if options_button.draw(screen):
        print("option")
    if quit_button.draw(screen):
        print("exit")
        pygame.quit()
        exit()   
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
   



    

    pygame.display.update()