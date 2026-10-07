"""
=============================================================================
Test Suite : Comprehensive Automated Verification for TCP Multi-Client Server
File Name  : test_suite.py
Description: Runs all 6 core tests and additional feature tests against
             server.py and client.py socket routines.
=============================================================================
"""

import socket
import subprocess
import sys
import time
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def run_tests():
    print("=" * 60)
    print("STARTING AUTOMATED TEST SUITE FOR TCP MULTI-CLIENT SERVER")
    print("=" * 60)

    # -------------------------------------------------------------
    # TEST 6: Client attempts connection when server is NOT running
    # -------------------------------------------------------------
    print("\n[TEST 6] Testing connection failure when server is offline...")
    try:
        dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy_sock.settimeout(2.0)
        dummy_sock.connect((SERVER_HOST, SERVER_PORT))
        print("[-] FAIL: Server was already running or port open!")
        dummy_sock.close()
        sys.exit(1)
    except (ConnectionRefusedError, socket.timeout, OSError) as e:
        print(f"[+] PASS (Test 6): Connection properly refused when server offline ({type(e).__name__}).")

    # Start the server process
    print("\n[SETUP] Starting server.py in background...")
    server_proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(1.0)  # Wait for server socket to bind & listen

    try:
        # -------------------------------------------------------------
        # TEST 1: Single client connection & communication
        # -------------------------------------------------------------
        print("\n[TEST 1] Single client connects and sends message...")
        c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c1.connect((SERVER_HOST, SERVER_PORT))
        welcome1 = c1.recv(1024).decode("utf-8")
        assert "Welcome" in welcome1, f"Unexpected welcome message: {welcome1}"
        print(f"    Client 1 received welcome banner.")

        c1.sendall("Hello Server".encode("utf-8"))
        res1 = c1.recv(1024).decode("utf-8")
        assert res1 == "Server received: Hello Server", f"Unexpected response: {res1}"
        print(f"    Client 1 received expected echo: '{res1}'")
        print("[+] PASS (Test 1): Single client communication succeeded.")

        # -------------------------------------------------------------
        # TEST 2 & 3: Multiple clients connect simultaneously (3 clients)
        # -------------------------------------------------------------
        print("\n[TEST 2 & 3] Two and three clients connect simultaneously...")
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect((SERVER_HOST, SERVER_PORT))
        welcome2 = c2.recv(1024).decode("utf-8")

        c3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c3.connect((SERVER_HOST, SERVER_PORT))
        welcome3 = c3.recv(1024).decode("utf-8")

        print("    Client 2 and Client 3 connected successfully.")
        print("[+] PASS (Test 2 & 3): 3 simultaneous connections established.")

        # -------------------------------------------------------------
        # TEST 4: Clients send different messages concurrently
        # -------------------------------------------------------------
        print("\n[TEST 4] Clients send distinct messages concurrently...")
        c1.sendall("Client 1 message: Status check".encode("utf-8"))
        c2.sendall("Client 2 message: Computational data".encode("utf-8"))
        c3.sendall("Client 3 message: Ping 123".encode("utf-8"))

        r1 = c1.recv(1024).decode("utf-8")
        r2 = c2.recv(1024).decode("utf-8")
        r3 = c3.recv(1024).decode("utf-8")

        assert r1 == "Server received: Client 1 message: Status check"
        assert r2 == "Server received: Client 2 message: Computational data"
        assert r3 == "Server received: Client 3 message: Ping 123"

        print(f"    c1 reply: '{r1}'")
        print(f"    c2 reply: '{r2}'")
        print(f"    c3 reply: '{r3}'")
        print("[+] PASS (Test 4): All clients communicated independently without blocking.")

        # -------------------------------------------------------------
        # TEST 7 (Broadcast Enhancement): Client 1 broadcasts to c2 & c3
        # -------------------------------------------------------------
        print("\n[TEST 7] Testing Broadcast feature...")
        c1.sendall("/broadcast Hello everyone from Client 1!".encode("utf-8"))
        c1_ack = c1.recv(1024).decode("utf-8")
        assert "Broadcast sent" in c1_ack, f"Unexpected broadcast ack: {c1_ack}"

        c2_bcast = c2.recv(1024).decode("utf-8")
        c3_bcast = c3.recv(1024).decode("utf-8")

        assert "Hello everyone from Client 1!" in c2_bcast
        assert "Hello everyone from Client 1!" in c3_bcast
        print(f"    Client 2 received broadcast: '{c2_bcast.strip()}'")
        print(f"    Client 3 received broadcast: '{c3_bcast.strip()}'")
        print("[+] PASS (Test 7): Broadcast successfully reached peer clients.")

        # -------------------------------------------------------------
        # TEST 5: One client disconnects while others stay connected
        # -------------------------------------------------------------
        print("\n[TEST 5] Client 1 sends 'exit' to disconnect...")
        c1.sendall("exit".encode("utf-8"))
        c1.close()
        time.sleep(0.5)

        # Verify c2 and c3 are still operational
        c2.sendall("Are you still there, Server?".encode("utf-8"))
        r2_after = c2.recv(1024).decode("utf-8")
        assert r2_after == "Server received: Are you still there, Server?"

        c3.sendall("Client 3 still active!".encode("utf-8"))
        r3_after = c3.recv(1024).decode("utf-8")
        assert r3_after == "Server received: Client 3 still active!"

        print(f"    Client 2 response after Client 1 disconnected: '{r2_after}'")
        print(f"    Client 3 response after Client 1 disconnected: '{r3_after}'")
        print("[+] PASS (Test 5): Client 1 disconnected; other clients remained connected.")

        # Cleanup remaining clients
        c2.sendall("exit".encode("utf-8"))
        c2.close()
        c3.sendall("exit".encode("utf-8"))
        c3.close()
        time.sleep(0.5)

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED SUCCESSFULLY! (6/6 Core Tests + Broadcast)")
        print("=" * 60)

    finally:
        # Terminate server process cleanly
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            server_proc.kill()


if __name__ == "__main__":
    run_tests()
