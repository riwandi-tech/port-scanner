import socket
import argparse
import concurrent.futures
from termcolor import colored


def grab_banner(sock, port):
    """
    Smart banner grabbing functionality.
    Uses a combination of Null Probes and Protocol-Specific Payloads
    to elicit responses from both active and passive services.
    """
    try:
        # Phase 1: Null Probe
        # Wait briefly to see if the service sends a welcome message automatically (e.g., SSH, FTP)
        sock.settimeout(2.0)

        try:
            # Attempt to receive data without sending anything first
            banner = sock.recv(1024).decode().strip()
            if banner:
                return banner.split('\n')[0]  # Return only the first line for clean output
        except socket.timeout:
            # If the service is silent, move to Phase 2 (Targeted Probing)
            pass

            # Phase 2: Targeted Probes
        # Send specific payloads based on common port numbers to wake up passive services
        if port in [80, 443, 8080, 8443]:
            # Send a standard HTTP GET request for web servers
            sock.send(b"GET / HTTP/1.1\r\n\r\n")
        else:
            # Send a generic newline payload for other passive services
            sock.send(b"\r\n\r\n")

            # Catch the response triggered by our probe
        banner = sock.recv(1024).decode().strip()
        return banner.split('\n')[0]

    except Exception:
        # Return an empty string if no banner can be retrieved or connection drops
        return ""


def scan_port(ip_address, port, output_file):
    """
    Core scanning mechanism for a single port.
    Attempts a TCP connection and triggers banner grabbing if open.
    """
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a very short timeout (0.5s) to quickly skip filtered or closed ports
        sock.settimeout(0.5)

        # connect_ex returns 0 if the connection is successful (port is open)
        result = sock.connect_ex((ip_address, port))

        if result == 0:
            # Port is open: execute smart banner grabbing
            banner = grab_banner(sock, port)

            # Format the output string
            if banner:
                report_text = f"[+] Port {port:<5} is OPEN | Service: {banner}"
            else:
                report_text = f"[+] Port {port:<5} is OPEN"

            # Print the formatted result to the terminal in green
            print(colored(report_text, 'green'))

            # If the user provided an output file, append the result to it
            if output_file:
                # 'a' mode (append) ensures we don't overwrite previous lines
                with open(output_file, "a") as file:
                    file.write(report_text + "\n")

        # Always close the socket to free up system resources
        sock.close()
    except Exception:
        # Silently ignore errors like connection resets or unreachable hosts
        pass


def start_scan(target, ports, output_file):
    """
    Manages the concurrent execution of port scans.
    Deploys multiple threads to scan ports simultaneously for massive speed gains.
    """
    print(colored(f"\n[*] Starting scan on target: {target}", 'blue'))

    # Use ThreadPoolExecutor to run up to 100 threads concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, ports + 1):
            # Submit each port scanning task to the thread pool
            executor.submit(scan_port, target, port, output_file)


def main():
    """
    Entry point of the script.
    Handles command-line interface (CLI) arguments and initializes the scan.
    """
    parser = argparse.ArgumentParser(description="High-Speed Asynchronous Port Scanner")

    # Define CLI arguments
    parser.add_argument("-t", "--target", dest="target", required=True,
                        help="Target IP address or domain (use commas for multiple targets)")
    parser.add_argument("-p", "--ports", dest="ports", type=int, default=100,
                        help="Number of ports to scan (default: 100)")
    parser.add_argument("-o", "--output", dest="output",
                        help="Save the scan results to a text file (e.g., results.txt)")

    args = parser.parse_args()

    targets = args.target
    ports = args.ports
    output_file = args.output

    # Check if the user inputted multiple targets separated by commas
    if ',' in targets:
        print(colored("[*] Scanning multiple targets...", 'yellow'))
        for ip in targets.split(','):
            # Remove extra spaces and start scanning each target
            start_scan(ip.strip(), ports, output_file)
    else:
        # Start scanning a single target
        start_scan(targets, ports, output_file)


if __name__ == "__main__":
    # Execute the main function only if this script is run directly
    main()