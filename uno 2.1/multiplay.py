import socket
import random
import card_logic
import display_funct
import game_control
import Main_Decision_Tree
import pygame
import game_logic
from pygame.locals import *
import PY_UNO
import os
import game_logic

def server():
    HOST = '10.50.45.254'
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('서버가 시작되었습니다.')
        conn, addr = s.accept()
        with conn:
            answer = random.randint(1, 9)
            print(f'클라이언트가 접속했습니다:{addr}, 정답은 {answer} 입니다.')
            while True:
                data = conn.recv(1024).decode('utf-8')
                print(f'데이터:{data}')


def client():
    HOST = '10.50.45.254'
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            n = input("1-9 사이의 숫자를 입력하세요(0은 게임포기):")
            if not n.strip():
                print("입력값이 잘못되었습니다.")
                continue
            s.sendall(n.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            print(f'서버응답:{data}')
            if data == "정답" or data == "종료":
                break


def game_loop_multi_server(board, deck, players):
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
                game_logic.increment_card_old_vals(player)

            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            game_logic.extern_AI_player_turn(board, deck, player, players, turn)
        elif player.client:
            # 0512 : server가 보내는 정보 board, deck, player, players, turn
            # 0512 : client가 받는 정보도 똑같이 구성. 와카면 turn이 안바뀜 그래서 한번 더 돔?
            # 0512 : 클라이언트가 보내준 정보를 받고 화면 redraw
            # 0512 : client는 player[turn]이 
            (update, turn_done) = game_logic.extern_player_turn(board, deck,
                                                     player, players, turn)
        else:            # handle for a human player
            (update, turn_done) = game_logic.extern_player_turn(board, deck,
                                                     player, players, turn)
            
        if player in game_logic.winners:
            players.remove(player)
            restart_bool = game_logic.check_game_done(players)

            if restart_bool:
                return
            
        # iterate the turn
        turn = game_logic.compute_turn(players, turn, board.turn_iterator)

        # 0512 : client들에게 redraw에 필요한 파라미터를 data로 전달. client는 받아서 화면 출력.
        # 0512 : client는 player[turn]이 본인이면 자신의 턴을 진행하고 카드를 낼 때마다 server에게 낸 카드의 정보 전달
        # 0512 : 근데 와일드카드같은거 내는거면 1.client가 카드를 내고 server에게 전달해줌. 2. server는 나머지에게 모두 보내서 출력함
        # 0512 : 3. client는 서버가 보내준 걸 받고 다시 자기턴이니까 함 더함

def game_loop_multi_client(board, deck, players):
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
                game_logic.increment_card_old_vals(player)

            print("skipping", player.name, "turn")
            player.skip = False

        elif player.AI:  # handle for an AI player
            game_logic.extern_AI_player_turn(board, deck, player, players, turn)
        elif player.client:
            # 0512 : server가 보내는 정보 board, deck, player, players, turn
            # 0512 : client가 받는 정보도 똑같이 구성. 와카면 turn이 안바뀜 그래서 한번 더 돔?
            # 0512 : 클라이언트가 보내준 정보를 받고 화면 redraw
            # 0512 : client는 player[turn]이 
            (update, turn_done) = game_logic.extern_player_turn(board, deck,
                                                     player, players, turn)
        else:            # handle for a human player
            (update, turn_done) = game_logic.extern_player_turn(board, deck,
                                                     player, players, turn)
            
        if player in game_logic.winners:
            players.remove(player)
            restart_bool = game_logic.check_game_done(players)

            if restart_bool:
                return
            
        # iterate the turn
        turn = game_logic.compute_turn(players, turn, board.turn_iterator)

        # 0512 : client들에게 redraw에 필요한 파라미터를 data로 전달. client는 받아서 화면 출력.
        # 0512 : client는 player[turn]이 본인이면 자신의 턴을 진행하고 카드를 낼 때마다 server에게 낸 카드의 정보 전달
        # 0512 : 근데 와일드카드같은거 내는거면 1.client가 카드를 내고 server에게 전달해줌. 2. server는 나머지에게 모두 보내서 출력함
        # 0512 : 3. client는 서버가 보내준 걸 받고 다시 자기턴이니까 함 더함
    
def host_screen():
    #
    board1 = game_logic.game_classes.Board("board1")
    deck1 = game_logic.gen_rand_deck("deck1", 0)

    # defining a 7 player uno game
    player1 = game_logic.game_classes.Player("player_1")
    player1.grab_cards(deck1, 7)
    player2 = game_logic.game_classes.Player("player_2")
    player2.grab_cards(deck1, 7)
    playerAI_list = []
    players = []
    players.append(player1)
    players.append(player2)

    #sizeof playerAI_list 해서 하나씩 넣어야할수도
    players.append(playerAI_list)

    #클라이언트에 board1, deck1, players 전달
    
    game_loop_multi_server(board1, deck1, players)

def client_screen():
    return 0
    # 서버에서 전달받은 board1, deck1, players를 그대로 함수에 사용
    # game_loop_multi_client(board1, deck1, players)
    # 

def main():
    server()

if __name__ == "__main__":
    main() 