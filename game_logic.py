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
import socket
import pickle
import game_classes
import asyncio
import threading
import deck_gen
from sys import exit


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
winners_multi = []
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

def check_winners_multi(player, players):
    """
    Checks to see if a player has met the conditions of winning a round
    (having no more cards in hand). If so the player is appened onto the global
    list winners.

    O(1) runtime
    """
    global winners
    if player.name[8] == 'C':
        if player.hand == []:  # conditions for winning!
            print(player.name, "won and leaves this round!")
            winners.append(players[0])

    if player.name[8] == 'H':
        if player.hand == []:  # conditions for winning!
            player.name = 'Player1 Host'
            print(player.name, "won and leaves this round!")
            winners.append(players[0])

    else:
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

    try:
        display_funct.client_socket.close()
    except:
        pass
    try:
        display_funct.server_socket.close()
    except:
        pass

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
                        display_funct.story_screen()
                    else:
                        display_funct.title = True
                        PY_UNO.main()

    return False

who = ""

def extern_AI_player_turn(board, deck, player, players, turn):
    display_funct.wait(500000)
    stack_uno=0
    increment_card_old_vals(player)  # O(n)

    Main_Decision_Tree.travel_Main_Decision_Tree(board, deck, player,
                                                 players, player.Main_Decision_Tree.Dec_Tree)
    degrade_hatval(player)  # O(n)
    display_funct.redraw_screen([(players[0], None)], board, players)
    display_funct.wait(1000000)
#주석

    display_funct.redraw_screen([(players[0], None)], board, players)

    display_funct.wait(200)



def extern_player_turn(board, deck, player, players, turn):
    drop_again = True
    game_logic.start_ticks=pygame.time.get_ticks()
    game_logic.paused_time = 0
    display_funct.cont3 = 0
    stack_uno=0
    while drop_again:
        turn_done = False
        selected = None
        grab = False
        if display_funct.wildplayed == True:
            game_logic.start_ticks=pygame.time.get_ticks()
            game_logic.paused_time = 0
            display_funct.wildplayed = False

        for a in player.hand:
            if a.type == "d" or a.type == "a" or a.type == "c" or a.type == "p" or a.type == "s" or a.type == "r" or a.type == "k":
                display_funct.fair += 1

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
#주석
        if len(player.hand) == 1:
            
            test= False
            display_funct.redraw_screen([(player, None)], board, players)

            playing_1 = True
            while playing_1:
                stack_uno+=random.randint(1,4)
                uno_time = 4000 - stack_uno
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                uno_timer = game_font.render(str(uno_time), True, (255,255,255))
                pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                if stack_uno>4000:
                    test=True
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == display_funct.space:
                            playing_1 = False
                            test=False
                            
                pygame.display.flip()

            if test:
                print("드로우")
                player.grab_card(deck)
                display_funct.redraw_screen([(players[0], None)], board, players)
                test=False
                    
        display_funct.redraw_screen([(player, None)], board, players)

    return (player, turn_done)


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

    players[0].push(players)

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
        display_funct.turn_turn = player.name


        if player.skip:
            if player.AI:
                increment_card_old_vals(player)

            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            extern_AI_player_turn(board, deck, player, players, turn)
            stack_uno = 0
            if len(player.hand) == 1:
                test= False
                playing = True
                while playing:
                    stack_uno+=random.randint(1,4)
                    display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                    
                    uno_time = 4000 - stack_uno
                    display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                    uno_timer = game_logic.game_font.render(str(uno_time), True, (255,255,255))
                    pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                    display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                    if stack_uno>4000:
                        display_funct.unoother_played = True
                        test=False
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == display_funct.space:
                                playing = False
                                test = True
                    pygame.display.flip()

                if test:
                    print("드로우 됨")
                    player.grab_card(deck)
                    
                    display_funct.redraw_screen([(players[0], None)], board, players)
                    test=False
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
client_received = False
server_received = False

