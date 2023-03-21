import pygame

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Options")

# 버튼 이미지
button_on = pygame.image.load("mute.png")
button_off = pygame.image.load("unmute.png")

# 버튼 객체
button_music = {"image_on": button_on, "image_off": button_off, "x": 200, "y": 200, "state": "off"}
button_sound = {"image_on": button_on, "image_off": button_off, "x": 200, "y": 300, "state": "on"}

# 클릭한 좌표
click_x = None
click_y = None

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 왼쪽 버튼 클릭 처리
            if event.button == 1:
                click_x, click_y = event.pos
                if button_music["x"] <= click_x <= button_music["x"] + button_on.get_width() and \
                    button_music["y"] <= click_y <= button_music["y"] + button_on.get_height():
                    button_music["state"] = "off" if button_music["state"] == "on" else "on"
                elif button_sound["x"] <= click_x <= button_sound["x"] + button_on.get_width() and \
                    button_sound["y"] <= click_y <= button_sound["y"] + button_on.get_height():
                    button_sound["state"] = "off" if button_sound["state"] == "on" else "on"

    # 화면 지우기
    screen.fill((255, 255, 255))

    # 버튼 그리기
    screen.blit(button_music["image_"+button_music["state"]], (button_music["x"], button_music["y"]))

    # 화면 업데이트
    pygame.display.update()