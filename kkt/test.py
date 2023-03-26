import pygame
pygame.init()

#타이틀


# 화면 크기 및 제목 설정
screen_width, screen_height = 2560, 1440

#타이틀


screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("My Game")

# 배경 이미지 불러오기
"""
background = pygame. image.load("test.png");
screen.blit(background,(0,0));
"""

# 버튼 텍스트에 사용할 폰트 설정

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    display_info = pygame.display.Info()

    # 전체화면의 screen_width와 screen_height 구하기
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    print(screen_width)
    print(screen_height)
    


    pygame.display.update()