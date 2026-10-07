"""
=============================================================================
Project Title : Basic TCP Server with Multi-Client Support
File Name     : client.py
Description   : A TCP client application in Python using standard `socket`
                and `threading` modules. Connects to the server, sends messages,
                receives responses asynchronously, and handles disconnection cleanly.
Author        : 3rd-Year BTech Computer Science Student
Language      : Python 3
=============================================================================
"""

import socket
import threading
import sys

# Default Server Configuration Constants
DEFAULT_HOST = "127.0.0.1"   # IP address of the server
DEFAULT_PORT = 5000          # Port number the server is listening on
BUFFER_SIZE = 1024           # Size of buffer for reading data
ENCODING = "utf-8"           # Encoding used for text transmission


def receive_messages(client_socket: socket.socket, stop_event: threading.Event):
    """
    Background worker thread function that continuously listens for incoming
    messages from the server (responses, broadcasts, server shutdown notifications).
    Running this in a separate thread prevents the client UI from blocking while
    waiting for user input.

    Parameters:
        client_socket (socket.socket): The connected TCP socket
        stop_event (threading.Event): Signal used to stop both threads cleanly
    """
    while not stop_event.is_set():
        try:
            # recv() blocks until the server sends data or closes the connection
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                # An empty return from recv() means the server closed the connection
                if not stop_event.is_set():
                    print("\n\n[DISCONNECTED] Server closed the connection.")
                    stop_event.set()
                break

            response = data.decode(ENCODING)
            # Display received message cleanly to the terminal
            print(f"\n[SERVER RESPONSE] {response}")
            # Re-display prompt so user knows they can continue typing
            if not stop_event.is_set():
                print("Enter message: ", end="", flush=True)

        except (ConnectionResetError, ConnectionAbortedError):
            if not stop_event.is_set():
                print("\n\n[DISCONNECTED] Connection was reset by the server.")
                stop_event.set()
            break
        except OSError:
            # Socket was closed locally or encountered an error
            break


def send_messages(client_socket: socket.socket, stop_event: threading.Event):
    """
    Runs in the main thread to read user input from the console and transmit
    it across the TCP socket to the server.

    Parameters:
        client_socket (socket.socket): The connected TCP socket
        stop_event (threading.Event): Signal used to stop both threads cleanly
    """
    while not stop_event.is_set():
        try:
            message = input("Enter message: ").strip()

            if not message:
                continue

            # Send the encoded message to the server
            client_socket.sendall(message.encode(ENCODING))

            # If user typed 'exit', terminate the client session
            if message.lower() == "exit":
                print("[DISCONNECTED] You have disconnected from the server.")
                stop_event.set()
                break

        except (KeyboardInterrupt, EOFError):
            print("\n[DISCONNECTING] Exit requested by user (Ctrl+C).")
            try:
                client_socket.sendall("exit".encode(ENCODING))
            except OSError:
                pass
            stop_event.set()
            break
        except OSError as e:
            if not stop_event.is_set():
                print(f"\n[ERROR] Failed to send message: {e}")
                stop_event.set()
            break


def connect_to_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> socket.socket:
    """
    Creates an IPv4 TCP socket and connects to the server.
    Handles network errors gracefully (e.g. server offline, invalid address).

    Parameters:
        host (str): IP address of the target server
        port (int): Port number of the target server

    Returns:
        socket.socket: Successfully connected socket object, or exits cleanly.
    """
    # 1. Create a TCP socket using IPv4
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("==================================================")
    print("            TCP CLIENT APPLICATION               ")
    print("==================================================")
    print(f"[CONNECTING] Attempting to connect to server at {host}:{port}...")

    # 2. Establish connection to the server
    try:
        client_socket.connect((host, port))
        print(f"[CONNECTED] Successfully connected to {host}:{port}!")
        print("--------------------------------------------------")
        print("Commands & Usage:")
        print("  - Type any message and press Enter to send.")
        print("  - Type '/broadcast <message>' to broadcast to all clients.")
        print("  - Type 'exit' to disconnect cleanly.")
        print("==================================================")
        return client_socket

    except ConnectionRefusedError:
        print(f"\n[ERROR] Connection refused by {host}:{port}.")
        print("[REASON] The server does not appear to be running on this address/port.")
        print("[SOLUTION] Run 'python server.py' first in another terminal window.\n")
        client_socket.close()
        sys.exit(1)

    except socket.gaierror:
        print(f"\n[ERROR] Invalid host address: '{host}'. Could not resolve host.\n")
        client_socket.close()
        sys.exit(1)

    except OSError as e:
        print(f"\n[ERROR] Could not connect to server: {e}\n")
        client_socket.close()
        sys.exit(1)


def main():
    """
    Main function to initialize and run the TCP client.
    """
    # Optional command line arguments: python client.py [host] [port]
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    client_socket = connect_to_server(host, port)

    # Event flag to synchronize graceful termination across threads
    stop_event = threading.Event()

    # Start the background receiver thread (daemon=True ensures it dies when program exits)
    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, stop_event),
        daemon=True
    )
    receiver_thread.start()

    # Start the message input loop on main thread
    send_messages(client_socket, stop_event)

    # Cleanup socket on exit
    try:
        client_socket.close()
    except OSError:
        pass

    print("[SESSION ENDED] Client program closed cleanly.")


if __name__ == "__main__":
    main()
