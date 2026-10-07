"""
=============================================================================
Project Title : Basic TCP Server with Multi-Client Support
File Name     : server.py
Description   : A multithreaded TCP server implementation in Python using the
                standard `socket` and `threading` modules. The server can
                accept and communicate with multiple clients concurrently
                without blocking.
Author        : 3rd-Year BTech Computer Science Student
Language      : Python 3
=============================================================================
"""

import socket
import threading
import sys

# Server Configuration Constants
DEFAULT_HOST = "127.0.0.1"   # Standard loopback interface (localhost)
DEFAULT_PORT = 5000          # Non-privileged port for TCP communication
BUFFER_SIZE = 1024           # Size of receiving buffer (1 KB)
ENCODING = "utf-8"           # Character encoding format for messages

# Global data structure to keep track of connected clients
# Each entry is a tuple: (client_socket, client_address)
connected_clients = []
clients_lock = threading.Lock()  # Thread lock to prevent race conditions


def broadcast(message: str, sender_socket=None):
    """
    Sends a message to all connected clients.
    If sender_socket is provided, the message is sent to all clients EXCEPT
    the sender (used for broadcasting user messages to peers).
    """
    with clients_lock:
        disconnected_clients = []
        for client in connected_clients:
            client_sock, client_addr = client
            # Do not echo broadcast back to the sender
            if client_sock != sender_socket:
                try:
                    client_sock.sendall(message.encode(ENCODING))
                except (OSError, BrokenPipeError):
                    # Client socket is broken or disconnected
                    disconnected_clients.append(client)

        # Cleanup any dead sockets discovered during broadcast
        for dead_client in disconnected_clients:
            if dead_client in connected_clients:
                connected_clients.remove(dead_client)


def handle_client(client_socket: socket.socket, client_address: tuple):
    """
    Handles an individual client connection inside its own dedicated thread.
    Continuously listens for messages from this client, processes them,
    and returns appropriate responses.

    Parameters:
        client_socket  (socket.socket): The accepted client TCP socket
        client_address (tuple): Pair of (IP address, port number) of client
    """
    with clients_lock:
        active_count = len(connected_clients)

    print(f"[CONNECTED] Client {client_address} connected. Active connections: {active_count}")

    # Send a friendly welcome banner to the newly connected client
    welcome_message = (
        f"[SERVER] Welcome! Connected to TCP Server on {DEFAULT_HOST}:{DEFAULT_PORT}.\n"
        f"[SERVER] Type any message to receive an echo, or '/broadcast <msg>' to chat with others.\n"
        f"[SERVER] Type 'exit' to disconnect."
    )
    try:
        client_socket.sendall(welcome_message.encode(ENCODING))
    except OSError:
        pass

    try:
        while True:
            # recv() blocks until the client sends data or disconnects
            data = client_socket.recv(BUFFER_SIZE)

            # An empty byte string (b'') indicates that the client has closed the socket
            if not data:
                break

            # Decode the incoming byte stream into a Python string
            message = data.decode(ENCODING).strip()

            if not message:
                continue

            # Check if client explicitly requests to disconnect
            if message.lower() == "exit":
                print(f"[CLIENT {client_address}] Sent 'exit' signal.")
                break

            # Handle optional broadcast command: /broadcast <message>
            if message.startswith("/broadcast "):
                broadcast_content = message[len("/broadcast "):].strip()
                print(f"[BROADCAST from {client_address}] {broadcast_content}")

                # Send broadcast message to all other connected clients
                broadcast_packet = f"[BROADCAST from {client_address}]: {broadcast_content}"
                broadcast(broadcast_packet, sender_socket=client_socket)

                # Send confirmation back to the sender
                ack_response = f"Server received: Broadcast sent to all active clients."
                client_socket.sendall(ack_response.encode(ENCODING))

            else:
                # Standard echo response for basic TCP client-server communication
                print(f"[CLIENT {client_address}] {message}")
                response = f"Server received: {message}"
                client_socket.sendall(response.encode(ENCODING))

    except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
        # Client closed abruptly (e.g., closed terminal, killed process)
        print(f"[WARNING] Client {client_address} disconnected abruptly (connection reset).")
    except OSError as e:
        print(f"[ERROR] Socket error with client {client_address}: {e}")
    finally:
        # Resource cleanup when client thread terminates
        with clients_lock:
            # Remove client from active list
            client_record = (client_socket, client_address)
            if client_record in connected_clients:
                connected_clients.remove(client_record)
            remaining_connections = len(connected_clients)

        # Close client socket descriptor to release operating system resources
        try:
            client_socket.close()
        except OSError:
            pass

        print(f"[DISCONNECTED] Client {client_address} disconnected. Active connections: {remaining_connections}")


def start_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    """
    Initializes the TCP server socket, binds it to the specified host and port,
    listens for incoming connections, and spawns a new thread for each client.

    Parameters:
        host (str): IP address to bind to (default: 127.0.0.1)
        port (int): Port number to listen on (default: 5000)
    """
    # 1. Create a TCP socket using IPv4 addressing
    #    socket.AF_INET     -> IPv4 addressing family
    #    socket.SOCK_STREAM -> TCP (Transmission Control Protocol, reliable byte stream)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Allow immediate socket reuse after server restart to avoid "Address already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 3. Bind the socket to the chosen IP and Port
    try:
        server_socket.bind((host, port))
    except OSError as e:
        print(f"\n[ERROR] Failed to bind server to {host}:{port}.")
        print(f"[DETAILS] {e}")
        print("[HINT] Ensure no other instance or application is using this port.")
        sys.exit(1)

    # 4. Put the socket into listening mode (backlog queue of 5 pending connections)
    server_socket.listen(5)

    print("==================================================")
    print("           TCP MULTI-CLIENT SERVER               ")
    print("==================================================")
    print(f"[STARTED] Server is listening on {host}:{port}")
    print("[INFO] Waiting for incoming client connections...")
    print("[INFO] Press Ctrl+C at any time to stop the server.")
    print("==================================================")

    try:
        while True:
            # accept() blocks until an incoming client connection arrives.
            # Returns a new socket dedicated to this client and the client's address (IP, Port).
            client_socket, client_address = server_socket.accept()

            # Register client in global list inside lock
            with clients_lock:
                connected_clients.append((client_socket, client_address))

            # 5. Create and start a new daemon thread to handle this client independently
            #    This ensures the server main thread immediately returns to accept()
            #    without waiting for this client to finish!
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        # Graceful shutdown when user presses Ctrl+C in server terminal
        print("\n\n[SHUTDOWN] Server shutdown initiated by user (Ctrl+C).")
    finally:
        # Close all active client connections cleanly
        print("[CLEANUP] Closing all active client sockets...")
        with clients_lock:
            for client_sock, client_addr in connected_clients:
                try:
                    shutdown_msg = "[SERVER] Server is shutting down. Disconnecting.\n"
                    client_sock.sendall(shutdown_msg.encode(ENCODING))
                    client_sock.close()
                except OSError:
                    pass
            connected_clients.clear()

        # Close the listening server socket
        try:
            server_socket.close()
        except OSError:
            pass

        print("[STOPPED] Server has been terminated cleanly. Goodbye!")


if __name__ == "__main__":
    start_server()
