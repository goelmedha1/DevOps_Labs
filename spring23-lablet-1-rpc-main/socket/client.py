#!/usr/bin/env python3
import socket

s = socket.socket()
host = socket.gethostname()  # Get local machine name
port = 12345  # Specify the port to connect to

s.connect((host, port))
print(s.recv(1024))
s.close()  # Close the socket when done
