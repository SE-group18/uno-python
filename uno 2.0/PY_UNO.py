from deck_gen import gen_rand_deck
import display_funct
import game_AI
import game_classes
import game_logic
import pygame

pygame.display.set_caption("UNO!")
# loop for allowing multiple games to be restarted
def main():
    display_funct.title = True
    display_funct.setting = False
    display_funct.option = False
    display_funct.instorymode = False
    game_logic.uno_clicked = False
    display_funct.achieve_title = False
    
    while True:
        # initilizing the board to be used within the game
        display_funct.title_screen()

if __name__ == "__main__":
    main()