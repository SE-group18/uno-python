import pygame
pygame.init()

#타이틀
start_image = pygame.image.load("start.png")

#타이틀_ON
start_on_image = pygame.image.load("start_on.png")

# 화면 크기 및 제목 설정
screen_width, screen_height = 1600, 900

#타이틀
start_button = pygame.transform.scale(start_image, (screen_width*7/32,screen_height/9))

#타이틀_ON
start_on_button = pygame.transform.scale(start_on_image, (screen_width*7/32,screen_height/9))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# 배경 이미지 불러오기
"""
background = pygame. image.load("test.png");
screen.blit(background,(0,0));
"""

# 버튼 텍스트에 사용할 폰트 설정
selected = ""
# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = "start"
    
    print(selected)
    if selected == "start":
        screen.blit(start_on_button,(screen_width//2-screen_width/8,screen_height/2))
    else:
        screen.blit(start_button,(screen_width//2-screen_width/8,screen_height/2))

    pygame.display.update()