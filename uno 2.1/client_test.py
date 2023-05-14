import socket
import random
import pickle

def server():
    HOST = '10.50.45.254'
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('서버가 시작되었습니다.')
        conn, addr = s.accept()
        with conn:
            #수신
            data = conn.recv(1024).decode('utf-8')
            #송신
            #pickle을 통해 클래스 직렬화
            data = pickle.dumps(data)
            conn.sendall(data.encode('utf-8'))

def client():
    HOST = '10.50.45.254'
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.sendall(msg.encode())

def main():
    client()

if __name__ == "__main__":
    main() 