import socket
import time

def connect_and_send():
    server_host = "127.0.0.1"
    server_port = 12345

    while True:
        time.sleep(3)
        message = str(time.time())
        send_message(server_host, server_port, message)

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
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} refused. Is the server running?")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    connect_and_send()