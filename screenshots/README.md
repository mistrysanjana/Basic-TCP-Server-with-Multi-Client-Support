# Screenshots Directory

This directory is reserved for capturing and saving terminal screenshots for your project report, lab manual, and viva presentation.

## Recommended Screenshots to Capture

1. **`01_server_startup.png`**
   - Shows `python server.py` starting up on `127.0.0.1:5000` waiting for connections.

2. **`02_single_client_connect.png`**
   - Shows a client connecting, receiving the welcome message, and sending `"Hello Server"`.
   - Shows the corresponding log on the server terminal.

3. **`03_multi_client_split_screen.png`**
   - Split-screen view with 1 Server terminal and 3 Client terminals running concurrently.
   - Shows each client sending distinct messages and getting independent responses without blocking.

4. **`04_broadcast_feature.png`**
   - Shows Client 1 sending `/broadcast Hello everyone!`.
   - Shows Client 2 and Client 3 receiving the broadcast packet instantly.

5. **`05_client_disconnect.png`**
   - Shows Client 1 typing `exit` and disconnecting cleanly.
   - Shows the server logging the disconnection and updating the active connection count while other clients remain active.

6. **`06_automated_tests_pass.png`**
   - Shows the execution of `python test_suite.py` with all 6 tests passing.

---

### Tip for College Demonstrations

Arrange your terminal windows in a 2x2 grid on Windows:

- Top-Left: **Server**
- Top-Right: **Client 1**
- Bottom-Left: **Client 2**
- Bottom-Right: **Client 3**

This visually proves multi-client concurrency in a single screen!
