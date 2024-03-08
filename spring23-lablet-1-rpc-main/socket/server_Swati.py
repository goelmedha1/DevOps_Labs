#!/usr/bin/env python3
import socket

s = socket.socket()
host = '10.0.0.141'  # Get local machine name
port = 4385  # Reserve a port for your service
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection
while True:
    c, addr = s.accept()  # Establish connection with client
    print(f"Connection from {addr} has been established.")
    c.send(b"Thank you for connecting")
    c.close()  # Close the connection
