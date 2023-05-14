import AI_functs
import game_logic
import Main_Decision_Tree
import display_funct
import pygame

def update_mem_trees(board, deck, player, players):
    pass
    # TODO


def AI_wild_pick_4(board, deck, player, target, selected_color):
    """
    Card function that handles when the AI player plays a wild pick 4 card.

    O(1) runtime
    """
    board.color = selected_color
    print("New color: ", board.color)
    print("Targeted player: ", target.name)
    print("Trageted players hand size before: ", len(target.hand))
    target.grab_cards(deck, 4)  # O(4)
    print("Trageted players hand size after: ", len(target.hand))
    # update targets hatval of player
    game_logic.update_hatval(player, target, 4)


def AI_wild_color(board, player, selected_color):
    """
    Card function that handles when the AI player plays a wild color card.

    O(1) runtime
    """
    board.color = selected_color
    print("New color: ", board.color)


def AI_draw_2(deck, player, target):
    """
    Card function that handles when the AI player plays a draw 2 card.

    O(1) runtime
    """
    print("Targeted player: ", target.name)
    print("Trageted players hand size before: ", len(target.hand))
    target.grab_cards(deck, 2)
    print("Trageted players hand size after: ", len(target.hand))
    # update targets hatval of player
    game_logic.update_hatval(player, target, 2)


def AI_skip(board, player, target):
    """
    Card function that handles when the AI player plays a skip turn card.

    O(1) runtime
    """
    print("Targeted player skipping: ", target.name)
    target.skip = True
    # update targets hatval of player
    game_logic.update_hatval(player, target, 1)


def AI_reverse(board):
    """
    Card function that handles when the AI player plays the reverse card.

    O(1) runtime
    """
    turn_iterator = board.turn_iterator
    print("reversing", turn_iterator)
    board.turn_iterator = -turn_iterator

def AI_draw_1(deck, player, target):
    """
    Card function that handles when the AI player plays a draw 2 card.

    O(1) runtime
    """
    print("Targeted player: ", target.name)
    print("Trageted players hand size before: ", len(target.hand))
    target.grab_cards(deck, 1)
    print("Trageted players hand size after: ", len(target.hand))
    # update targets hatval of player
    game_logic.update_hatval(player, target, 1)

def AI_all_draw(deck, player, players, board, selected_color):
    board.color = selected_color
    for play in players:
        if play.name == player.name:
            pass
        else:
            play.grab_card(deck)

    
########################################################


def AI_card_played_type(board, deck, player, players, target=None, selected_color=None):
    """
    Logic function that takes the most recently played card and decides
    what game actions are needed to be taken to accomadate. These actions are
    then preformed by other functions detailed above.

    O(1) if target and selected color are already given

    or

    O(n) runtime where n is the number of players OR player handsize

    or

    Main_Decision_Tree is retraveled thus making stuff deeper.
    """
    stack_uno=0
    # check to see if AI won
    game_logic.check_winners(player)

    # if no target was selected set target to be most hated player
    if target is None:
        (max_hate, hate_player) = AI_functs.fetch_hate_priority(
            player, players)  # O(n)
        target = hate_player

    # if no color was selected set it to most common_color
    if selected_color is None:
        selected_color = AI_functs.fetch_most_common_color(player)  # O(n)

    played_type = board.type
    played_color = board.color

    print("Played:", played_color, played_type, "by:", player.name)


    if played_color == "w":
        if played_type == "d":      # wild choose color draw 4 card played
            AI_wild_pick_4(board, deck, player, target, selected_color)
        elif played_type == "c":    # wild choose color card played
            AI_wild_color(board, deck, selected_color)
        elif played_type == "a":
            AI_all_draw(deck,player,players, board,selected_color)

        # go through Main_Decision_Tree as another card can be played
        # as the AI played a wild card
        if player.hand == []:  # catch if the player has won
            return
        else:
            print("Wild played, playing again.")
            display_funct.redraw_screen([(players[0], None)], board, players)

            if len(player.hand) == 1:
                test= False
                playing = True
                while playing:
                    stack_uno += 1
                    display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                    
                    uno_time = 4000 - stack_uno
                    display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                    uno_timer = game_logic.game_font.render(str(uno_time), True, (255,255,255))
                    pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                    display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                    if stack_uno>4000:
                        test=False
                        game_logic.uno_clicked = False

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
                    player.grab_cards(deck,1)
                    
                    display_funct.redraw_screen([(players[0], None)], board, players)
                    test=False
            

            display_funct.redraw_screen([(players[0], None)], board, players)
            pygame.time.delay(1200)
             


            Main_Decision_Tree.travel_Main_Decision_Tree(board, deck, player,
                                                         players, player.Main_Decision_Tree.Dec_Tree)

    elif played_type == "p":        # draw 2 card played
        AI_draw_2(deck, player, target)

    elif played_type == "s":        # skip turn card played
        AI_skip(board, player, target)

    elif played_type == "r":        # reverse card played
        AI_reverse(board)

    elif played_type == "d":
        AI_draw_1(deck, player, target)

    elif played_type == "k":
        print("king played, play again")
        display_funct.redraw_screen([(players[0], None)], board, players)

        if len(player.hand) == 1:
            test= False
            playing = True
            while playing:
                stack_uno += 1
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                
                uno_time = 4000 - stack_uno
                display_funct.screen.blit(display_funct.uno_on_button, (display_funct.screen_width*1200/1600,display_funct.screen_height*495/900))
                uno_timer = game_logic.game_font.render(str(uno_time), True, (255,255,255))
                pygame.draw.rect(display_funct.screen, (0,0,0), [display_funct.screen_width*1400/1600,display_funct.screen_height*530/900,150,70])
                display_funct.screen.blit(uno_timer, (display_funct.screen_width*1400/1600,display_funct.screen_height*530/900))

                if stack_uno>4000:
                    test=False
                    game_logic.uno_clicked = False

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
                player.grab_cards(deck,1)
                
                display_funct.redraw_screen([(players[0], None)], board, players)
                test=False
            

        display_funct.redraw_screen([(players[0], None)], board, players)
        pygame.time.delay(1200)
        Main_Decision_Tree.travel_Main_Decision_Tree(board, deck, player,
                                                         players, player.Main_Decision_Tree.Dec_Tree)
    elif played_type.isdigit():     # normal number card played
        pass