def Client_Receive(client_socket,board, players, deck, deck1):
    try:
        print("Thread Client_Receive Start")

        serialized_dict = client_socket.recv(4096)
        both_dict = pickle.loads(serialized_dict)  # 1024는 수신 버퍼의 크기를 나타냄

        board_dict = both_dict[0]
        player_dict = both_dict[1]

        print(3)
        board.turn_iterator = board_dict[1]
        board.update_Board(deck1.grab_card_multi(board_dict[2]))
        board.color = board_dict[4]

        result = [len(value) for value in player_dict.values()]
        print(player_dict)

        for a in range(len(players)):
            players[a].hand = []
            if players[a].name[8] == "C":
                for i in player_dict[players[a].name]:
                    players[a].grab_card_multi(deck1,i)
            else:
                players[a].grab_cards(deck,result[a])

        print(player_dict)
        print(board_dict)

        game_logic.current_turn = board_dict[3][8]
        game_logic.client_received = True
        
        display_funct.turn_turn = board_dict[3]

        print(display_funct.turn_turn)

        print("Thread Client Exit")
    except:
        print("test")

played_color = 0
played_type = 0
grabbed = 0
played_card = 0

def Server_Receive(client_socket,board,player,deck1, players):
    try:
        print("Thread Server_Receive Start")
        client_played = client_socket.recv(4096)
        client_play = pickle.loads(client_played)
        player.hand=[]
        for card in list(client_play[0].values()):
            for a in card:
                player.hand.append(deck1.grab_card_multi(a))
        board.update_Board(deck1.grab_card_multi(client_play[1]))
        board.color = client_play[2]

        game_logic.played_color = client_play[1][0]
        game_logic.played_type = client_play[1][2]
        game_logic.grabbed = client_play[4]
        game_logic.played_card = client_play[3]

        game_logic.server_received = True
        
        print("Thread Server Exit")
    except:
        print("Client Exit")
        game_logic.server_received = True
        display_funct.client_socket.close()
        players.remove(player)
    


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
        display_funct.turn_turn = player.name

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
            display_funct.wait(1000)
            
            
            seednum=random.randrange(1,1000)
            
            random.seed(seednum)
            index=random.randrange(0,4)
            board.color=randcolor[index]
            
            asdf="small_cards/" + randcolor1[index] +"_"+ TYPE + ".png"
            board.card_stack[-1].card_data=pygame.image.load(asdf)

      
            print("변경된 색깔 :"+board.color+" 변경된 타입 :"+board.type) 
            display_funct.redraw_screen([(players[0], None)], board, players)
            display_funct.wait(1000)

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


