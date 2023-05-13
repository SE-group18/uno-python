
import card_logic
import display_funct
import game_control
import Main_Decision_Tree
import pygame
import game_logic
from pygame.locals import *
import PY_UNO
import os
import random

pygame.init()
game_font = pygame.font.Font(None, 40)
total_time = 15
start_ticks = 0
elapsed_time = 0
paused_time = 0
paused = False
# global list containing the winners in placement order
global winners
winners = []
uno_clicked = False
uno_stack = 0

def update_hatval(player, target, hate_increase=1):
    """
    Function that updates the hatval of a player in refrence to a player.

    Eg: a player (player A) plays a skip turn card on a target (player B)
    thus player B's hatval of player A goes up. The higher the hatval the
    more likely that player B will prioritize targeting player A over other
    logical plays.

    O(1) runtime
    """
    try:
        target.hatval[player] += hate_increase
    except KeyError:
        target.hatval[player] = hate_increase


def degrade_hatval(player):
    """
    Funciton that de-iterates the current players hatval of all other players
    by 1. Essentially preventing hatevals going extremely high, and making very
    mean AIs.

    O(n) runtime where n is the number of hated players number of
    (keys of players hatval).
    """
    for hated_player in player.hatval.keys():
        if player.hatval[hated_player] > 0:
            player.hatval[hated_player] -= 1


def increment_card_old_vals(player):
    """
    Function for AI use that updates the old values of their hands cards.
    Each turn the all of the current turn AI's cards old values goes up by one.

    O(n) runtime where n is the size of the players hand
    """
    for card in player.hand:
        card.old_val += 1


def compute_turn(players, turn, turn_iterator):
    """
    Function that handles PY-UNO turn iterations for any amount of players.

    O(1) runtime
    """
    turn = turn + turn_iterator
    # catch to reloop over players array
    if turn < 0:
        turn = len(players) - 1
    elif turn >= len(players):
        turn = 0
    print("Turn iterator: ", turn_iterator)
    print("__TURN_END__ \n")

    return turn


def check_update(board, allowed_card_list, selected, player, players, update):
    """
    Checks to see during a human players turn if updating the screen is
    nessicarry. This helps reduce redundant updates and keeps the screen
    refreshing crisp.

    Worst case:
    O(m*n) runtime where m is the amount of players to be drawn and
    n is the size of the players hand. Since both of these sizes should be
    relatively small optimizing was considered negligible.
    """
    if update:
        update = False
        if selected is None:
            display_funct.redraw_screen(
                [(player, None)], board, players)
        else:
            display_funct.redraw_screen(
                [(player, allowed_card_list[selected])], board, players)
    return update


def check_winners(player):
    """
    Checks to see if a player has met the conditions of winning a round
    (having no more cards in hand). If so the player is appened onto the global
    list winners.

    O(1) runtime
    """
    global winners
    if player.hand == []:  # conditions for winning!
        print(player.name, "won and leaves this round!")
        winners.append(player)


def check_game_done(players, turn_tot):
    """
    Checks to see if the PY-UNO game is over (only one player left with cards).
    If so the last player with cards is appened to the winners list and then
    the game displays the winners with placeholder green cards (with a numeric
    value the same as their name number) in win order. The left most card
    displayed is first place while the rightmost is last. Winners are also
    printed out within terminal (printed in winning placement order).

    Args:
        players: a game_classes.py player that will iterate through allowing
        for turns with each player.

    O(n) runtime where n is the length of winners. However this is the end game
    state so this is likely no a problem.
    """
    global winners

    print(display_funct.player_total)
    
    if display_funct.fair == 0:
        display_funct.fair = True

    else:
        display_funct.fair = 0

    if len(players) <= display_funct.player_total-1:
        print("\n\ngame done!!!!!")
        # adding last place
        winners.append(players[0])

        place = 1
        print("displaying winners in order:")
        for player in winners:
            print(place, player.name)
            place += 1

        display_funct.draw_winners(winners, turn_tot)
        winning = True
        while winning:  # wait till the player exits out of the game
            for event in pygame.event.get():
                (select_L, select_R, select_UP, select_DOWN, select_SPACE) = game_control.get_keypress(event)

                if select_UP:
                    # clear winners for next game
                    winners = []
                    if display_funct.instorymode:
                        game_logic.uno_clicked = False
                        display_funct.story_screen()
                    else:
                        display_funct.title = True
                        PY_UNO.main()

    return False

