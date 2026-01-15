#!/usr/bin/env python3
from scapy.all import (
    sniff, IP, IPv6, TCP, UDP, ICMP, ICMPv6EchoRequest, ICMPv6EchoReply
)
from datetime import datetime
import sqlite3

DB = "ids.db"

conn = sqlite3.connect(DB, check_same_thread=False)
cur = conn.cursor()

cur.execute("PRAGMA journal_mode=WAL;")
conn.commit()


def insert_event(ev):
    cur.execute("""
        INSERT INTO packets (ts, src, dst, sport, dport, proto, flags)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        ev["ts"],
        ev["src"],
        ev["dst"],
        ev["sport"],
        ev["dport"],
        ev["proto"],
        ev["flags"]
    ))
    conn.commit()


def packet_callback(pkt):

    if not (IP in pkt or IPv6 in pkt): #only IPv4 and IPv6 will be processed
        return

    ev = {
        "ts": pkt.time,
        "src": None,
        "dst": None,
        "sport": None,
        "dport": None,
        "proto": None,
        "flags": None,
    }

    # ---------- IPv4 ----------
    if IP in pkt:
        ip = pkt[IP]
        ev["src"] = ip.src
        ev["dst"] = ip.dst
        proto = ip.proto

        if proto == 6 and TCP in pkt:
            ev["proto"] = "TCP"
            tcp = pkt[TCP]
            ev["sport"] = tcp.sport
            ev["dport"] = tcp.dport
            ev["flags"] = str(tcp.flags)

        elif proto == 17 and UDP in pkt:
            ev["proto"] = "UDP"
            udp = pkt[UDP]
            ev["sport"] = udp.sport
            ev["dport"] = udp.dport

        elif proto == 1 and ICMP in pkt:
            ev["proto"] = "ICMP"

        else:
            ev["proto"] = str(proto)

    # ---------- IPv6 ----------
    elif IPv6 in pkt:
        ip6 = pkt[IPv6]
        ev["src"] = ip6.src
        ev["dst"] = ip6.dst
        nh = ip6.nh

        if nh == 6 and TCP in pkt:
            ev["proto"] = "TCP"
            tcp = pkt[TCP]
            ev["sport"] = tcp.sport
            ev["dport"] = tcp.dport
            ev["flags"] = tcp.sprintf("%TCP.flags%")

        elif nh == 17 and UDP in pkt:
            ev["proto"] = "UDP"
            udp = pkt[UDP]
            ev["sport"] = udp.sport
            ev["dport"] = udp.dport

        elif nh == 58:
            ev["proto"] = "ICMPv6"

        else:
            ev["proto"] = str(nh)

    insert_event(ev)

    print(ev)


def main():
    print("Sniffer started. Writing to ids.db")
    sniff(prn=packet_callback, store=False)


if __name__ == "__main__":
    main()
