import socket


def main():
    # local host IP '127.0.0.1'
    host = "10.0.0.141"

    # Define the port on which you want to connect
    port = 12345


    # message you send to server
    while True:
        message = input("please input your message, type exit to stop\n")

        if message.lower() == "exit":
            break

        s = socket.socket()

        # connect to server
        s.connect((host, port))

        # message sent to server
        s.send(message.encode("ascii"))

        # message received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print("Server replied: {}".format(str(data.decode("ascii"))))

        # close the connection
        s.close()


if __name__ == "__main__":
    main()