who = ""

def extern_AI_player_turn(board, deck, player, players, turn):
    pygame.time.delay(800)

    increment_card_old_vals(player)  # O(n)

    Main_Decision_Tree.travel_Main_Decision_Tree(board, deck, player,
                                                 players, player.Main_Decision_Tree.Dec_Tree)
    degrade_hatval(player)  # O(n)
    display_funct.redraw_screen([(players[0], None)], board, players)

    if len(player.hand) == 1:
        playing = True
        while playing:
            display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == display_funct.space:
                        playing = False
            pygame.display.flip()

    display_funct.redraw_screen([(players[0], None)], board, players)

    pygame.time.delay(200)



def extern_player_turn(board, deck, player, players, turn):
    drop_again = True
    game_logic.start_ticks=pygame.time.get_ticks()
    game_logic.paused_time = 0
    display_funct.cont3 = 0
    while drop_again:
        turn_done = False
        selected = None
        grab = False
        if display_funct.wildplayed == True:
            game_logic.start_ticks=pygame.time.get_ticks()
            game_logic.paused_time = 0
            display_funct.wildplayed = False

        display_funct.cont3 += 1

        # redraw display at start of human turn
        display_funct.redraw_screen([(player, None)], board, players)

        # grab the list of allowed_cards cards
        allowed_card_list = card_logic.card_allowed(board, player)
        # if no cards can be played end turn
        if len(allowed_card_list) == 0:
            display_funct.drawplay.play()
            player.grab_card(deck)
            display_funct.redraw_screen([(players[0], None)], board, players)
            turn = compute_turn(players, turn, board.turn_iterator)
            return (player, turn)

        while not turn_done:
            (update, selected, turn_done, grab) = intern_player_turn(
                board, deck, player,players, allowed_card_list, selected)
        
            check_winners(player)

            update = check_update(board, allowed_card_list, selected,
                                  player, players, update)


        # returns false unless a drop_again type card is played
        if (grab==True):
            break
        else:
            drop_again = card_logic.card_played_type(board, deck,
                                                 player, players)
        
        if drop_again == True:
            display_funct.wildplayed = True

        if display_funct.cont3 >= 4:
            display_funct.cont3_true = True

        if len(player.hand) == 1:
            display_funct.redraw_screen([(player, None)], board, players)
            playing_1 = True
            while playing_1:
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == display_funct.space:
                            playing_1 = False
                            
                pygame.display.flip()

        display_funct.redraw_screen([(player, None)], board, players)

    return (player, turn)


def intern_player_turn(board, deck, player,players, allowed_card_list, selected):

    update = False
    grab = False
    game_logic.elapsed_time = (pygame.time.get_ticks() - game_logic.start_ticks) / 1000
    time = int(total_time - game_logic.elapsed_time + game_logic.paused_time)
    timer = game_font.render("timer: " + str(time), True, (255,255,255))

    if allowed_card_list == []:
        print("bug")
        player.grab_card(deck)
        selected = None
        update = True
        turn_done = True
        return (update, selected, turn_done, grab)

    while not update:
        #무한 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        if display_funct.option == True:
            pause_time = pygame.time.get_ticks()
            display_funct.esc_screen()
            if game_logic.paused == True:
                pausing_time = pygame.time.get_ticks()
                game_logic.paused = False
            game_logic.paused_time = game_logic.paused_time + (pausing_time - pause_time) / 1000

            turn_done = False
            update = True
            return(update, selected, turn_done, grab)
            
        else:
            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
            display_funct.screen.blit(timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))
            pygame.display.flip()

            key_pressed = pygame.key.get_pressed()
            if key_pressed[display_funct.esc]:
                game_logic.paused = True
                display_funct.option = True

            if time <= 0:
                display_funct.drawplay.play()
                player.grab_card(deck)
                turn_done=True
                update=True
                return(update, selected, turn_done, grab)
            
            (update, selected, turn_done, grab, space) = game_control.player_LR_selection_hand(
                player, selected, board, allowed_card_list)
            
            
            
            if(grab):
                display_funct.drawplay.play()
                player.grab_card(deck)

        

        return (update, selected, turn_done, grab)


