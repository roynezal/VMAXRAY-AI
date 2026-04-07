@echo off
cd /d C:\vmaxray

start "VMAXRAY-ChatServer" cmd /k python vmaxray_chat_server_LATEST_FOR_WIN7.py >> server.log 2>&1

timeout /t 6 /nobreak

start "VMAXRAY-Tunnel" cmd /k python vmaxray_tunnel_win7.py >> tunnel.log 2>&1

echo VMAXRAY started. Check tunnel.log for status.
