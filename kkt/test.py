import pygame
pygame.init()

#이미지 파일
option_image = pygame.image.load('options.png')
button_on = pygame.image.load("mute.png")
button_off = pygame.image.load("unmute.png")
button_music = {"image_on": button_on, "image_off": button_off, "x": 200, "y": 200, "state": "off"}
anybutton = pygame.image.load("a.png")

#사운드 파일
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)

# 버튼에 사용할 색상 지정
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)

# 화면 크기 및 제목 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# 버튼 텍스트에 사용할 폰트 설정
font = pygame.font.Font(None, screen_height//12)


# 버튼 생성 함수
def create_button(x, y, width, height, text, bool):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.x, button_rect.y = x, y

    if bool==True:
        pygame.draw.rect(button_surface, BUTTON_SELECTED_COLOR, (0, 0, width, height), 1)
    else:
        pygame.draw.rect(button_surface, BUTTON_COLOR, (0, 0, width, height), 1)

    text_surface = font.render(text, True, (123, 123, 123))
    text_rect = text_surface.get_rect(center=button_rect.center)
    button_surface.blit(text_surface, text_rect)

    screen.blit(button_surface, button_rect)  # 버튼 surface를 화면 surface에 blit
    screen.blit(text_surface, text_rect)
    return button_rect  # 버튼 rect를 반환
    


# 버튼 생성
start_button = create_button(screen_width//2-screen_width/8, screen_height/3, screen_width/4, screen_height/12, "Start Game",True)
options_button = create_button(screen_width//2-screen_width/8, screen_height/2, screen_width/4, screen_height/12, "Options",False)
quit_button = create_button(screen_width//2-screen_width/8, screen_height/1.5, screen_width/4, screen_height/12, "Quit",False)

# 선택된 버튼
selected_button_list = [start_button,options_button,quit_button]
selected_button = start_button
# 게임 루프
my_address = 0
while True:
    for event in pygame.event.get():
        if my_address == 0:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_x, click_y = event.pos
                    print(event.button)
                    #Start 버튼
                    if screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/3 <= click_y <= screen_height/3 + screen_height/12:
                        pass
                    #Option 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                        screen_height/2 <= click_y <= screen_height/2 + screen_height/12:
                        my_address = 1
                            
                        
                    #Quit 버튼
                    elif screen_width//2-screen_width/8 <= click_x <= screen_width//2-screen_width/8 + screen_width/4 and \
                    screen_height/1.5 <= click_y <= screen_height/1.5 + screen_height/12:
                        pygame.quit()
                        exit()
   
        if my_address == 1:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(option_image,(screen_width/8,screen_height/8))
                screen.blit(button_music["image_"+button_music["state"]], (button_music["x"], button_music["y"]))
                screen.blit(anybutton, (500,500))
                if event.button == 1:
                    click_x, click_y = event.pos
                    if button_music["x"] <= click_x <= button_music["x"] + button_on.get_width() and \
                        button_music["y"] <= click_y <= button_music["y"] + button_on.get_height():
                        button_music["state"] = "off" if button_music["state"] == "on" else "on"
                        if button_music["state"] == "on":
                            pygame.mixer.music.set_volume(0.25)
                        elif button_music["state"] == "off":
                            pygame.mixer.music.set_volume(0)
                    elif 500 <= click_x <= 530 and 500 <= click_y <= 530:
                        screen_width = 1200
                        screen_height = 900
                        screen = pygame.display.set_mode((screen_width, screen_height))
                    

   

    pygame.display.update()