
# **Note:** This project has been moved to my [Custom-Security-Tools](https://github.com/riwandi-tech/Custom-Security-Tools/tree/main/port-scanner) for better management.

---

# ⚡ Async Python Port Scanner

A high-speed, concurrent TCP port scanner built with Python. Designed for penetration testers and network administrators who need rapid reconnaissance with intelligent banner grabbing capabilities.

## 🚀 Features

- **High-Speed Execution:** Utilizes `concurrent.futures.ThreadPoolExecutor` to scan hundreds of ports concurrently.
- **Smart Banner Grabbing:**
  - **Phase 1 (Passive):** Employs Null Probes to safely identify polite services (SSH, FTP) without triggering
    alarms.
  - **Phase 2 (Active):** Deploys protocol-specific payloads to elicit responses from passive services (e.g., HTTP Web
    Servers).
- **Multi-Target Support:** Scan multiple IP addresses or domains in a single command.
- **Output Routing:** Save your reconnaissance data cleanly into a text report.

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/riwandi-tech/Custom-Security-Tools.git
   ```

2. **Navigate to the tool's directory:**

   ```bash
   cd Custom-Security-Tools/port-scanner
   ```

3. **Create a virtual environment (Recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Use the `-h` or `--help` flag to see all available options.

```bash
python scanner.py --help
```

**Example 1: Fast scan on a single target (100 ports)**

```bash
python scanner.py -t scanme.nmap.org -p 100
```

**Example 2: Scan multiple targets and save the output to a file**

```bash
python scanner.py -t 127.0.0.1,scanme.nmap.org -p 50 -o final_report.txt
```

## ⚠️ Disclaimer

This tool is created for educational purposes and authorized penetration testing only. Do not use this tool against
systems you do not own or have explicit permission to test. The author is not responsible for any misuse or damage
caused by this program.
