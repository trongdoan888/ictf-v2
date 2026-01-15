#!/bin/bash
GB_ID=$(sudo docker ps -qf "name=gamebot")

echo "[+] Dang khoi dong Dashboard..."
sudo docker exec -d $GB_ID python3 /opt/ictf/gamebot/ictf_final_web.py

echo "[+] Dang khoi dong Gamebot..."
sudo docker exec -d $GB_ID python3 /opt/ictf/gamebot/nckh_gamebot.py

echo "[+] Dang khoi dong Worker..."
sudo docker exec -d $GB_ID python3 /opt/ictf/gamebot/manual_worker.py

echo "[!] Tat ca he thong da san sang!"