get_out = False
def game_loop_host(board, deck, players):
    display_funct.player_total = 0
    for i in players:
        display_funct.player_total += 1

    board.turn_iterator = 1
    turn = 0
    turn_tot = 0
    drop_again = False
    board.update_Board(deck.grab_card())
    

    board_dict = []
    board_dict.append(board.name)
    board_dict.append(board.turn_iterator)
    board_dict.append(board.card_stack[-1].name)
    board_dict.append(board.color)
    board_dict.append(board.color)

    player_dict = {}
    for player in players:
        player_dict[player.name] = []
        for a in range(len(player.hand)):
            player_dict[player.name].append(player.hand[a].name)


    both_dict = []
    both_dict.append(board_dict)
    both_dict.append(player_dict)

    both_dict_pickle = pickle.dumps(both_dict)         
    display_funct.client_socket.sendall(both_dict_pickle)
    
    deck1 = deck_gen.gen_rand_deck("deck2",1)

    while True:
        player = players[turn]
        turn_tot += 1

        print("Turn number:", turn_tot)
        print("PLAYER: ", player.name, "TURN")

        display_funct.turn_turn = player.name

        if player.skip:
            if player.AI:
                increment_card_old_vals(player)
            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            extern_AI_player_turn(board, deck, player, players, turn)

            try:
                board_dict = []
                board_dict.append(board.name)
                board_dict.append(board.turn_iterator)
                board_dict.append(board.card_stack[-1].name)
                board_dict.append(player.name)
                board_dict.append(board.color)

                player_dict = {}

                for playersa in players:
                    player_dict[playersa.name] = []
                    for a in range(len(playersa.hand)):
                        player_dict[playersa.name].append(playersa.hand[a].name)

                both_dict = []
                both_dict.append(board_dict)
                both_dict.append(player_dict)

                both_dict_pickle = pickle.dumps(both_dict)         
                display_funct.client_socket.sendall(both_dict_pickle)
                print("player AI both send")

            except:
                print("AI Client exit")
            
            stack_uno = 0
            if len(player.hand) == 1:
                    test= False
                    playing = True
                    while playing:
                        stack_uno+=random.randint(1,4)
                        display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                        
                        uno_time = 4000 - stack_uno
                        display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                        uno_timer = game_font.render(str(uno_time), True, (255,255,255))
                        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                        display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                        if stack_uno>4000:
                            test=False
                            display_funct.unoother_played = True
                            break
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == display_funct.space:
                                    playing = False
                                    test = True
                        pygame.display.flip()

                    if test:
                        print("드로우")
                        player.grab_card(deck)
                        display_funct.redraw_screen([(players[0], None)], board, players)
                        test=False
        
        elif player.Client:
            try:
                print("클라이언트 플레이 대기중")
                done = False
                display_funct.redraw_screen([(players[0], None)], board, players)
                while not done:
                    board_dict = []
                    board_dict.append(board.name)
                    board_dict.append(board.turn_iterator)
                    board_dict.append(board.card_stack[-1].name)
                    board_dict.append(player.name)
                    board_dict.append(board.color)

                    player_dict = {}


                    for playersa in players:
                        for a in range(len(playersa.hand)):
                            try:
                                player_dict[playersa.name].append(playersa.hand[a].name)
                            except:
                                player_dict[playersa.name] = [playersa.hand[a].name]

                    both_dict = []
                    both_dict.append(board_dict)
                    both_dict.append(player_dict)

                    both_dict_pickle = pickle.dumps(both_dict)         
                    display_funct.client_socket.sendall(both_dict_pickle)
                    print("player Client both send")

                    s_r = threading.Thread(target=Server_Receive, args=(display_funct.client_socket, board, player, deck1,players))
                    s_r.start()

                    multi_wait()

                    if game_logic.grabbed == True:
                        display_funct.redraw_screen([(players[0], None)], board, players)
                        break

                    if played_color == "w":
                        for a in range(len(players)):
                            if  players[a].name == game_logic.played_card:
                                target = a
                        if played_type == "d":      # wild choose color draw 4 card played
                            players[target].grab_cards(deck, 4)
                        elif played_type == "a":
                            for play in players:
                                if play.name == player.name:
                                    pass
                                else:
                                    play.grab_card(deck)
        
                                

                    elif played_type == "p":        # draw 2 card played
                        for a in range(len(players)):
                            if  players[a].name == game_logic.played_card:
                                target = a
                        players[target].grab_cards(deck, 2)
                        done = True
                    elif played_type == "s":        # skip turn card played
                        for a in range(len(players)):
                            if  players[a].name == game_logic.played_card:
                                target = a
                        players[target].skip = True
                        done = True
                    elif played_type == "d":
                        for a in range(len(players)):
                            if  players[a].name == game_logic.played_card:
                                target = a
                        players[target].grab_cards(deck, 1)
                        done = True
                    elif played_type == "k":
                        pass
                    else:
                        done = True

                    check_winners(player)

                    display_funct.redraw_screen([(players[0], None)], board, players)
                display_funct.wait(500000)

            except:
                display_funct.client_socket.close()
                players.remove(player)

        else:            # handle for a human player
            
            (update, turn_done) = extern_player_turn_host(board, deck,
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


current_turn = ''

def game_loop_client():

    # here
    serialized_dict = display_funct.client_socket.recv(4096)
    both_dict = pickle.loads(serialized_dict)  # 1024는 수신 버퍼의 크기를 나타냄

    board_dict = both_dict[0]
    player_dict = both_dict[1]

    board = game_classes.Board("board1")

    players = []
    display_funct.player_total = 0
    for a in range(len(list(player_dict.keys()))):
        player_ = game_classes.Player(list(player_dict.keys())[a])
        players.append(player_)
        display_funct.player_total += 1

    My_turn = 0
    for a in range(len(list(player_dict.keys()))):
        if list(player_dict.keys())[a][8] == "C":
            My_turn = a

    deck = deck_gen.gen_rand_deck("deck", 0)
    deck1 = deck_gen.gen_rand_deck("deck1",1)

    
    for a in range(len(players)):
            players[a].hand = []
            if players[a].name[8] == "C":
                for i in player_dict[players[a].name]:
                    players[a].grab_card_multi(deck1,i)
            else:
                players[a].grab_cards(deck,5)

    board.turn_iterator = board_dict[1]
    board.update_Board(deck1.grab_card_multi(board_dict[2]))
    board.color = board_dict[4]


    display_funct.redraw_screen([(players[My_turn], None)], board, players)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        c_r = threading.Thread(target=Client_Receive, args=(display_funct.client_socket, board, players, deck, deck1))
        c_r.start()

        multi_wait()

        print("redraw")
        display_funct.redraw_screen([(players[My_turn], None)], board, players)
        

        for player in players:
            check_winners_multi(player,players)
            if len(winners) >= 1:
                players.remove(player)
                restart_bool = check_game_done(players, 1)

                # leaves this instance of the game logic loop back to PY-UNO start
                # in which a new game is started
                if restart_bool:
                    return



        if game_logic.current_turn == 'C':
            print("My turn")
            done = False
            while not done:
                #내 턴
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                (grab, turn_done) = extern_player_turn_client(board, deck,players[My_turn], players, 0)

                if turn_done == True or grab == True:
                    done = True

            for player in players:
                if player in winners:
                    players.remove(player)
                    restart_bool = check_game_done(players, 1)

                    # leaves this instance of the game logic loop back to PY-UNO start
                    # in which a new game is started
                    if restart_bool:
                        return
            
        else:
            for player in players:
                if player.name == display_funct.turn_turn:
                    if len(player.hand) == 1:
                        playing_1 = True
                        stack_uno = 0
                        while playing_1:
                            stack_uno+=random.randint(1,4)
                            uno_time = 4000 - stack_uno
                            display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                            uno_timer = game_font.render(str(uno_time), True, (255,255,255))
                            pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                            display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                            if stack_uno>4000:
                                test=True
                                playing_1 = False

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == display_funct.space:
                                        playing_1 = False
                                        test=False
                                        
                            pygame.display.flip()

                    display_funct.redraw_screen([(players[My_turn], None)], board, players)
            print("Not my turn")


def extern_player_turn_host(board, deck, player, players, turn):
    drop_again = True
    game_logic.start_ticks=pygame.time.get_ticks()
    game_logic.paused_time = 0
    display_funct.cont3 = 0
    stack_uno=0
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
        
        print(board.card_stack[-1].name)

        # returns false unless a drop_again type card is played
        if (grab==True):
            break
        else:
            drop_again = card_logic.card_played_type(board, deck,
                                                 player, players)
            
        print(board.card_stack[-1].name)

        try:
            board_dict = []
            board_dict.append(board.name)
            board_dict.append(board.turn_iterator)
            board_dict.append(board.card_stack[-1].name)
            board_dict.append(player.name)
            board_dict.append(board.color)

            player_dict = {}
            for playersa in players:
                player_dict[playersa.name] = []
                for a in range(len(playersa.hand)):
                    player_dict[playersa.name].append(playersa.hand[a].name)

                

            both_dict = []
            both_dict.append(board_dict)
            both_dict.append(player_dict)

            both_dict_pickle = pickle.dumps(both_dict)         
            display_funct.client_socket.sendall(both_dict_pickle)
            print("player both send")
        except:
            print("My turn Client Exit")

        if drop_again == True:
            display_funct.wildplayed = True

        if display_funct.cont3 >= 4:
            display_funct.cont3_true = True
#주석   
        

        if len(player.hand) == 1:
            
            test= False
            display_funct.redraw_screen([(player, None)], board, players)

            playing_1 = True
            while playing_1:
                stack_uno+=random.randint(1,4)
                uno_time = 4000 - stack_uno
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                uno_timer = game_font.render(str(uno_time), True, (255,255,255))
                pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                if stack_uno>4000:
                    test=True
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == display_funct.space:
                            playing_1 = False
                            test=False
                            
                pygame.display.flip()

            if test:
                print("드로우")
                player.grab_card(deck)
                display_funct.redraw_screen([(players[0], None)], board, players)
                test=False
                    
        display_funct.redraw_screen([(player, None)], board, players)

    return (player, turn_done)

target = 0

def extern_player_turn_client(board, deck, player, players, turn):
    drop_again = True
    game_logic.start_ticks=pygame.time.get_ticks()
    game_logic.paused_time = 0
    display_funct.cont3 = 0
    stack_uno=0
    stack_wild=0
    while drop_again:
        turn_done = False
        selected = None
        grab = False

        if display_funct.wildplayed == True:
            game_logic.start_ticks=pygame.time.get_ticks()
            game_logic.paused_time = 0
            display_funct.wildplayed = False

        if stack_wild == 1:
            serialized_dict = display_funct.client_socket.recv(4096)
            stack_wild = 0

        # redraw display at start of human turn
        display_funct.redraw_screen([(player, None)], board, players)

        # grab the list of allowed_cards cards
        allowed_card_list = card_logic.card_allowed(board, player)
        # if no cards can be played end turn
        if len(allowed_card_list) == 0:
            display_funct.drawplay.play()
            player.grab_card(deck)
            display_funct.redraw_screen([(player, None)], board, players)
            turn = compute_turn(players, turn, board.turn_iterator)
            grab = True
            turn_done = True

        while not turn_done:
            (update, selected, turn_done, grab) = intern_player_turn(
                board, deck, player,players, allowed_card_list, selected)
        
            check_winners_multi(player,players)

            update = check_update(board, allowed_card_list, selected,
                                  player, players, update)

        

        # returns false unless a drop_again type card is played
        if (grab==True):
            client_dict = []
            player_client_dict = {}
            for a in range(len(player.hand)):
                try:
                    player_client_dict[player.name].append(player.hand[a].name)
                except:
                    player_client_dict[player.name] = [player.hand[a].name]

            client_dict.append(player_client_dict)
            client_dict.append(board.card_stack[-1].name) 
            client_dict.append(board.color)
            client_dict.append(game_logic.target)
            client_dict.append(grab)

            client_dict_pickle = pickle.dumps(client_dict)
            display_funct.client_socket.sendall(client_dict_pickle)
            return (grab, turn)
        else:
            drop_again = card_logic.card_played_type(board, deck,
                                                 player, players)

        if drop_again == True:
            stack_wild += 1

        client_dict = []
        player_client_dict = {}
        for a in range(len(player.hand)):
            try:
                player_client_dict[player.name].append(player.hand[a].name)
            except:
                player_client_dict[player.name] = [player.hand[a].name]

        client_dict.append(player_client_dict)
        client_dict.append(board.card_stack[-1].name) 
        client_dict.append(board.color)
        client_dict.append(game_logic.target)
        client_dict.append(grab)

        client_dict_pickle = pickle.dumps(client_dict)
        display_funct.client_socket.sendall(client_dict_pickle)

        if len(player.hand) == 1:
            
            test= False
            display_funct.redraw_screen([(player, None)], board, players)

            playing_1 = True
            while playing_1:
                stack_uno+=random.randint(1,4)
                uno_time = 4000 - stack_uno
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                uno_timer = game_font.render(str(uno_time), True, (255,255,255))
                pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                if stack_uno>4000:
                    test=True
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == display_funct.space:
                            playing_1 = False
                            test=False
                            
                pygame.display.flip()
                    
        display_funct.redraw_screen([(player, None)], board, players)

    return (grab, turn_done)

def multi_wait():
    done = False
    timer_start = True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if timer_start == True:
            start_ticks_multi = pygame.time.get_ticks()
            timer_start = False

        time = int(15 - (pygame.time.get_ticks() - start_ticks_multi) / 1000)
        if time < 0:
            time = 0
        timer = game_font.render("timer: " + str(time), True, (255,255,255))
        pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
        display_funct.screen.blit(timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))
        pygame.display.flip()

        if game_logic.server_received == True:
            print("done")
            done = True
            game_logic.server_received = False

        if game_logic.client_received == True:
            print("done")
            done = True
            game_logic.client_received = False

        
