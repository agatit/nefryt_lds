import socket
import time
import threading
import math as m

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

def send(i, t):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 502))
        message = tcp.write_multiple_registers(slave_id=1, starting_address=i*1000, values=list(range(100)))
        response = tcp.send_message(message, sock)
        print(f"done {i} - {t} {time.time()}")



t = m.floor(time.time()) + 0.5
while True:
    print(f"{time.time()}")
    for i in range(4): 
        threading.Thread(target=send, args=(i,t)).start() 
    
    time.sleep(t - time.time() + 1)
    t += 1
        
