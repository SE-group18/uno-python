import socket
import pickle

# 서버의 IP 주소와 포트 번호
SERVER_HOST = '192.168.0.25'  # 서버 IP 주소
SERVER_PORT = 5555  # 서버 포트 번호

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# 서버로부터 응답 수신
datas = client_socket.recv(4096)
selected_ais = pickle.loads(datas)
print(selected_ais)