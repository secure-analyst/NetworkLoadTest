# NetworkLoadTest

**Educational Purpose Only** - Asyncio Network Stress Testing Tool

## ⚠️ DISCLAIMER
FOR AUTHORIZED SECURITY TESTING AND EDUCATIONAL USE ONLY.
USE ONLY ON SYSTEMS YOU OWN OR HAVE EXPLICIT WRITTEN PERMISSION TO TEST.
UNAUTHORIZED USE IS ILLEGAL AND MAY RESULT IN CRIMINAL CHARGES.
THE AUTHOR IS NOT RESPONSIBLE FOR ANY MISUSE, DAMAGE, OR LEGAL CONSEQUENCES.

## Features
- HTTP GET Flood (with proxy and random user agent support)
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

# Installation

## Clone the repository
git clone https://github.com/secure-analyst/NetworkLoadTest.git

## Navigate to the folder
cd NetworkLoadTest

## Install dependencies
pip install -r requirements.txt

# Usage
## HTTP Flood
python NetworkLoadTest.py httpflood --url https://example.com/ --quantity 100 --duration 30 --delay 1 --proxies http://proxy1.com:8080 http://proxy2.com:8080

## UDP Flood
python NetworkLoadTest.py udpflood --target_ip 192.168.1.1 --quantity 200 --duration 45 --port 53

## ICMP Flood
python NetworkLoadTest.py icmpflood --target_ip 192.168.1.1 --quantity 1000 --duration 30 --weight 64

## SYN Flood
python NetworkLoadTest.py synflood --target_ip 192.168.1.1 --quantity 500 --duration 60 --port 80

## TCP Flood
python NetworkLoadTest.py tcpflood --target_ip 192.168.1.1 --quantity 50 --duration 60 --port 443 --timeout 2

# Reference

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
