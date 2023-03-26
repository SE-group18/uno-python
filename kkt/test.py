import pygame
import json

pygame.init()

#타이틀


# 화면 크기 및 제목 설정
screen_width, screen_height = 1280, 720

#타이틀
try:
    with open("config.txt", "r") as f:
        config = json.load(f)
    screen_width = config["screen_width"]
    screen_height = config["screen_height"]
except:
    pass




screen = pygame.display.set_mode((screen_width, screen_height))
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

    # 전체화면의 screen_width와 screen_height 구하기
    


    pygame.display.update()