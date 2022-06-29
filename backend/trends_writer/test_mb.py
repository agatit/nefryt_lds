import socket

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 502))
    message = tcp.write_multiple_registers(slave_id=1, starting_address=1000, values=list(range(100)))
    response = tcp.send_message(message, sock)
    print(response)

    message = tcp.write_multiple_registers(slave_id=1, starting_address=2000, values=list(range(100)))
    response = tcp.send_message(message, sock)
    print(response)    
