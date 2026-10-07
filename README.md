# Basic TCP Server with Multi-Client Support

> **A Complete College-Level Computer Networks Project**  
> *Developed for 3rd-Year BTech Computer Science & Engineering*

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Technologies Used](#technologies-used)
5. [System Architecture](#system-architecture)
6. [Project Folder Structure](#project-folder-structure)
7. [Installation & Setup](#installation--setup)
8. [How to Run (Step-by-Step)](#how-to-run-step-by-step)
9. [Example Output](#example-output)
10. [Core Features](#core-features)
11. [Optional Enhancement: Broadcast Feature](#optional-enhancement-broadcast-feature)
12. [Error Handling & Edge Cases](#error-handling--edge-cases)
13. [Testing Procedure & Automated Test Suite](#testing-procedure--automated-test-suite)
14. [Viva Questions and Answers (20 Questions)](#viva-questions-and-answers-20-questions)
15. [Future Scope](#future-scope)
16. [Presentation Guide](#presentation-guide)

---

## Project Overview

**Basic TCP Server with Multi-Client Support** is a foundational Computer Networks project built using **Python 3**, the standard `socket` module, and the `threading` module

It implements a client-server architecture where a centralized TCP server can accept, communicate with, and manage **multiple clients simultaneously**. Each client connects independently over TCP/IP, sends messages, receives server responses, and can disconnect without affecting other active clients.

---

## Problem Statement

In a traditional **single-threaded iterative TCP server**, the server handles connections sequentially:

1. It listens on an IP and Port.
2. It accepts Client 1.
3. It enters a blocking loop reading data from Client 1 using `recv()`.
4. While communicating with Client 1, the server **cannot accept or serve any other client**.
5. Client 2 and Client 3 are stalled in the connection queue until Client 1 disconnects.

If Client 1 remains connected without sending data, the entire server is blocked, leading to client starvation and poor resource utilization.

### The Solution: Multithreading

This project solves the problem by leveraging **multithreading**:

- The main thread of the server only listens for incoming connections using `accept()`.
- The moment a new client connects, the server spawns an **independent worker thread** dedicated exclusively to that client.
- The main thread immediately loops back to accept more clients.
- Thus, Client 1, Client 2, and Client $N$ communicate concurrently with zero blocking.

---

## Objectives

- Understand and implement **TCP/IP socket communication** at the transport layer.
- Master core socket lifecycle methods: `socket()`, `bind()`, `listen()`, `accept()`, `recv()`, `sendall()`, and `close()`.
- Eliminate blocking using Python's native `threading` module.
- Manage concurrent client connections safely using thread synchronization (`threading.Lock`).
- Implement clean, user-friendly terminal interfaces for both server and clients.
- Handle common real-world networking errors gracefully (port conflicts, sudden disconnects, offline server).
- Provide an automated test suite verifying all required academic test scenarios.

---

## Technologies Used

| Technology | Category | Purpose |

|---|---|---|
| **Python 3** (3.8+) | Programming Language | Core application logic |
| **`socket` module** | Python Standard Library | Low-level Berkeley Sockets API (TCP/IP) |
| **`threading` module** | Python Standard Library | Concurrency & multi-client thread management |
| **IPv4 (`AF_INET`)** | Network Layer | Addressing scheme (`127.0.0.1` localhost) |
| **TCP (`SOCK_STREAM`)** | Transport Layer | Reliable, ordered, connection-oriented byte stream |
| **Command Line / Terminal** | User Interface | Lightweight, distraction-free execution environment |

*No third-party packages or heavy frameworks (e.g., Flask, Django, Node.js) are used.*

---

## System Architecture

```text
 Client 1 (Terminal 1) ──┐
 Client 2 (Terminal 2) ──┼──> TCP Server (127.0.0.1:5000)
 Client 3 (Terminal 3) ──┘        │
                                  ├── Thread 1 ──> Dedicated handler for Client 1
                                  ├── Thread 2 ──> Dedicated handler for Client 2
                                  └── Thread 3 ──> Dedicated handler for Client 3
```

### Communication Flow

1. **Server Initialization**:
   `socket.socket(AF_INET, SOCK_STREAM)` $\rightarrow$ `bind(('127.0.0.1', 5000))` $\rightarrow$ `listen(5)`.
2. **Accepting Connections**:
   `conn, addr = server_socket.accept()`.
3. **Thread Dispatch**:
   `threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()`.
4. **Data Transmission**:
   Client sends encoded bytes via `sendall()`. The dedicated thread reads them via `recv(1024)`, logs them, and replies with `Server received: <message>`.

---

## Project Folder Structure

```text
Basic-TCP-MultiClient-Server/
│
├── server.py              # Multithreaded TCP server implementation
├── client.py              # TCP client with asynchronous receiver thread
├── test_suite.py          # Automated verification script for all 6 tests
├── launch_demo.bat        # Windows batch script to launch 1 server + 3 clients
├── PRESENTATION.md        # 13-slide viva & project presentation guide
├── README.md              # Comprehensive documentation and viva preparation
├── requirements.txt       # Project requirements & library documentation
├── .gitignore             # Standard git exclusions for Python
└── screenshots/           # Directory for lab report and presentation screenshots
    └── README.md          # Guide on required screenshots
```

---

## Installation & Setup

### Prerequisites

You only need Python 3 installed on your computer.

1. **Verify Python Installation**:

   Open Command Prompt / PowerShell / Terminal and run:

   ```bash
   python --version
   ```

   *Expected output*: `Python 3.x.x` (e.g., Python 3.10, 3.11, 3.12, 3.14).

2. **Navigate to Project Directory**:

   ```bash
   cd "cd "Basic TCP Server with Multi-Client Support""
   ```

3. **Check Dependencies**:
   Since the project uses only the Python standard library, no `pip install` commands are required!

---

## How to Run (Step-by-Step)

To demonstrate multi-client concurrency, open multiple terminal windows:

### Step 1: Start the Server (Terminal 1)

```bash
python server.py
```

*The server will initialize and begin listening on `127.0.0.1:5000`.*

### Step 2: Connect Client 1 (Terminal 2)

```bash
python client.py
```

*Client 1 connects, receives a welcome banner, and displays an input prompt.*

### Step 3: Connect Client 2 (Terminal 3)

```bash
python client.py
```

*Client 2 connects independently. Notice that Server reports `Active connections: 2`.*

### Step 4: Connect Client 3 (Terminal 4)

```bash
python client.py
```

*Client 3 connects. All 3 clients can now send messages simultaneously!*

---

### One-Click Demo on Windows (`launch_demo.bat`)

For quick viva demonstration, simply double-click **`launch_demo.bat`** (or run `.\launch_demo.bat` in PowerShell). It automatically opens 1 Server terminal and 3 Client terminals in tiled windows.

---

## Example Output

### Server Terminal (`server.py`)

```text
==================================================
           TCP MULTI-CLIENT SERVER               
==================================================
[STARTED] Server is listening on 127.0.0.1:5000
[INFO] Waiting for incoming client connections...
[INFO] Press Ctrl+C at any time to stop the server.
==================================================
[CONNECTED] Client ('127.0.0.1', 54210) connected. Active connections: 1
[CLIENT ('127.0.0.1', 54210)] Hello Server
[CONNECTED] Client ('127.0.0.1', 54212) connected. Active connections: 2
[CLIENT ('127.0.0.1', 54212)] How are you?
[BROADCAST from ('127.0.0.1', 54210)] Hello everyone
[CLIENT ('127.0.0.1', 54210)] Sent 'exit' signal.
[DISCONNECTED] Client ('127.0.0.1', 54210) disconnected. Active connections: 1
```

### Client 1 Terminal (`client.py`)

```text
==================================================
            TCP CLIENT APPLICATION               
==================================================
[CONNECTING] Attempting to connect to server at 127.0.0.1:5000...
[CONNECTED] Successfully connected to 127.0.0.1:5000!
--------------------------------------------------
Commands & Usage:
  - Type any message and press Enter to send.
  - Type '/broadcast <message>' to broadcast to all clients.
  - Type 'exit' to disconnect cleanly.
==================================================

[SERVER RESPONSE] [SERVER] Welcome! Connected to TCP Server on 127.0.0.1:5000.
[SERVER] Type any message to receive an echo, or '/broadcast <msg>' to chat with others.
[SERVER] Type 'exit' to disconnect.
Enter message: Hello Server

[SERVER RESPONSE] Server received: Hello Server
Enter message: /broadcast Hello everyone

[SERVER RESPONSE] Server received: Broadcast sent to all active clients.
Enter message: exit
[DISCONNECTED] You have disconnected from the server.
[SESSION ENDED] Client program closed cleanly.
```

### Client 2 Terminal (`client.py`)

```text
Enter message: How are you?

[SERVER RESPONSE] Server received: How are you?
Enter message: 
[SERVER RESPONSE] [BROADCAST from ('127.0.0.1', 54210)]: Hello everyone
Enter message: 
```

---

## Core Features

1. **True Multi-Client Concurrency**: Each connection is handled in an independent thread; one slow or idle client never blocks another.
2. **Reliable TCP Transport**: Uses `SOCK_STREAM` ensuring ordered, guaranteed message delivery.
3. **Clean Terminal Interface**: Formatted banners, timestamps, connection counters, and clear message tags.
4. **Clean Disconnection Flow**: Clients can type `exit` to disconnect cleanly, freeing server resources.
5. **Thread Safety**: Uses `threading.Lock()` to prevent race conditions when updating the connected client registry.
6. **Socket Address Reuse**: Employs `SO_REUSEADDR` to avoid `Address already in use` errors during fast server restarts.
7. **Asynchronous Client Receiver**: The client utilizes a background receiver thread so incoming broadcasts or server notices appear immediately without blocking user keyboard input.

---

## Optional Enhancement: Broadcast Feature

In addition to standard request-response (echo) communication, the server supports real-time **message broadcasting**:

- Any client can type `/broadcast <message>` (e.g., `/broadcast Good morning team!`).
- The server extracts the message and dispatches it to **all other connected clients**.
- The server does not send the broadcast back to the sender, but provides a confirmation acknowledgment: `Server received: Broadcast sent to all active clients.`

---

## Error Handling & Edge Cases

The project incorporates comprehensive error handling to ensure production-like stability:

| Potential Failure | Handled In | How It Is Resolved |

|---|---|---|
| **Port already in use** | `server.py` | Catches `OSError` (WinError 10048 / EADDRINUSE) and displays an informative hint without crashing. |
| **Server is offline** | `client.py` | Catches `ConnectionRefusedError` and instructs the user to start `server.py` first. |
| **Client killed abruptly** (Ctrl+C / closed window) | `server.py` | Catches `ConnectionResetError` / `ConnectionAbortedError`, safely removes the client from registry, and decrements connection count. |
| **Server shutdown** (Ctrl+C on server) | `server.py` | Catches `KeyboardInterrupt`, notifies all connected clients, closes all sockets, and shuts down cleanly. |
| **Invalid hostname / IP** | `client.py` | Catches `socket.gaierror` and prints an address resolution error message. |

---

## Testing Procedure & Automated Test Suite

### Automated Test Suite (`test_suite.py`)

To run all tests automatically in one command:

```bash
python test_suite.py
```

### Manual Test Matrix (All 6 Required Academic Tests)

| Test Case | Scenario | Action | Expected Result | Status |

|---|---|---|---|---|
| **Test 1** | Single Client Connection | Start server, start 1 client, send `"Hello Server"` | Server logs connection, returns `"Server received: Hello Server"`. |  PASS |
| **Test 2** | Two Clients Simultaneously | Connect Client 1 and Client 2 together | Server shows `Active connections: 2`. Both operate independently. |  PASS |
| **Test 3** | Three or More Clients | Connect Client 1, 2, and 3 | Server handles all 3 clients simultaneously without queuing. |  PASS |
| **Test 4** | Different Concurrent Messages | Client 1 sends "Msg A", Client 2 sends "Msg B", Client 3 sends "Msg C" | Each client receives its own exact matching echo response. |  PASS |
| **Test 5** | Single Client Disconnection | Client 1 types `"exit"` | Client 1 disconnects; Server logs disconnect; Client 2 and 3 continue communicating seamlessly. |  PASS |
| **Test 6** | Offline Server Connection | Run `client.py` without starting `server.py` | Client catches `ConnectionRefusedError` and outputs helpful error message without Python crash. |  PASS |

---

## Viva Questions and Answers (20 Questions)

Here are the top 20 questions examiners frequently ask during practical evaluations and project vivas, along with simple, technically precise answers:

### 1. What is TCP?

> **Answer**: TCP (Transmission Control Protocol) is a connection-oriented, reliable transport layer protocol in the TCP/IP suite. It guarantees ordered, error-checked, and complete delivery of data streams between applications using acknowledgments, sequence numbers, and retransmissions.

### 2. What is socket programming?

> **Answer**: Socket programming is a method of enabling two nodes on a computer network to communicate with each other. A socket acts as an endpoint of a two-way communication link between two programs running on the network.

### 3. What is a socket?

> **Answer**: A socket is an abstraction provided by the operating system representing a communication endpoint. It is uniquely identified by the combination of an **IP address** and a **port number** (e.g., `127.0.0.1:5000`).

### 4. Why is TCP used in this project instead of UDP?

> **Answer**: TCP is chosen because this project requires **reliable, lossless, and ordered message delivery**. In messaging and client-server commands, packet loss or scrambled message order is unacceptable. UDP is connectionless and does not guarantee delivery.

### 5. What is the difference between TCP and UDP?

> **Answer**:
>
> - **TCP**: Connection-oriented, establishes connection via 3-way handshake, guarantees delivery, slower due to acknowledgment overhead.
>
> - **UDP**: Connectionless, no handshake, does not guarantee delivery or packet order, faster, ideal for video streaming and online gaming.

### 6. What is an IP address?

> **Answer**: An Internet Protocol (IP) address is a numerical label assigned to every device connected to a computer network that uses the Internet Protocol for communication. It identifies the host and network location (e.g., `127.0.0.1` represents the local loopback address).

### 7. What is a port number?

> **Answer**: A port number is a 16-bit integer (ranging from 0 to 65535) used to identify a specific application or process running on a host computer. While the IP address identifies the machine, the port number identifies the specific process receiving the data.

### 8. What does `bind()` do in socket programming?

> **Answer**: The `bind()` method associates a newly created socket with a specific network interface (IP address) and port number on the host machine. It tells the operating system that incoming traffic on that port belongs to this socket.

### 9. What does `listen()` do?

> **Answer**: The `listen()` method puts the server socket into passive listening mode, enabling it to accept incoming connection requests from clients. It takes a `backlog` parameter specifying the maximum number of pending connections allowed in the queue.

### 10. What does `accept()` do?

> **Answer**: The `accept()` method extracts the first connection request from the listening queue, completes the TCP 3-way handshake, and returns a **new socket object** dedicated exclusively to communicating with that specific client, along with the client's IP and port address tuple `(IP, port)`.

### 11. What does `recv()` do?

> **Answer**: The `recv(buffer_size)` method reads incoming data from the socket's receive buffer up to the specified byte length. It is a blocking call by default. If the peer closes the connection cleanly, `recv()` returns an empty byte string (`b''`).

### 12. What does `send()` or `sendall()` do?

> **Answer**: `send()` transmits byte data across the socket. `sendall()` is a Python convenience method that continues sending bytes from the buffer until all data is transmitted or an error occurs, preventing partial transmission issues.

### 13. Why is multithreading used in this project?

> **Answer**: In a single-threaded server, socket calls like `recv()` and `accept()` are blocking. Multithreading allows the server to handle each client in a separate, concurrent thread of execution so that one client waiting or sending data does not freeze or delay the server for other clients.

### 14. How does the server handle multiple clients simultaneously?

> **Answer**: The main thread runs an infinite loop calling `accept()`. When a client connects, `accept()` returns a client socket. The server wraps this socket inside a new thread target `handle_client` using `threading.Thread(...)` and starts it. The main thread immediately loops back to `accept()`, ready for the next client.

### 15. What happens when a client disconnects?

> **Answer**: When a client closes its socket or sends `"exit"`, the server's `recv()` call returns an empty byte string `b''` or raises `ConnectionResetError`. The server catches this, removes the client from the active client registry inside a thread lock, closes the client socket with `close()`, logs the disconnection, and terminates that client's thread. Other client threads are completely unaffected.

### 16. What is the client-server architecture?

> **Answer**: It is a distributed computing structure that partitions workloads between resource/service providers called **servers** and service requesters called **clients**. Clients initiate communication sessions with servers, which await incoming requests.

### 17. Why is `AF_INET` used?

> **Answer**: `AF_INET` stands for Address Family: Internet. It specifies that the socket will communicate using the **IPv4** addressing protocol (32-bit addresses formatted as dotted-decimal strings like `127.0.0.1`).

### 18. Why is `SOCK_STREAM` used?

> **Answer**: `SOCK_STREAM` specifies the socket type for **TCP**. It indicates a sequenced, reliable, two-way, connection-based byte stream. (In contrast, `SOCK_DGRAM` is used for UDP).

### 19. What happens if two clients connect at the exact same millisecond?

> **Answer**: The operating system maintains a TCP connection backlog queue (configured via `server_socket.listen(backlog)`). The OS kernel handles the TCP 3-way handshakes at the network level and enqueues the connections. The server's main thread then dequeues them sequentially via `accept()` and spawns respective worker threads in milliseconds without dropping either connection.

### 20. What are the limitations of this project, and how can it scale in production?

> **Answer**
>
> - **Thread Overhead**Spawning one operating system thread per client consumes memory and CPU context-switching time. While excellent for tens or hundreds of clients, it does not scale to tens of thousands of concurrent clients (the C10K problem).
> - **Production Solution**: Large-scale production servers use **asynchronous, event-driven I/O** (such as Python's `asyncio` or Linux `epoll`/`selectors`), where a single thread multiplexes thousands of active sockets using an event loop.

---

## Future Scope

1. **Transport Layer Security (SSL/TLS)**: Wrap raw TCP sockets using Python's `ssl` module to provide end-to-end encryption.
2. **Graphical User Interface (GUI)**: Build a desktop chat interface using `tkinter` or `PyQt`.
3. **User Authentication**: Implement user registration, passwords, and session tokens.
4. **Chat Rooms & Private Messaging**: Allow clients to join specific topic channels or whisper to specific IP/usernames.
5. **File Transfer Support**: Implement chunked binary streaming to transfer documents, images, and files over TCP.
6. **AsyncIO Architecture**: Refactor using `asyncio` to achieve high-performance asynchronous networking capable of handling 10,000+ connections.

---

## Presentation Guide

A complete 13-slide presentation outline with slide bullet points and presenter speaking notes is provided in **[`PRESENTATION.md`](file:///C:/Users/Aman%20kumar/.gemini/antigravity/scratch/Basic-TCP-MultiClient-Server/PRESENTATION.md)**. Use it directly to prepare your PowerPoint slides or project presentation deck!
