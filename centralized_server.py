import socket
import threading
import queue

# HOST = 'localhost'  # Change later for 2 PCs
HOST = '0.0.0.0'
PORT = 5000

request_queue = queue.Queue()
lock = threading.Lock()

def client_handler(conn, addr):
    print(f"[Server] Connected to {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == 'REQUEST':
                with lock:
                    if request_queue.empty():
                        conn.send('GRANTED'.encode())
                    else:
                        request_queue.put(conn)
                print(f"[Server] Received REQUEST from {addr}")
            elif data == 'RELEASE':
                with lock:
                    if not request_queue.empty():
                        next_conn = request_queue.get()
                        next_conn.send('GRANTED'.encode())
                print(f"[Server] Received RELEASE from {addr}")
        except:
            break
    conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Server] Coordinator started on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_handler, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()