# PacketLogger

PacketLogger is a lightweight network packet metadata collector built with **Python**, **Scapy**, and **SQLite**. It passively sniffs IPv4 and IPv6 traffic and stores structured packet metadata into a local database for later analysis.

---

## Features

* Live packet sniffing using Scapy
* Supports **IPv4 and IPv6**
* Parses:

  * TCP (ports + flags)
  * UDP (ports)
  * ICMP / ICMPv6
* Stores packet metadata in **SQLite**
* Write-Ahead Logging (WAL) enabled

---

## Project Structure

```
.
├── PacketLogger.py        # Main packet sniffer
├── init_db.py        # Initializes the SQLite database
├── log.db            # SQLite database (created after init)
└── README.md
```

---

## Database Schema

The database contains a single table called `packets` with the following fields:

| Column | Type    | Description                      |
| ------ | ------- | -------------------------------- |
| ts     | REAL    | Packet timestamp (epoch)         |
| src    | TEXT    | Source IP address                |
| dst    | TEXT    | Destination IP address           |
| sport  | INTEGER | Source port (if applicable)      |
| dport  | INTEGER | Destination port (if applicable) |
| proto  | TEXT    | Protocol name                    |
| flags  | TEXT    | TCP flags (TCP only)             |

---

## Requirements

* Python **3+**
* Root / Administrator privileges (required for packet sniffing)

Python dependencies:

```bash
pip install scapy
pip install sqlite3
```

---

## Setup

### 1. Initialize the database

Run the database initialization script:

```bash
python3 init_db.py
```

This will create the `log.db` file and the required tables.

---

### 2. Start the sniffer

```bash
sudo python3 sniffer.py
```

You should see output similar to:

![demo1](https://github.com/user-attachments/assets/12ca0b89-da4f-401f-af85-88128098cdb8)

The sniffer runs continuously until interrupted.

---

## Preview results
You can simply preview the saved metadata by openning log.db

![demo2](https://github.com/user-attachments/assets/10f37e2d-9236-439d-a57a-7c8d4dd85155)


## Future Improvements

Potential enhancements:

* Protocol-specific detection rules
* Rate-based alerts (port scans, floods)
* Web dashboard
* Daemon / system service support
