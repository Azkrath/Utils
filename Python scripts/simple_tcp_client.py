import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9999

# create a socket object
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
CLIENT.connect((TARGET_HOST, TARGET_PORT))

# send some data
CLIENT.send(b'ABCDF')

# receive some data
RESPONSE = CLIENT.recv(4096)

print(RESPONSE)
