#!/bin/bash
cd /home/live/VMAXRAY/vmax_web_chat

python vmaxcode >> /var/log/vmaxcode.log 2>&1 &
sleep 5
python /home/live/VMAXRAY/vmaxray_tunnel_minios.py >> /var/log/vmaxray_tunnel.log 2>&1 &

echo "VMAXCODE started on port 8081"
echo "Tunnel running"
