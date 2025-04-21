import threading
import socket
import logging


# A "receiver" component that receives the messages and logs them.
class server_program():

    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        # logging setup
        self.log_loc = logging.getLogger("server_log")
        self.log_loc.setLevel(logging.INFO)
        self.log_loc.addHandler(logging.FileHandler("server_log.txt"))

    def handle_client(self, conn: socket.socket, addr):
        """Handles communication with a single client."""
        print(f"Connection by {str(addr)}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                self.log_loc.info(data.decode())
                response = data.decode().encode()
                conn.sendall(response)
        except Exception as e:
            print(f"Error handling client {str(addr)}: {e}")
        finally:
            print(f"Connection with {str(addr)} closed.")
            conn.close()

    def start_server(self):
        # Starts a persistent socket server that handles multiple clients.
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = self.server_socket.accept()
                # Start a new thread to handle each client connection
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True  # Allow the main thread to exit even if clients are connected
                client_thread.start()
        except Exception as e:
            print(f"Error in server: {e}")
        finally:
            if 'server_socket' in locals():
                self.server_socket.close()

    def stop(self):
        self.server_socket.close()        

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345

    server_instance = server_program(host, port)
    # Start the persistent server in a separate thread
    server_thread = threading.Thread(target=server_instance.start_server, daemon=True)
    server_thread.start()

    print("Server started in the background.")
    input("Press Enter to close the server...\n")

    # No explicit closing needed here because of server_thread.daemon = True
    print("Server shutting down.")