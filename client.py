import socket
import time
import unittest
import server
import logging
import threading


def compare_logs(client_log, server_log, lines=5) -> bool:
    """Compares the last lines in two logs."""
    with open(client_log, 'r') as log1:
        lines1 = log1.readlines()[-1 * lines:]
    with open(server_log, 'r') as log2:
        lines2 = log2.readlines()[-1 * lines:]
    return lines1 == lines2

# A "sender" component that emits a "heartbeat" message over a TCP socket on regular intervals.
def connect_and_send(freq, duration, message, host="127.0.0.1", port=12345):
    log_loc = logging.getLogger("client_log")
    log_loc.setLevel(logging.INFO)
    log_loc.addHandler(logging.FileHandler("client_log.txt"))
    start = time.time()
    while start + duration > time.time():
        time.sleep(freq)
        log_loc.info(send_message(host, port, message))

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
    client_file = "client_log.txt"
    server_file = "server_log.txt"

    @classmethod
    def setUpClass(cls):
        """Start the test server before running any tests."""
        cls.server_instance = server.server_program(cls.SERVER_HOST, cls.SERVER_PORT)
        cls.server_thread = threading.Thread(target=cls.server_instance.start_server, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    def test_short_message_stability(self):
        """Tests sending a short ASCII message."""
        message = "hello"
        connect_and_send(1, 5, message, self.SERVER_HOST, self.SERVER_PORT)
        self.assertTrue(compare_logs(self.client_file, self.server_file))

    def test_long_message_stability(self):
        """Tests sending a long ASCII message."""
        message = "hello"*500
        connect_and_send(1, 5, message, self.SERVER_HOST, self.SERVER_PORT)
        self.assertTrue(compare_logs(self.client_file, self.server_file))

if __name__ == "__main__":
    # connect_and_send(1, 5, "hello")
    unittest.main()