import pygame

pygame.init()

# 화면 설정
display_width = 480
display_height = 640
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("timer")

# 폰트 설정
game_font = pygame.font.Font(None, 40)

# FPS
clock = pygame.time.Clock()

# 시간 정보
total_time = 10
start_ticks = pygame.time.get_ticks()

# 이벤트 루프
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    # 타이머
    timer = game_font.render("timer: " + str(int(total_time - elapsed_time)), True, (255,255,255))

    #경과 시간 표시
    screen.fill((0,0,0))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False

    pygame.display.update()

pygame.quit()

