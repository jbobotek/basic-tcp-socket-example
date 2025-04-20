import socket
import time
import unittest
import server
import logging


def connect_and_send(freq, duration, message, host="127.0.0.1", port=12345):
    log_loc = logging.basicConfig(filemode='a', filename="client_log.txt", level=logging.INFO)
    start = time.time()
    while start + duration > time.time():
        time.sleep(freq)
        logging.info(send_message(host, port, message))

# A "sender" component that emits a "heartbeat" message over a TCP socket on regular intervals.
def send_message(host, port, message):
    """Sends a message to the server and prints the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode()}")
            return data.decode()
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} refused. Is the server running?")
    except Exception as e:
        print(f"Error sending message: {e}")

class tester(unittest.TestCase):
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 65432

    @classmethod
    def setUpClass(cls):
        """Start the test server before running any tests."""
        cls.server_thread = threading.Thread(target=server.server_program.start_server, args=(cls.SERVER_HOST, cls.SERVER_PORT), daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    def test_short_ascii_message_stability(self):
        """Tests sending a short ASCII message."""
        message = "hello"
        connect_and_send(1, 5, message, self.SERVER_HOST, self.SERVER_PORT)
        self.assertEqual(response, f"Server received: {message}")
    

if __name__ == "__main__":
    connect_and_send(1, 5, "hello")