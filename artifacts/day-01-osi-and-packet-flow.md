# Day 01 Synthesis: OSI Layer Encapsulation & End-to-End Packet Flow
- Date: 2026-09-23
- Domain: 1.1 OSI Architecture & 1.2 Data Link Mechanics

## 1. Technical Mechanics (Deep Breakdown)

Network data transmission operates through systematic encapsulation down the transmitter's protocol stack, physical serialization across a transmission medium, and symmetrical decapsulation up the receiver's stack. 

At Layer 7 through Layer 5 (Application, Presentation, Session), the client application (e.g., an HTTP/2 browser request) generates the raw message payload. When handed down to Layer 4 (Transport), TCP prepends a 20-byte base header containing source and destination port numbers (e.g., ephemeral port 51234 to destination port 443), a 32-bit sequence number, acknowledgement number, window size for flow control, checksum, and control flags (SYN, ACK, PSH, FIN, RST, URG). This unit is now a TCP Segment. If the application payload exceeds the Maximum Segment Size (MSS, typically 1460 bytes for standard 1500-byte MTU Ethernet), TCP segments the data stream into discrete segments.

At Layer 3 (Network), the segment is encapsulated into an IPv4 Packet. The IP header adds another minimum of 20 bytes, detailing the Version (4), IHL (5 words), Type of Service (DSCP/ECN), Total Length, Identification, Flags (DF, MF), Fragment Offset, Time to Live (TTL, typically initialized to 64 or 128), Protocol identifier (0x06 for TCP), Header Checksum, Source IP (e.g., 192.168.1.50), and Destination IP (e.g., 93.184.216.34).

At Layer 2 (Data Link), the packet is encapsulated into an Ethernet II Frame. The layer prepends a 14-byte header consisting of a 6-byte Destination MAC (learned via ARP resolution for the default gateway next-hop router), a 6-byte Source MAC (the sender's NIC hardware address), and a 2-byte EtherType (0x0800 for IPv4). Crucially, Layer 2 appends a 4-byte Frame Check Sequence (FCS) trailer computed via CRC-32 across the frame headers and payload.

At Layer 1 (Physical), the frame is encoded into line symbols (e.g., PAM-5 for 1000BASE-T Gigabit Ethernet over 4 unshielded twisted pairs) with an 8-byte preamble and Start Frame Delimiter (SFD: 10101011) for bit synchronization.

## 2. Architectural ASCII / Topology Diagram

```text
+-----------------------------------------------------------------------------------------+
|                               OSI DATA ENCAPSULATION FLOW                               |
+-----------------------------------------------------------------------------------------+
[ L7-L5: Data ]          [ Application Payload: HTTP/TLS GET Request ]
       |
       v  (Prepend TCP Header: Src/Dst Ports, Seq/Ack, Flags, Window)
[ L4: Segment ]         | TCP Header (20B) |             Data Payload             |
       |
       v  (Prepend IP Header: Src/Dst IPs, TTL, Protocol 0x06)
[ L3: Packet  ]  | IP Hdr (20B) | TCP Header (20B) |      Data Payload             |
       |
       v  (Prepend Ethernet Header: Dst/Src MAC, EtherType 0x0800; Append CRC FCS)
[ L2: Frame   ]  | Eth Hdr (14B) | IP Hdr | TCP Hdr |     Data Payload     | FCS Trailer (4B) |
       |
       v  (Preamble + SFD + Line Encoding: PAM-5 / Manchester / 4B5B)
[ L1: Bits    ]  1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 1 0 1 1 0 0 1 0 1 ... (Physical Medium)
+-----------------------------------------------------------------------------------------+

+-----------------+         Trunk 802.1Q          +-----------------+         Next-Hop
| Workstation Host | ===========================> | Layer 3 Switch  | -----------------> Internet
| 192.168.1.50/24  |   Tagged Frame (VLAN 10)     | Gateway: .1     | (Decrements TTL,
| MAC: aa:bb:cc... |   Preamble + Eth + IP + Data | Routes to WAN   | Rewrites L2 MAC)
+-----------------+                               +-----------------+
```

## 3. Edge Cases & Troubleshooting Scenarios

### Scenario 1: Path MTU Black Hole via DF Bit & Blocked ICMP Type 3 Code 4
- **Failure Mode:** Workstation can initiate a TCP three-way handshake (SYN, SYN-ACK, ACK all under 64 bytes) to an internet server, but any subsequent HTTP/TLS data exchange freezes or times out indefinitely.
- **Root Cause:** An intermediate router or VPN tunnel (e.g., GRE or IPsec) has an MTU lower than 1500 bytes (e.g., 1400 bytes due to encapsulation headers). When the server sends a 1500-byte packet with the `DF` (Don't Fragment) flag set, the bottleneck router discards the packet and attempts to send back an ICMP Type 3 Code 4 ("Destination Unreachable, Fragmentation Needed and DF Set"). However, a misconfigured perimeter firewall drops all ICMP traffic. The server never learns that the packet was dropped, never reduces its segment size, and retransmits until timing out.
- **Diagnostic Steps:**
  1. Test path MTU using ping with DF flag set and buffer sizing:
     `ping -f -l 1472 93.184.216.34` (Windows) or `ping -M do -s 1472 93.184.216.34` (Linux).
  2. Decrement payload size until echo replies return (e.g., 1372 bytes + 28 bytes header = 1400 MTU).
  3. Inspect packet capture in Wireshark for repeated TCP Retransmissions matching the maximum segment size without ACK.
  4. Fix: Enable TCP MSS Clamping on the border router (`ip tcp adjust-mss 1360`) or permit ICMP Type 3 Code 4 transit.

### Scenario 2: Ethernet Duplex Mismatch (Half vs. Full Duplex)
- **Failure Mode:** Network connectivity appears operational for basic ping commands (1 packet/sec), but file transfers suffer severe throughput degradation, link latency spikes, and Wireshark reveals hundreds of TCP Dup ACKs and retransmissions.
- **Root Cause:** Workstation NIC is manually set to 100 Mbps Full Duplex, while the connected switch port is left on Auto-Negotiation. Under IEEE 802.3u, if auto-negotiation fails to detect partner capabilities (parallel detection fallback), the switch defaults to Half Duplex. The workstation transmits frames whenever it wants (Full Duplex), while the switch listens for carrier and collision detect (CSMA/CD). When the switch is receiving while transmitting, it interprets it as a collision, aborts, and sends a 32-bit jam signal.
- **Diagnostic Steps:**
  1. Inspect switch port interface statistics: `show interfaces GigabitEthernet0/1`. Look for rising counters of **Late Collisions** (collisions occurring after the first 64 bytes of transmission) and **FCS / CRC Alignment Errors**.
  2. Inspect workstation interface: `netstat -e` or `ethtool eth0` to check negotiated duplex.
  3. Fix: Configure both ends to Auto-Negotiation (`speed auto`, `duplex auto`), or manually hard-code both ends to 100/Full.
