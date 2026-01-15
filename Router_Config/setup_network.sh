#!/bin/bash
# Bat IP Forwarding
sudo sysctl -w net.ipv4.ip_forward=1
# NAT Internet tu ens33 sang ens37
sudo iptables -t nat -A POSTROUTING -o ens33 -j MASQUERADE
# Mo thong cac cong quan trong
sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 5000 -j ACCEPT
sudo iptables -P FORWARD ACCEPT
echo "Cau hinh mang Router hoan tat!"
