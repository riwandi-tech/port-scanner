import socket
import argparse
import concurrent.futures
from termcolor import colored


def grab_banner(sock):
    """
    Attempts to read the welcome message (banner) sent by the target service.
    """
    try:
        # Wait to receive up to 1024 bytes of data from the target
        banner = sock.recv(1024).decode().strip()
        return banner
    except Exception:
        # Return an empty string if the target doesn't send a banner
        return ""


def scan_port(ip_address, port):
    """
    Connects to a specific port and grabs its banner if it is open.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((ip_address, port))

        if result == 0:
            # Port is open. Increase timeout slightly to wait for the banner.
            sock.settimeout(2.0)
            banner = grab_banner(sock)

            if banner:
                print(colored(f"[+] Port {port:<5} is OPEN | Service: {banner}", 'green'))
            else:
                print(colored(f"[+] Port {port:<5} is OPEN", 'green'))

        sock.close()
    except Exception:
        pass


def start_scan(target, ports):
    """
    Initializes the scanning process using multithreading for maximum speed.
    """
    print(colored(f"\n[*] Starting scan on target: {target}", 'blue'))

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, ports + 1):
            executor.submit(scan_port, target, port)


def main():
    """
    Parses command-line arguments and triggers the scanning logic.
    """
    parser = argparse.ArgumentParser(description="High-Speed Asynchronous Port Scanner")

    parser.add_argument("-t", "--target", dest="target", required=True,
                        help="Target IP address or domain (use commas for multiple targets)")
    parser.add_argument("-p", "--ports", dest="ports", type=int, default=100,
                        help="Number of ports to scan (default: 100)")

    args = parser.parse_args()

    targets = args.target
    ports = args.ports

    if ',' in targets:
        print(colored("[*] Scanning multiple targets...", 'yellow'))
        for ip in targets.split(','):
            start_scan(ip.strip(), ports)
    else:
        start_scan(targets, ports)


if __name__ == "__main__":
    main()