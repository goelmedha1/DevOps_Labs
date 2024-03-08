import asyncio, socket


async def handle_client(c):
    loop = asyncio.get_event_loop()
    while True:
        # data received from client
        data = await loop.sock_recv(c, 1024)

        if not data:
            print("Bye")
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        await loop.sock_sendall(c, data)

    # connection closed
    c.close()


async def run_server():
    server = socket.socket()
    server.bind(("localhost", 12345))
    server.listen(5)
    server.setblocking(False)
    print("socket is listening")

    loop = asyncio.get_event_loop()

    while True:
        client, addr = await loop.sock_accept(server)
        print("Connected to :", addr[0], ":", addr[1])
        loop.create_task(handle_client(client))


    asyncio.run(run_server())
