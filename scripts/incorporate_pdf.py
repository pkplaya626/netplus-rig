#!/usr/bin/env python3
"""
Incorporates the 40-page CompTIA Network+ Comprehensive Knowledge Architecture PDF
into data/cards.json, data/reviews.json, and data/questions.json.
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(__file__).resolve().parent.parent

# 1. Load existing cards
cards_path = repo_root / "data" / "cards.json"
reviews_path = repo_root / "data" / "reviews.json"
questions_path = repo_root / "data" / "questions.json"

with open(cards_path, "r", encoding="utf-8") as f:
    cards = json.load(f)

with open(reviews_path, "r", encoding="utf-8") as f:
    reviews = json.load(f)

with open(questions_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

existing_ids = {c["id"] for c in cards}

new_cards = [
  {
    "id": "n10-009-0156",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.2 Ports & Protocols",
    "front": "What port and protocol does Kerberos use, and what is its operational function in Active Directory?",
    "back": "TCP/UDP port 88. Enterprise authentication based on symmetric key cryptography and Key Distribution Center (KDC) ticket granting (TGT/TGS), serving as default Active Directory authentication.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0157",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.2 Ports & Protocols",
    "front": "What port does Microsoft SQL Server operate on by default?",
    "back": "TCP port 1433. Relational database client query protocol utilized for structured enterprise data operations.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0158",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.2 Ports & Protocols",
    "front": "What ports and transport protocols are used by Session Initiation Protocol (SIP) for VoIP signaling in cleartext vs encrypted mode?",
    "back": "Port 5060 (TCP/UDP) for cleartext SIP VoIP signaling; Port 5061 (TCP) for SIP over TLS (encrypted multimedia signaling).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0159",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.1 OSI Model",
    "front": "What are the core functions, data formats, and technologies of Layer 6 (Presentation) in the OSI model?",
    "back": "PDU: Data. Handles character encoding/translation (ASCII, Unicode), data compression/formatting (JPEG, GIF, MPEG), and cryptographic TLS/SSL encryption and decryption processes.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0160",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.1 OSI Model",
    "front": "What are the core functions and representative protocols of Layer 5 (Session) in the OSI model?",
    "back": "PDU: Data. Establishes, controls, checkpoints, and terminates dialogues and communication sessions between local and remote applications. Protocols: RPC, NetBIOS, SQL Sockets, NFS, Named Pipes.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0161",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.1 OSI Model",
    "front": "What are the two distinct sublayers of Layer 2 (Data Link) and their respective functions?",
    "back": "1. LLC (Logical Link Control, IEEE 802.2): Interacts with Layer 3 Network layer, handles flow control, error checking, and frame multiplexing.\n2. MAC (Media Access Control): Controls hardware physical addressing (48-bit MAC) and media access rules (CSMA/CD, CSMA/CA).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0162",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.1 TCP Connection Establishment",
    "front": "Detail the byte/packet-level exchange and architectural significance of the TCP three-way handshake.",
    "back": "Sequence: SYN (client ISN) -> SYN-ACK (server ISN, ACK client ISN+1) -> ACK (client ACK server ISN+1). Establishes Transmission Control Blocks (TCBs), synchronizes initial sequence numbers, and negotiates Maximum Segment Size (MSS) and window scale.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0163",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.1 TCP Connection Termination",
    "front": "What is the four-step sequence for graceful TCP connection teardown and why is it structured this way?",
    "back": "Sequence: FIN -> ACK (from receiver), then FIN -> ACK (from sender). Coordinates full-duplex session termination, ensuring both communication endpoints independently flush and close their respective transmission buffers.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0164",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.1 Copper Media",
    "front": "What is Direct Attach Copper (DAC) cabling and where is it typically deployed?",
    "back": "Factory-integrated twinaxial copper cable assembly with fixed SFP+ or QSFP transceivers (1 to 7 meters). Delivers high-speed (up to 100 Gbps), ultra-low latency, and low cost for intra-rack top-of-rack switch-to-server interconnects.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0165",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.1 Cable Installation",
    "front": "Compare Plenum-rated (CMP) vs Riser-rated (CMR) cabling in fire rating and installation criteria.",
    "back": "Plenum (CMP): Jacketed in low-smoke, low-flame Fluorinated Ethylene Polymer (FEP). Mandated by fire safety codes in drop ceilings and raised floors acting as environmental air return ducts.\nRiser (CMR): Flame-retardant PVC engineered to prevent vertical fire spread through floor penetrations; strictly forbidden in plenum air handling spaces.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0166",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.1 Transceiver Types",
    "front": "Differentiate the supported port speeds and physical density profiles of SFP, SFP+, QSFP+, and QSFP28 transceivers.",
    "back": "SFP: Up to 1 Gbps (standard modular Gigabit).\nSFP+: Up to 10 Gbps (shares standard SFP footprint).\nQSFP / QSFP+: 40 Gbps (bundles 4 x 10 Gbps lanes for datacenter uplinks).\nQSFP28: 100 Gbps (bundles 4 x 25 Gbps lanes for modern spine-and-leaf switches).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0167",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.2 Wireless Standards",
    "front": "Compare legacy Wi-Fi standards 802.11b, 802.11a, and 802.11g in frequency, maximum theoretical speed, and modulation.",
    "back": "802.11b: 2.4 GHz, 11 Mbps, DSSS / CCK, 20 MHz channel.\n802.11a: 5 GHz, 54 Mbps, OFDM, 20 MHz channel.\n802.11g: 2.4 GHz, 54 Mbps, OFDM, 20 MHz channel.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0168",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.2 Wireless Standards",
    "front": "Compare 802.11n (Wi-Fi 4) and 802.11ac (Wi-Fi 5) in frequency bands, modulation, and maximum theoretical speeds.",
    "back": "Wi-Fi 4 (802.11n): 2.4 & 5 GHz, up to 600 Mbps, MIMO (up to 4 spatial streams), 64-QAM, 20/40 MHz channels.\nWi-Fi 5 (802.11ac): 5 GHz only, up to 6.93 Gbps, Downlink MU-MIMO, 256-QAM, channel widths up to 80/160 MHz.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0169",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.2 Wireless Architecture",
    "front": "What are the non-overlapping channels in the 2.4 GHz spectrum in North America (FCC) and why does channel overlap cause issues?",
    "back": "Channels 1, 6, and 11 (each spaced 25 MHz apart with 20 MHz channel widths). Deploying adjacent APs on overlapping channels (e.g. 2, 3, 4, 5) creates adjacent-channel interference (ACI), collisions, and packet retries.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0170",
    "domain": "4.0 Network Security",
    "subdomain": "4.4 Wireless Security",
    "front": "What architectural vulnerability affects WPA2-Personal (PSK) and how does WPA3-Personal resolve it?",
    "back": "WPA2-Personal uses a single PSK vulnerable to offline dictionary brute-force attacks via captured 4-way EAPOL handshakes.\nWPA3-Personal replaces PSK with Simultaneous Authentication of Equals (SAE / Dragonfly handshake), providing forward secrecy and rendering captured handshakes useless for offline cracking.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0171",
    "domain": "4.0 Network Security",
    "subdomain": "4.2 Network Access Control",
    "front": "Explain the three functional entities of 802.1X Network Access Control and its security benefits over WPA-Personal.",
    "back": "Entities: Supplicant (client software), Authenticator (switch/AP permitting only EAPoL traffic until authed), Authentication Server (RADIUS/TACACS+).\nBenefits: Eliminates shared pre-shared keys, authenticates individual user directory accounts, and generates dynamic per-user/per-session encryption keys.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0172",
    "domain": "4.0 Network Security",
    "subdomain": "4.1 Authentication Protocols",
    "front": "Differentiate EAP-TLS, PEAP, and EAP-TTLS authentication mechanisms in certificate requirements.",
    "back": "EAP-TLS: Requires mutual authentication where BOTH the server and client validate each other via X.509 digital certificates (highest security).\nPEAP: Only the server presents an X.509 certificate to establish an encrypted TLS tunnel; client authenticates via username/password (MS-CHAPv2).\nEAP-TTLS: Server presents a certificate tunnel; supports multiple inner client authentication methods.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0173",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.3 IPv4 Addressing",
    "front": "What is the IPv4 Multicast address range (Class D) and what protocols manage multicast routing?",
    "back": "224.0.0.0/4 (224.0.0.0 to 239.255.255.255, RFC 5771). Delivers one-to-many communications without broadcasting; routed by multicast protocols such as PIM (Protocol Independent Multicast) and managed locally via IGMP.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0174",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.4 IPv6 Autoconfiguration",
    "front": "Explain how IPv6 Stateless Address Autoconfiguration (SLAAC) and EUI-64 generate a 128-bit address.",
    "back": "SLAAC: Host receives a 64-bit network prefix via ICMPv6 Router Advertisements (RA) from local routers.\nEUI-64: Host generates its 64-bit Interface ID by splitting its 48-bit MAC address in half, inserting 16-bit 0xFFFE in the middle, and inverting the 7th bit (Universal/Local bit). (e.g. 00:11:22:33:44:55 -> 0211:22ff:fe33:4455).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0175",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.2 CLI Utilities",
    "front": "What is the purpose of running `ping -f -l 1472 <IP>` on Windows?",
    "back": "Discovers Path MTU without fragmentation. `-f` sets the DF (Don't Fragment) bit; `-l 1472` specifies 1472 bytes of ICMP payload. Adding 20 bytes IP header + 8 bytes ICMP header = exactly 1500 bytes (standard Ethernet MTU).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0176",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.2 CLI Utilities",
    "front": "Explain the syntax and purpose of Windows `tracert -d` and Linux `traceroute -n -T`.",
    "back": "Windows `tracert -d`: Skips reverse DNS lookup for each hop, accelerating path tracing.\nLinux `traceroute -n -T`: `-n` skips DNS resolution, and `-T` sends TCP SYN packets to port 80/443 instead of UDP, successfully traversing firewalls that drop UDP probes.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0177",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.2 CLI Utilities",
    "front": "What specific outputs are provided by `netstat -ano` versus `netstat -r`?",
    "back": "`netstat -ano`: Displays all active connections and listening ports numerically (-n) alongside their Process Identifiers (PID, -o).\n`netstat -r`: Displays the host operating system's local Layer 3 IPv4/IPv6 routing table.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0178",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.2 CLI Utilities",
    "front": "What does the `+trace` option do in the BIND `dig` utility?",
    "back": "Performs iterative, hierarchical DNS resolution starting from the 13 Root DNS servers (root hints), following delegation down to TLD (.com) servers, and finally querying authoritative nameservers, displaying full response times and delegation flags.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0179",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.4 Packet Analysis",
    "front": "In `tcpdump -i eth0 -nn -s 0 port 80 -w capture.pcap`, what do the `-nn` and `-s 0` flags accomplish?",
    "back": "`-nn`: Prevents protocol and port name resolution (keeps IP addresses and ports numeric to avoid DNS delays).\n`-s 0`: Sets snaplen to 0 (captures the entire packet payload without truncation for Wireshark inspection).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0180",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.2 CLI Utilities",
    "front": "What is `iperf3` used for and what does `iperf3 -c <IP> -u -b 100M` measure?",
    "back": "Measures throughput and network performance between client and server endpoints.\n`-c <IP>`: Client mode targeting server.\n`-u`: Tests UDP datagrams instead of TCP.\n`-b 100M`: Sets target bandwidth to 100 Mbps, measuring UDP jitter, packet loss, and out-of-order delivery.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0181",
    "domain": "3.0 Network Operations",
    "subdomain": "3.5 Disaster Recovery",
    "front": "Differentiate MTBF (Mean Time Between Failures) and MTTR (Mean Time to Repair).",
    "back": "MTBF: Quantifies equipment reliability by calculating the average operating time between unexpected hardware breakdowns.\nMTTR: Measures maintainability and service recovery speed by calculating the average time required to diagnose, repair, and restore a failed system to production.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0182",
    "domain": "3.0 Network Operations",
    "subdomain": "3.5 Disaster Recovery",
    "front": "Differentiate Recovery Time Objective (RTO) and Recovery Point Objective (RPO) in disaster recovery.",
    "back": "RTO (Recovery Time Objective): Maximum acceptable duration of service downtime before operational harm occurs (Time limit to restore).\nRPO (Recovery Point Objective): Maximum acceptable threshold of data loss measured in time backwards from disruption (Data age acceptable to lose).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0183",
    "domain": "3.0 Network Operations",
    "subdomain": "3.2 Network Monitoring",
    "front": "Compare SNMPv1/v2c security with SNMPv3 User-Based Security Model (USM).",
    "back": "SNMPv1/v2c: Uses clear-text 'community strings' (public/private) for authorization with zero payload encryption or integrity checks.\nSNMPv3: Introduces USM supporting authPriv mode, providing HMAC-MD5/SHA message integrity/authentication and CBC-DES/AES packet encryption.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0184",
    "domain": "5.0 Network Troubleshooting",
    "subdomain": "5.3 Troubleshooting Methodology",
    "front": "When should an engineer employ Bottom-Up, Top-Down, or Divide-and-Conquer troubleshooting?",
    "back": "Bottom-Up (L1->L7): Suspected physical cabling, transceiver, or switchport link light issues.\nTop-Down (L7->L1): Connectivity is intact but specific applications, DNS lookups, or HTTP APIs fail.\nDivide-and-Conquer (L3 first): Starts with gateway ping; success immediately rules out L1/L2 and ARP, isolating faults to L4-L7.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0185",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.3 IPv4 Subnetting",
    "front": "What is the golden rule when creating a Variable Length Subnet Masking (VLSM) addressing plan?",
    "back": "Subnets must ALWAYS be allocated starting from the LARGEST host requirement down to the SMALLEST host requirement. Violating this rule causes overlapping boundaries and fragmented, unusable IP address blocks.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0186",
    "domain": "3.0 Network Operations",
    "subdomain": "3.1 Routing Protocols",
    "front": "Explain the 'Longest Prefix Match' rule in Layer 3 IP routing.",
    "back": "A router always forwards packets matching the route with the most specific (highest) prefix length (e.g., /24 beats /16 and /8), regardless of whether another route has a lower Administrative Distance or better metric.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0187",
    "domain": "3.0 Network Operations",
    "subdomain": "3.1 Routing Protocols",
    "front": "Order these routing sources by Administrative Distance from most preferred (lowest AD) to least: Static, OSPF, eBGP, RIP, Connected, EIGRP (internal).",
    "back": "1. Connected (0)\n2. Static (1)\n3. External BGP / eBGP (20)\n4. Internal EIGRP (90)\n5. OSPF (110)\n6. RIP (120)",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0188",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.3 Switching & VLANs",
    "front": "What are the 4 sub-fields within a 32-bit (4-byte) IEEE 802.1Q VLAN tag?",
    "back": "1. TPID (16 bits): Tag Protocol ID, set to 0x8100.\n2. PCP (3 bits): Priority Code Point, marks Class of Service (CoS) for L2 QoS.\n3. DEI (1 bit): Drop Eligible Indicator, marks frames drop-eligible during congestion.\n4. VID (12 bits): VLAN ID, supporting up to 4,096 VLANs (1-4094 usable).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0189",
    "domain": "4.0 Network Security",
    "subdomain": "4.2 Port Security",
    "front": "How does an 802.1Q Double-Tagging Attack work and how is it mitigated?",
    "back": "Attack: Attacker sends frame with two 802.1Q tags where the outer tag matches the trunk's Native VLAN. The first switch strips the outer tag and sends the frame untagged. The second switch reads the inner tag and forwards it into a restricted target VLAN, bypassing firewalls.\nMitigation: Change Native VLAN from default 1 to an unused VLAN ID and force tagging on native traffic (vlan dot1q tag native).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0190",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.3 Spanning Tree",
    "front": "How is the Spanning Tree Protocol (STP) Root Bridge elected?",
    "back": "Switches exchange BPDUs containing their Bridge ID (BID). The BID consists of Bridge Priority (default 32,768 in steps of 4,096) + base MAC address. The switch with the lowest numerical BID is elected Root Bridge.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0191",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.3 Spanning Tree",
    "front": "Compare Classic STP (802.1D) vs Rapid STP (802.1w) in convergence time and transition mechanisms.",
    "back": "Classic STP (802.1D): 30-50 seconds convergence; relies on static timers (20s Max Age, 15s Forward Delay across Blocking, Listening, Learning, Forwarding).\nRapid STP (802.1w): Millisecond convergence; replaces static timers with proactive Proposal-Agreement handshakes across Discarding, Learning, and Forwarding states.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0192",
    "domain": "2.0 Network Implementation",
    "subdomain": "2.3 Link Aggregation",
    "front": "What happens if two switch interfaces connected via an Ethernet trunk are both configured in LACP Passive mode?",
    "back": "The link will FAIL to aggregate into a Port-Channel. In Passive mode, a port responds to LACP packets but never initiates negotiation. At least one end must be configured in Active mode for LACP trunking to establish.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0193",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 Datacenter Architecture",
    "front": "Explain the cabling topology and traffic advantages of a Spine-and-Leaf (Clos) datacenter architecture.",
    "back": "Topology: Every Leaf switch connects to every Spine switch in a full mesh. Leaf switches never connect to leaf switches, and spine switches never connect to spine switches.\nAdvantages: Optimized for East-West server-to-server traffic; provides deterministic, predictable single-hop latency between any two servers using Layer 3 ECMP load balancing.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0194",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 Network Overlays",
    "front": "What transport protocol, destination port, and identifier does VXLAN utilize?",
    "back": "Transport: UDP destination port 4789. Uses a 24-bit VXLAN Network Identifier (VNI) supporting over 16 million logical segments (compared to 4,096 in 802.1Q). Terminated by VXLAN Tunnel Endpoints (VTEPs) over Layer 3 IP underlays.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0195",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 Software-Defined Networking",
    "front": "Differentiate the Management, Control, and Data planes in Software-Defined Networking (SDN).",
    "back": "Management Plane: Admin interfaces (SSH, HTTPS, API, SNMP).\nControl Plane: Routing logic, topology calculation, and path tables (OSPF, BGP, STP); centralized in the SDN controller.\nData Plane: High-speed hardware packet forwarding and frame switching via ASICs.\nCommunication uses Southbound APIs (OpenFlow, NETCONF, RESTCONF).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0196",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 SD-WAN",
    "front": "What is SD-WAN and what does Zero-Touch Provisioning (ZTP) accomplish?",
    "back": "SD-WAN: Application-aware software overlay aggregating hybrid WAN links (MPLS, broadband, 5G) into an encrypted fabric with dynamic traffic steering.\nZTP (Zero-Touch Provisioning): Allows newly connected edge branch appliances to automatically boot, fetch configurations, download policies, and register certificates with zero manual on-site engineer configuration.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0197",
    "domain": "4.0 Network Security",
    "subdomain": "4.1 Zero-Trust Architecture",
    "front": "What are the three core operational pillars of Zero-Trust Architecture (NIST SP 800-207)?",
    "back": "1. Microsegmentation (isolating workloads into granular security zones to prevent lateral movement).\n2. Continuous Adaptive Verification (session-long assessment of device health, user context, and anomalies).\n3. Least-Privilege Enforcement (strictly limiting access to the minimum permissions required).",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0198",
    "domain": "4.0 Network Security",
    "subdomain": "4.2 Layer 2 Hardening",
    "front": "Map these 4 Layer 2 attacks to their primary switch mitigation: MAC Flooding, Rogue DHCP, ARP Poisoning, STP Hijacking.",
    "back": "1. MAC Flooding (CAM exhaustion) -> Port Security (mac-address sticky, errdisable).\n2. Rogue DHCP / Starvation -> DHCP Snooping (trusted vs untrusted ports).\n3. ARP Poisoning (MitM) -> Dynamic ARP Inspection (DAI, checks DHCP snooping DB).\n4. STP Hijacking -> BPDU Guard (shuts down PortFast ports receiving BPDUs) and Root Guard.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0199",
    "domain": "3.0 Network Operations",
    "subdomain": "3.3 High Availability",
    "front": "Compare HSRP, VRRP, and GLBP in standard status, preemption defaults, and load-balancing capabilities.",
    "back": "HSRP: Cisco proprietary; Active/Standby; preemption disabled by default; virtual MAC 0000.0c07.acXX.\nVRRP: IETF open standard (RFC 5798); Master/Backup; preemption ENABLED by default; virtual MAC 00-00-5E-00-01-XX.\nGLBP: Cisco proprietary; Active Virtual Gateway (AVG) assigns up to 4 Active Virtual Forwarders (AVFs), providing true active-active load balancing.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  },
  {
    "id": "n10-009-0200",
    "domain": "3.0 Network Operations",
    "subdomain": "3.5 Disaster Recovery",
    "front": "Compare Cold Site, Warm Site, and Hot Site (Active-Active) in readiness, RTO, and RPO.",
    "back": "Cold Site: Space/power/cooling only, no hardware, days-to-weeks RTO, high data loss RPO, lowest cost.\nWarm Site: Hardware pre-racked, periodic backups (no live mirror), hours-to-days RTO and RPO, moderate cost.\nHot Site (Active-Active): Redundant live clusters, synchronous replication, near-zero instantaneous RTO and zero transactional data loss RPO, highest cost.",
    "repetitions": 0, "interval": 1, "easeFactor": 2.5, "dueDate": "2026-09-23"
  }
]

# Append only cards not already present
added_count = 0
for c in new_cards:
    if c["id"] not in existing_ids:
        cards.append(c)
        existing_ids.add(c["id"])
        added_count += 1
        # Add to reviews.json
        reviews.setdefault("cards", {})[c["id"]] = {
            "repetitions": 0,
            "interval": 1,
            "easeFactor": 2.5,
            "dueDate": "2026-09-23",
            "history": []
        }

print(f"Added {added_count} new flashcards from PDF. Total deck size: {len(cards)}")

# Save updated cards & reviews
with open(cards_path, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2)

with open(reviews_path, "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=2)

# 2. Add new domain diagnostic questions derived from the PDF
new_questions = [
  {
    "id": "q-109",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 Modern Datacenter Architectures",
    "question": "A network architect designs a datacenter fabric optimized for high-volume East-West container communication with deterministic, single-hop latency between any two servers. Which topology and load-balancing mechanism should be deployed?",
    "options": [
      "Traditional Three-Tier Hierarchical with Spanning Tree Protocol",
      "Two-Tier Spine-and-Leaf (Clos) architecture with Layer 3 ECMP routing",
      "Collapsed Core topology with 802.1D Spanning Tree timers",
      "Ring topology with Token Passing arbitration"
    ],
    "correctIndex": 1,
    "explanation": "In a Spine-and-Leaf (Clos) topology, every Leaf switch connects to every Spine switch in a full mesh. Traffic between any two servers experiences a single hop across the spine layer, utilizing Layer 3 ECMP for load balancing."
  },
  {
    "id": "q-110",
    "domain": "1.0 Networking Concepts",
    "subdomain": "1.5 Network Overlays",
    "question": "An enterprise requires extending Layer 2 broadcast domains across a routed Layer 3 IP backbone, expanding beyond the 4,096 VLAN limitation to support multi-tenant isolation. What technology and transport protocol does this?",
    "options": [
      "802.1Q Tagging over TCP port 80",
      "VXLAN (RFC 7348) using UDP destination port 4789 with a 24-bit VNI",
      "GRE without IPsec over IP protocol 47",
      "MPLS LDP using TCP port 646"
    ],
    "correctIndex": 1,
    "explanation": "Virtual Extensible LAN (VXLAN) encapsulates Ethernet frames inside UDP datagrams using destination port 4789. It uses a 24-bit VXLAN Network Identifier (VNI) to support over 16 million logical broadcast domains."
  },
  {
    "id": "q-307",
    "domain": "3.0 Network Operations",
    "subdomain": "3.1 Routing Principles",
    "question": "A router routing table contains the following entries: 10.0.0.0/8 (Connected, AD 0), 10.20.0.0/16 (Static, AD 1), and 10.20.30.0/24 (BGP, AD 20). A packet arrives destined for IP 10.20.30.55. Which route will the router select to forward the packet?",
    "options": [
      "10.0.0.0/8 because Connected routes have the lowest Administrative Distance (AD 0)",
      "10.20.0.0/16 because Static routes are manually configured",
      "10.20.30.0/24 because Longest Prefix Match (/24) takes absolute precedence over Administrative Distance",
      "The router drops the packet due to conflicting routing sources"
    ],
    "correctIndex": 2,
    "explanation": "The Longest Prefix Match rule is the fundamental decision rule in Layer 3 IP forwarding. The route with the most specific prefix (/24) always wins, regardless of Administrative Distance."
  },
  {
    "id": "q-308",
    "domain": "3.0 Network Operations",
    "subdomain": "3.3 High Availability",
    "question": "A network administrator inspects an ARP table on a client workstation and notices the default gateway MAC address is 00-00-5E-00-01-0A. What first-hop redundancy protocol is in operation?",
    "options": [
      "HSRPv1",
      "HSRPv2",
      "VRRP for IPv4",
      "GLBP"
    ],
    "correctIndex": 2,
    "explanation": "VRRP for IPv4 uses the standard IETF virtual MAC address format 00-00-5E-00-01-XX (where XX represents the VRRP group ID in hex, here 0A = group 10). HSRPv1 uses 0000.0c07.acXX, and GLBP uses 0007.b400.XXYY."
  },
  {
    "id": "q-408",
    "domain": "4.0 Network Security",
    "subdomain": "4.2 Layer 2 Attacks",
    "question": "What switchport security mitigation prevents a malicious host from crafting frames with two 802.1Q tags to bypass firewall inspection and hop into a restricted VLAN via the Native VLAN?",
    "options": [
      "Configure the Native VLAN to an unused VLAN ID (e.g. 999) and enable explicit native tagging",
      "Enable Dynamic Trunking Protocol (DTP) on all access ports",
      "Set STP Bridge Priority to 0",
      "Configure Half Duplex on trunk interfaces"
    ],
    "correctIndex": 0,
    "explanation": "To prevent 802.1Q Double-Tagging Attacks, security best practices mandate changing the Native VLAN from default 1 to an unused VLAN ID and forcing explicit native tagging (`vlan dot1q tag native`) so the outer tag is never stripped untagged."
  },
  {
    "id": "q-409",
    "domain": "4.0 Network Security",
    "subdomain": "4.2 Layer 2 Hardening",
    "question": "A rogue laptop connected to an access port begins broadcasting gratuitous ARP replies associating its MAC address with the default gateway IP. Which switch feature will intercept and drop these malicious ARP packets?",
    "options": [
      "BPDU Guard",
      "Dynamic ARP Inspection (DAI)",
      "Storm Control",
      "Root Guard"
    ],
    "correctIndex": 1,
    "explanation": "Dynamic ARP Inspection (DAI) intercepts all ARP requests and responses on untrusted ports, validating the IP-to-MAC bindings against the trusted database created by DHCP Snooping."
  }
]

existing_q_ids = {q["id"] for q in questions}
q_added = 0
for q in new_questions:
    if q["id"] not in existing_q_ids:
        questions.append(q)
        existing_q_ids.add(q["id"])
        q_added += 1

with open(questions_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)

print(f"Added {q_added} new questions. Total diagnostic questions pool: {len(questions)}")
