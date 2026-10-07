@echo off
:: =============================================================================
:: Quick Demo Launcher for College Presentation & Viva
:: Launches 1 Server and 3 Client terminal windows automatically
:: =============================================================================
echo ===================================================
echo   Launching TCP Server with Multi-Client Support
echo ===================================================
echo Starting Server Window...
start "TCP Server" cmd /k "python server.py"

:: Wait 2 seconds for server to bind & listen
timeout /t 2 /nobreak >nul

echo Starting Client 1 Window...
start "TCP Client 1" cmd /k "python client.py"

timeout /t 1 /nobreak >nul

echo Starting Client 2 Window...
start "TCP Client 2" cmd /k "python client.py"

timeout /t 1 /nobreak >nul

echo Starting Client 3 Window...
start "TCP Client 3" cmd /k "python client.py"

echo ===================================================
echo All 4 windows launched successfully!
echo You can now send messages between clients and server.
echo ===================================================
pause
