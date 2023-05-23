import threading

import pygame

# Pygame 초기화
pygame.init()

# 창 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

print(pygame.key.name(pygame.K_UP))


#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.KEYDOWN:
#            print(event.key)