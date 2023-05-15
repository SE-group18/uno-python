# 멀티플레이 시 ip inputbox 구현 참고 코드 

import socket
import pickle

HOST = '192.168.0.25'
PORT = 5555  # 포트 번호 (임의의 값으로 설정)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# 클라이언트 관리를 위한 리스트
selected_ai2 = "no"
selected_ai3 = "no"
selected_ai4 = "no"
selected_ais = [selected_ai2,selected_ai3,selected_ai4]

client_socket, addr = server_socket.accept()
while True:
    # 클라이언트 연결 수락
    serialized_data = pickle.dumps(selected_ais)
    client_socket.sendall(serialized_data)