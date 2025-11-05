# NetworkLoadTest

**Educational Purpose Only** - Asyncio Network Stress Testing Tool

## ⚠️ DISCLAIMER
This tool is for authorized security testing and educational purposes ONLY.
Use only on systems you own or have explicit written permission to test.
Unauthorized use may be illegal and violate terms of service.
The author is not responsible for any misuse, damage, or legal consequences.

## Features
- HTTP GET Flood (with proxy support)
- ICMP Flood (raw ICMP packet flooding)
- TCP Flood (TCP connection exhaustion)
- UDP Flood (UDP packet bombardment)
- SYN Flood (TCP SYN packet flooding)
- Cross-platform support (Windows, Linux, macOS)
"ip spoofing is available with syn, icmp, and udp"

## Requirements
- Python 3.8+
- aiohttp
- requests
- scapy

## Installation

# Clone the repository
git clone https://github.com/secure-analyst/NetworkLoadTest.git

# Navigate to the folder
cd NetworkLoadTest

# Install dependencies
pip install -r requirements.txt

## Usage
# HTTP flood
python NetworkLoadTest.py httpflood --url https://example.com/ --quantity 100 --duration 30 --delay 1 --proxies http://proxy1.com:8080 http://proxy2.com:8080

# UDP flood
python NetworkLoadTest.py udpflood --target_ip 192.168.1.1 --quantity 200 --duration 45 --port 53

# ICMP flood
python NetworkLoadTest.py icmpflood --target_ip 192.168.1.1 --quantity 1000 --duration 30 --weight 64

# SYN flood
python NetworkLoadTest.py synflood --target_ip 192.168.1.1 --quantity 500 --duration 60 --port 80

# TCP flood
python NetworkLoadTest.py tcpflood --target_ip 192.168.1.1 --quantity 50 --duration 60 --port 443 --timeout 2

## Reference

HTTPFLOOD
---------
usage: NetworkLoadTest.py httpflood [-h] --url URL [--quantity QUANTITY] [--duration DURATION] [--delay DELAY]
                                    [--proxies PROXIES [PROXIES ...]] [--timeout TIMEOUT]

options:
  -h, --help            show this help message and exit
  --url URL             target url
  --quantity QUANTITY   number of requests per bunch
  --duration DURATION   duration of the attack(in seconds)
  --delay DELAY         delay after each bunch
  --proxies PROXIES [PROXIES ...]
                        List of proxy URLs
  --timeout TIMEOUT     http request timeout
[edor@archlinux NetworkLoadTest]$ 

UDPFLOOD
--------
usage: NetworkLoadTest.py udpflood [-h] --target_ip TARGET_IP [--quantity QUANTITY] [--weight WEIGHT] [--delay DELAY]
                                   [--duration DURATION] [--src SRC] [--port PORT] [--ttl TTL]

options:
  -h, --help            show this help message and exit
  --target_ip TARGET_IP
                        target ip
  --quantity QUANTITY   number of requests per bunch
  --weight WEIGHT       packet size
  --delay DELAY         delay after each bunch
  --duration DURATION   duration of the attack(in seconds)
  --src SRC             source ip (random by default)
  --port PORT           destination port
  --ttl TTL             time to live for packets


TCPFLOOD
--------

usage: NetworkLoadTest.py tcpflood [-h] --target_ip TARGET_IP [--port PORT] [--quantity QUANTITY] [--delay DELAY]
                                   [--duration DURATION] [--timeout TIMEOUT]

options:
  -h, --help            show this help message and exit
  --target_ip TARGET_IP
                        target ip
  --port PORT           target port
  --quantity QUANTITY   number of connections
  --delay DELAY         delay after each bunch
  --duration DURATION   duration of the attack(in seconds)
  --timeout TIMEOUT     tcp connection timeout

SYNFLOOD
--------

usage: NetworkLoadTest.py synflood [-h] [--weight WEIGHT] --target_ip TARGET_IP [--quantity QUANTITY] [--delay DELAY]
                                   [--src SRC] [--duration DURATION] [--port PORT] [--ttl TTL]

options:
  -h, --help            show this help message and exit
  --weight WEIGHT       packet size
  --target_ip TARGET_IP
                        target ip
  --quantity QUANTITY   number of requests per bunch
  --delay DELAY         delay after each bunch
  --src SRC             source ip (random by default)
  --duration DURATION   duration of the attack(in seconds)
  --port PORT           destination port
  --ttl TTL             time to live for packets

ICMPFLOOD
---------

usage: NetworkLoadTest.py icmpflood [-h] --quantity QUANTITY --target_ip TARGET_IP [--src SRC] [--duration DURATION]
                                    [--weight WEIGHT] [--delay DELAY] [--ttl TTL]

options:
  -h, --help            show this help message and exit
  --quantity QUANTITY   number of requests per bunch
  --target_ip TARGET_IP
                        target ip
  --src SRC             source ip (random by default)
  --duration DURATION   duration of the attack(in seconds)
  --weight WEIGHT       packet size
  --delay DELAY         delay after each bunch
  --ttl TTL             time to live for packets
