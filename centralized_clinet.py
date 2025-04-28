import socket
import time

COORDINATOR_IP = 'localhost'  # Change later for 2 PCs
PORT = 5000

def request_critical_section():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((COORDINATOR_IP, PORT))

    print("[Client] Sending REQUEST...")
    s.send('REQUEST'.encode())

    reply = s.recv(1024).decode()
    if reply == 'GRANTED':
        print("[Client] Access GRANTED! Entering Critical Section...")
        time.sleep(5)  # Simulate work
        print("[Client] Exiting Critical Section.")
        s.send('RELEASE'.encode())
    
    s.close()

if _name_ == "_main_":
    request_critical_section()