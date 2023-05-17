import pygame

# pygame 초기화
pygame.init()

# 화면 생성
screen = pygame.display.set_mode((800, 600))

# 이미지 로드
image1 = pygame.image.load("title.png")
image2 = pygame.image.load("resume_on.png")

# 이미지의 Rect 객체 생성
rect = image1.get_rect()
rect.topleft = (100, 100)  # 이미지의 위치를 (100, 100)으로 설정

# 이미지를 화면에 출력
screen.blit(image1, rect)
pygame.display.flip()

# 게임 루프
while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # 현재 마우스 위치를 가져옴
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 마우스가 이미지 위에 있을 때 이미지를 변경
    if rect.collidepoint(mouse_x, mouse_y):
        screen.blit(image2, rect)
    # 마우스가 이미지 밖으로 나갈 때 이미지를 다시 원래대로 변경
    else:
        screen.blit(image1, rect)

    pygame.display.flip()