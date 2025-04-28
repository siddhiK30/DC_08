import socket
import threading
import time

MY_IP = '10.10.40.213'
MY_PORT = 5000
NEXT_IP = '10.10.40.132'
NEXT_PORT = 5001

HAS_TOKEN = True

def listen_for_token():
    global HAS_TOKEN
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', MY_PORT))
    s.listen()
    print(f"[Node] Listening for token on port {MY_PORT}...")
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024).decode()
        if data == 'TOKEN':
            print(f"[Node] Received TOKEN from {addr}")
            HAS_TOKEN = True
        conn.close()

def send_token():
    global HAS_TOKEN
    while True:
        if HAS_TOKEN:
            print("[Node] I have the token! Entering Critical Section...")
            time.sleep(5)  # Simulate critical section
            print("[Node] Exiting Critical Section. Passing token...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((NEXT_IP, NEXT_PORT))
            s.send('TOKEN'.encode())
            s.close()
            HAS_TOKEN = False
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=listen_for_token).start()
    threading.Thread(target=send_token).start()
