# import socket programming library
import socket
import threading


# thread function
def threaded(c):
    # data received from client
    data = c.recv(1024)
    if  data:
        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    print("Bye")
    # connection closed
    c.close()


def main():
    host = "10.0.0.141"

    # reverse a port on your computer
    # in our case it is 12345 but it can be anything
    port = 12345
    s = socket.socket()
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print("Connected to :", addr[0], ":", addr[1])

        # Start a new thread and return its identifier
        t = threading.Thread(target=threaded, args=(c,))
        t.start()


if __name__ == "__main__":
    main()
