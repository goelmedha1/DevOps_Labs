import java.io.*;
import java.net.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

// Server class
class Server {
    public static void main(String[] args) {
        ServerSocket server = null;

        try {
            // server is listening on port 1234
            server = new ServerSocket(1234);
            server.setReuseAddress(true);

            // create Threadpool
            ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(2);

            // running infinite loop for getting client request
            while (true) {
                // socket object to receive incoming client requests
                Socket client = server.accept();

                // Displaying that new client is connected to server
                System.out.println(
                        "New client connected: " + client.getInetAddress());

                // create a new thread object
                ClientHandler clientSock = new ClientHandler(client);

                // Execute the client handler on the executor
                executor.execute(clientSock);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (server != null) {
                try {
                    server.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // ClientHandler class
    private static class ClientHandler implements Runnable {
        private final Socket clientSocket;

        // Constructor
        public ClientHandler(Socket socket) {
            this.clientSocket = socket;
        }

        public void run() {
            PrintWriter out = null;
            BufferedReader in = null;

            try {
                // get the outputstream of client
                out = new PrintWriter(clientSocket.getOutputStream(), true);

                // get the inputstream of client
                in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

                String line;
                while ((line = in.readLine()) != null) {

                    // writing the received message from client
                    System.out.printf(" Sent from the client: %s\n", line);
                    out.println(new StringBuilder(line).reverse().toString());
                }

                System.out.println("Bye");
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    if (out != null) {
                        out.close();
                    }
                    if (in != null) {
                        in.close();
                        clientSocket.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}