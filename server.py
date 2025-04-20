import threading
import socket
import logging


# A "receiver" component that receives the messages and logs them.
class server_program():

    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.log_loc = logging.basicConfig(filemode='a', filename="log.txt", level=logging.INFO)

    def handle_client(self, conn: socket.socket, addr):
        # Handles communication with a single client.
        print(f"Connection by {str(addr)}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logging.info(f"Received from {str(addr)}: {data.decode()}")
                response = "ACK".encode() # f"Server received: {data.decode('utf-8')}\n".encode('utf-8')
                conn.sendall(response)
        except Exception as e:
            print(f"Error handling client {str(addr)}: {e}")
        finally:
            print(f"Connection with {str(addr)} closed.")
            conn.close()

    def start_server(self):
        # Starts a persistent socket server that handles multiple clients.
        # try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)  # Listen for all incoming connections
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = server_socket.accept()
            # Start a new thread to handle each client connection
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.daemon = True  # Allow the main thread to exit even if clients are connected
            client_thread.start()
        # except Exception as e:
        #     print(f"Error in server: {e}")
        # finally:
        #     if 'server_socket' in locals():
        #         server_socket.close()



if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345

    server_instance = server_program(host, port)
    # Start the persistent server in a separate thread
    server_thread = threading.Thread(target=server_instance.start_server)
    server_thread.daemon = True  # Allow the main thread to exit
    server_thread.start()

    print("Server started in the background.")
    input("Press Enter to close the server...\n")
    # No explicit closing needed here because of server_thread.daemon = True
    print("Server shutting down (implicitly).")