def game_loop(board, deck, players):
    """
    Main logic and turn while loop that controlls the game.

    Args:
        board: a game_classes.py board class in which the cards within the game
        will be played on.

        deck: a game_classes.py deck class to be used as the deck to have cards
        drawn from.

        players: a game_classes.py player that will iterate through allowing
        for turns with each player.
    """
    for i in players:
        display_funct.player_total += 1

    board.turn_iterator = 1
    turn = 0
    turn_tot = 0
    drop_again = False
    board.update_Board(deck.grab_card())
    while True:
        player = players[turn]
        turn_tot += 1
        print("Turn number:", turn_tot)
        print("PLAYER: ", player.name, "TURN")

        if player.skip:
            if player.AI:
                increment_card_old_vals(player)

            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            extern_AI_player_turn(board, deck, player, players, turn)

        else:            # handle for a human player
            (update, turn_done) = extern_player_turn(board, deck,
                                                     player, players, turn)
        # check if the player won this round and properly remove them from the
        # game. Also check if the game is done "only one player left".
        if player in winners:
            players.remove(player)
            restart_bool = check_game_done(players, turn_tot)

            # leaves this instance of the game logic loop back to PY-UNO start
            # in which a new game is started
            if restart_bool:
                return

        # iterate the turn
        turn = compute_turn(players, turn, board.turn_iterator)

#######################################사운드#############################################
mainmusic = pygame.mixer.Sound(os.getcwd()+"/sound/background.mp3")
mainmusic.set_volume(0.25)


#C지역 게임 모드
def game_loop_C(board, deck, players):
    """
    C지역 게임 모드입니다.
    
    """
    for i in players:
        display_funct.player_total += 1
    board.turn_iterator = 1
    turn = 0
    turn_tot = 0
    drop_again = False
    board.update_Board(deck.grab_card())
   
   
    while True:  
        num=0
        player = players[turn]
        turn_tot += 1
        print("Turn number:", turn_tot)
        print("PLAYER: ", player.name, "TURN")

        randcolor=['y','r','b','g']
        randcolor1=['yellow','red','blue','green']
        card_type = ["picker", "skip", "reverse", "0",
                 "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        card_type1 = ["p", "s", "r", "0",
                 "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in card_type:
            if(board.card_stack[-1].type==i):
                TYPE=card_type1[card_type.index(i)]


        
    #새로 추가 부분
        if(turn_tot%5==0 and turn_tot!=0):
            pygame.time.delay(1000)
            
            
            seednum=random.randrange(1,1000)
            
            random.seed(seednum)
            index=random.randrange(0,4)
            board.color=randcolor[index]
            
            asdf="small_cards/" + randcolor1[index] +"_"+ TYPE + ".png"
            board.card_stack[-1].card_data=pygame.image.load(asdf)

      
            print("변경된 색깔 :"+board.color+" 변경된 타입 :"+board.type) 
            display_funct.redraw_screen([(players[0], None)], board, players)
            pygame.time.delay(1000)

        if player.skip:
            if player.AI:
                increment_card_old_vals(player)

            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            extern_AI_player_turn(board, deck, player, players, turn)
            

        else:            # handle for a human player
            (update, turn_done) = extern_player_turn(board, deck,
                                                     player, players, turn)
            

        # check if the player won this round and properly remove them from the
        # game. Also check if the game is done "only one player left".
        if player in winners:
            players.remove(player)
            restart_bool = check_game_done(players)

            # leaves this instance of the game logic loop back to PY-UNO start
            # in which a new game is started
            if restart_bool:
                return

        # iterate the turn
        turn = compute_turn(players, turn, board.turn_iterator)

