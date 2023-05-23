# 멀티플레이 시 ip inputbox 구현 참고 코드 

import socket
import pickle
import threading

def Receive():
    print("Thread Receive Start")

s = threading.Thread(target=Receive, args=())
s.start()

