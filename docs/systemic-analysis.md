# CompTIA Network+ (N10-009) Comprehensive Knowledge Architecture: Systemic Analysis & Operational Reference

This document encapsulates the authoritative systemic analysis, multidimensional architectural behaviors, and deep operational frameworks from the CompTIA Network+ (N10-009) curriculum.

---

## 1. CompTIA Seven-Step Network Troubleshooting Methodology

CompTIA establishes a structured, seven-step troubleshooting methodology that guides engineers through diagnosing, isolating, resolving, and documenting complex network disruptions.

| Step Number & Title | Primary Operational Objectives & Diagnostic Tasks | Operational Risks of Non-Compliance |
| :--- | :--- | :--- |
| **Step 1: Identify the Problem** | Gather detailed symptoms, question end users, determine scope, review change records, and duplicate faults safely. Establish scope: single host, entire subnet, IDF, or core backbone. | Acting on incomplete information leads to misdiagnosed root causes and wasted troubleshooting effort. |
| **Step 2: Establish a Theory of Probable Cause** | Evaluate common failure modes, apply structured OSI models (top-down, bottom-up, divide-and-conquer), and question the obvious. | Jumping directly to conclusions without broad evaluation introduces confirmation bias and prolongs outages. |
| **Step 3: Test the Theory to Determine Cause** | Execute non-destructive diagnostics to validate hypotheses; systematically re-evaluate or escalate when theories are disproved. | Making unverified production changes during the testing phase can cause unexpected secondary outages. |
| **Step 4: Establish a Plan of Action & Identify Potential Effects** | Design a detailed implementation sequence, assess cross-system risks (STP recalculations, routing adjacencies, database locks), draft rollback procedures, and secure change approvals. | Unplanned production modifications trigger cascading failures across dependent infrastructure components. |
| **Step 5: Implement the Solution or Escalate as Necessary** | Methodically execute the approved configuration changes modifying one variable at a time, or escalate issues beyond administrative/skill thresholds. | Changing multiple variables at once obscures which adjustment resolved the issue or introduced new errors. |
| **Step 6: Verify Full System Functionality & Apply Preventative Controls** | Confirm complete end-to-end service restoration with end users, monitor telemetry baselines, and deploy hardening controls (e.g. BPDU Guard, DHCP Snooping). | Restoring link-level connectivity without verifying services leaves dependent business applications broken. |
| **Step 7: Document Findings, Actions, and Outcomes** | Update ticketing databases, change management systems, logical/physical network diagrams, and IPAM repositories. | Undocumented resolutions lead to recurring troubleshooting cycles and outdated infrastructure records. |

### Diagnostic Investigation Strategies
- **Bottom-Up:** Starts at Layer 1 (physical media, link lights, cable certs) before checking Layer 2 switching and Layer 3 routing. Ideal when physical installation changes or hardware faults are suspected.
- **Top-Down:** Starts at Layer 7 (application daemons, HTTP status codes, DNS resolution) before evaluating transport mechanisms. Best suited when link connectivity is verified but specific software operations fail.
- **Divide-and-Conquer:** Starts at Layer 3 using utilities like `ping` or `traceroute`. A successful ping to the gateway verifies physical cabling, framing, and ARP, focusing troubleshooting on upper layers.

---

## 2. Mathematical Mechanics of IPv4 Subnetting, VLSM Design, and Route Summarization

### Core Subnetting Equations
$$\text{Created Subnets} = 2^n \quad (\text{where } n = \text{borrowed network bits})$$
$$\text{Usable Hosts per Subnet} = 2^h - 2 \quad (\text{where } h = \text{remaining host bits})$$
$$\text{Magic Number (Block Size)} = 256 - \text{Decimal Mask in Target Octet} = 2^{(8-b)}$$

### Dotted Decimal Subnet Mask & Block Size Table (/24 to /32)
| CIDR Prefix | Dotted Decimal Subnet Mask | Altered Octet | Magic Number (Block Size) | Total IP Addresses | Usable Host Capacity |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **/24** | 255.255.255.0 | 4th Octet | 256 | 256 | 254 |
| **/25** | 255.255.255.128 | 4th Octet | 128 | 128 | 126 |
| **/26** | 255.255.255.192 | 4th Octet | 64 | 64 | 62 |
| **/27** | 255.255.255.224 | 4th Octet | 32 | 32 | 30 |
| **/28** | 255.255.255.240 | 4th Octet | 16 | 16 | 14 |
| **/29** | 255.255.255.248 | 4th Octet | 8 | 8 | 6 |
| **/30** | 255.255.255.252 | 4th Octet | 4 | 4 | 2 (Point-to-Point WAN) |
| **/31** | 255.255.255.254 | 4th Octet | 2 | 2 | 2 (RFC 3021 Point-to-Point) |
| **/32** | 255.255.255.255 | 4th Octet | 1 | 1 | 1 (Host Loopback Interface) |

### Variable Length Subnet Masking (VLSM) Allocation Walkthrough
**Rule:** Subnets must always be allocated from **largest host requirement to smallest** to prevent address space fragmentation and overlap.

**Scenario:** Given allocated block `10.50.4.0/24`:
1. **Tier 1 - Systems Engineering (55 hosts required):**
   $2^h - 2 \ge 55 \implies h = 6$ host bits ($2^6 - 2 = 62$ hosts). Prefix: $32 - 6 = \mathbf{/26}$ (Mask: `255.255.255.192`, Block size: 64).
   - Network: `10.50.4.0/26`
   - Usable Hosts: `10.50.4.1` – `10.50.4.62`
   - Broadcast: `10.50.4.63`
2. **Tier 2 - Corporate Sales (26 hosts required):**
   $2^h - 2 \ge 26 \implies h = 5$ host bits ($2^5 - 2 = 30$ hosts). Prefix: $32 - 5 = \mathbf{/27}$ (Mask: `255.255.255.224`, Block size: 32).
   - Network: `10.50.4.64/27`
   - Usable Hosts: `10.50.4.65` – `10.50.4.94`
   - Broadcast: `10.50.4.95`
3. **Tier 3 - Facilities Infrastructure (10 hosts required):**
   $2^h - 2 \ge 10 \implies h = 4$ host bits ($2^4 - 2 = 14$ hosts). Prefix: $32 - 4 = \mathbf{/28}$ (Mask: `255.255.255.240`, Block size: 16).
   - Network: `10.50.4.96/28`
   - Usable Hosts: `10.50.4.97` – `10.50.4.110`
   - Broadcast: `10.50.4.111`
4. **Tier 4 - Point-to-Point Uplink (2 hosts required):**
   $2^h - 2 \ge 2 \implies h = 2$ host bits ($2^2 - 2 = 2$ hosts). Prefix: $32 - 2 = \mathbf{/30}$ (Mask: `255.255.255.252`, Block size: 4).
   - Network: `10.50.4.112/30`
   - Usable Hosts: `10.50.4.113` – `10.50.4.114`
   - Broadcast: `10.50.4.115`
5. **Reserved / Unallocated Space:** `10.50.4.116` through `10.50.4.255` preserved for growth.

### CIDR Route Summarization
Contiguous routing entries are collapsed into a single supernet advertisement to reduce router memory overhead and prevent link flap cascades:
- `172.16.8.0/24` $\to$ Third octet: `00001 000`
- `172.16.9.0/24` $\to$ Third octet: `00001 001`
- `172.16.10.0/24` $\to$ Third octet: `00001 010`
- `172.16.11.0/24` $\to$ Third octet: `00001 011`
First 16 bits (`172.16`) match + 5 bits (`00001`) match = **21 common bits**.  
**Summarized Route:** `172.16.8.0/21` (Mask: `255.255.248.0`, covering `172.16.8.0` through `172.16.15.255`).

---

## 3. Dynamic Routing Fabric, Administrative Distance, and Path Determination

### Path Determination Hierarchy
1. **Longest Prefix Match:** Always takes precedence over Administrative Distance and metric. A `/24` route is always chosen over a `/16` or `/8` route regardless of protocol.
2. **Administrative Distance (AD):** Breaks ties when multiple protocols advertise identical prefix lengths to the same destination. Lower numerical value = higher believability.
3. **Metric:** Breaks ties when routes are learned from the same protocol with identical prefix length. Equal metrics trigger Equal-Cost Multi-Path (ECMP) load balancing.

### Default Administrative Distance (AD) Reference Table
| Routing Source / Protocol | Default AD | Protocol Classification | Metric Mechanics |
| :--- | :---: | :--- | :--- |
| **Connected Interface** | **0** | Hardware State | Direct physical link status |
| **Static Route** | **1** | Manual Configuration | Administratively assigned next-hop |
| **External BGP (eBGP)** | **20** | Path Vector | AS-Path length, Local Pref, MED |
| **Internal EIGRP** | **90** | Advanced Distance Vector | Composite: Bandwidth + Delay |
| **Open Shortest Path First (OSPF)** | **110** | Link-State | Cumulative Cost = $10^8 / \text{bandwidth}$ |
| **IS-IS** | **115** | Link-State | Cumulative arbitrary integer cost |
| **Routing Information Protocol (RIP)** | **120** | Distance Vector | Hop count (max 15; 16 = unreachable) |
| **External EIGRP** | **170** | Advanced Distance Vector | Composite metric for redistributed routes |
| **Internal BGP (iBGP)** | **200** | Path Vector | BGP path attributes within single AS |
| **Gateway of Last Resort** | **Fallback** | Default Route | Matches `0.0.0.0/0` traffic |

---

## 4. Enterprise Switching Dynamics: Trunking, STP, and Link Aggregation

### IEEE 802.1Q Frame Tag Structure (4 Bytes / 32 Bits)
- **TPID (Tag Protocol Identifier):** 16-bit field set to `0x8100`.
- **PCP (Priority Code Point):** 3-bit Class of Service (CoS) for Layer 2 QoS prioritization.
- **DEI (Drop Eligible Indicator):** 1-bit flag marking frames eligible for drop during congestion.
- **VID (VLAN Identifier):** 12-bit field supporting up to 4,096 VLANs (0 and 4095 reserved; 1 to 4094 usable).

### Native VLAN Security
- **Native VLAN Mismatch:** Connected trunk ports configured with divergent native VLANs leak traffic across broadcast domains and trigger STP error states.
- **Double-Tagging Attack:** Attacker crafts frame with two 802.1Q tags. When the switch strips the outer native VLAN tag, the frame is delivered untagged across the trunk, and the next switch forwards the inner tag into a restricted VLAN, bypassing L3 firewalls.
- **Mitigation:** Change Native VLAN from default `1` to an unused VLAN ID (e.g. `999`), and explicitly enable 802.1Q native VLAN tagging (`vlan dot1q tag native`).

### Spanning Tree Protocol (STP) Standards
| Standard | IEEE Spec | Convergence Time | Port States | Key Mechanics |
| :--- | :---: | :---: | :--- | :--- |
| **Classic STP** | 802.1D | 30 – 50 sec | Blocking $\to$ Listening $\to$ Learning $\to$ Forwarding | Static timers: 20s Max Age, 15s Forward Delay |
| **Rapid STP (RSTP)** | 802.1w | Milliseconds | Discarding $\to$ Learning $\to$ Forwarding | Proactive Proposal-Agreement handshakes |
| **Multiple STP (MSTP)** | 802.1s | Milliseconds | Discarding $\to$ Learning $\to$ Forwarding | Maps multiple VLANs into distinct spanning tree instances |

### Link Aggregation Control Protocol (LACP: IEEE 802.3ad / 802.1ax)
- Bundles physical interfaces into logical Port-Channels without triggering STP blocking.
- Modes: **Active** (proactively initiates LACP negotiation) and **Passive** (responds to LACP requests). Two passive ends will fail to aggregate.
- Frame distribution: Hashing algorithms based on Layer 2 MAC, Layer 3 IP, or Layer 4 port pairings ensure frames within the same conversation maintain sequence order.

---

## 5. Modern Datacenter Architectures: Spine-and-Leaf, VXLAN, and SDN

### Three-Tier vs. Two-Tier Spine-and-Leaf (Clos) Architecture
| Domain | Three-Tier Hierarchical | Two-Tier Spine-and-Leaf (Clos) |
| :--- | :--- | :--- |
| **Hierarchy** | Access, Distribution, and Core tiers | Leaf (Access/ToR) and Spine (Fabric Backbone) tiers |
| **Traffic Optimization** | North-South perimeter client-to-server traffic | East-West lateral server-to-server cluster traffic |
| **Forwarding Protocol** | Spanning Tree Protocol (STP); blocks links | Layer 3 routing with Equal-Cost Multi-Path (ECMP) |
| **Latency Profile** | Variable depending on network traversal depth | Deterministic, single-hop latency between any two leaf switches |
| **Scalability** | Limited by distribution switch uplink port capacity | Linearly scalable by adding spine switches |

### VXLAN Overlay (RFC 7348)
- Encapsulates Layer 2 Ethernet frames inside Layer 4 UDP datagrams on destination **UDP port 4789**.
- Replaces 12-bit VLAN IDs with **24-bit VXLAN Network Identifiers (VNIs)**, expanding segmentation space from 4,096 to over **16 million** logical broadcast domains.
- Terminated by **VXLAN Tunnel Endpoints (VTEPs)** residing on hardware switches or hypervisor virtual switches.

### Software-Defined Networking (SDN) Planes
- **Management Plane:** Administrative CLI, GUI, scripting, SNMP, telemetry monitoring.
- **Control Plane:** Routing table computation, protocol adjacencies (OSPF, BGP, STP), path resolution.
- **Data Plane:** High-speed ASIC hardware forwarding, frame switching, and packet decapsulation.
- **SDN Controller:** Decouples the control plane into a centralized controller that directs forwarding nodes via Southbound APIs (OpenFlow, NETCONF, RESTCONF).
- **SD-WAN:** Application-aware WAN routing across hybrid transports (MPLS, Broadband, LTE/5G) with Zero-Touch Provisioning (ZTP).

---

## 6. Enterprise Security Architecture & Layer 2 Defensive Hardening

### Zero-Trust Architecture (ZTA, NIST SP 800-207)
Replaces perimeter castle-and-moat models with three core pillars:
1. **Microsegmentation:** Small, protected security zones containing breaches and blocking lateral attacker movement.
2. **Continuous Adaptive Verification:** Session-long validation of device health, patch level, and user anomalies.
3. **Least-Privilege Enforcement:** Strictly restricting user and service rights to the minimum necessary functions.

### IEEE 802.1X Port-Based Network Access Control (PNAC)
- **Supplicant:** Client software endpoint requesting network access.
- **Authenticator:** Edge switch or wireless AP holding port in unauthorized state, permitting only EAPoL traffic.
- **Authentication Server:** RADIUS or TACACS+ server validating credentials against Active Directory / LDAP.
- **EAP Flavors:**
  - **EAP-TLS:** Mutual certificate authentication (both client and server present X.509 digital certs). Highest security.
  - **PEAP:** Server certificate terminates TLS tunnel; inner MS-CHAPv2 validates client credentials.
  - **EAP-TTLS:** Server certificate tunnel supporting broader inner authentication protocols.

### Layer 2 Threat & Defensive Hardening Matrix
| Threat Vector | Attack Mechanics | Defensive Configuration |
| :--- | :--- | :--- |
| **CAM Table Exhaustion (MAC Flooding)** | Attacker floods switch with bogus source MACs to fill CAM table, causing switch to fail open as hub. | **Port Security:** Restricts permitted MAC count, enables `mac-address sticky`, and sets violation to `errdisable`. |
| **DHCP Starvation & Rogue DHCP** | Attacker exhausts DHCP scope and deploys rogue DHCP server to intercept gateway/DNS. | **DHCP Snooping:** Configures trusted vs. untrusted ports; drops DHCP server offers on untrusted interfaces. |
| **ARP Poisoning (On-Path Attack)** | Attacker broadcasts fraudulent ARP replies associating their MAC with the gateway IP. | **Dynamic ARP Inspection (DAI):** Intercepts and validates ARP packets against the DHCP Snooping database. |
| **STP Root Hijacking** | Rogue switch advertises Bridge Priority 0 to seize Root Bridge status and redirect traffic. | **BPDU Guard** (err-disables PortFast ports receiving BPDUs) and **Root Guard** (prevents downstream root election). |

---

## 7. High Availability (FHRP) and Disaster Recovery

### First Hop Redundancy Protocols (FHRP)
| Protocol | Standard | Roles & Operation | Virtual MAC Signature | Preemption |
| :--- | :--- | :--- | :--- | :--- |
| **HSRP** | Cisco Proprietary (RFC 2281) | Active router forwards; Standby monitors via hello packets. | `0000.0c07.acXX` (v1) / `0000.0c9f.fXXX` (v2) | Disabled by default |
| **VRRP** | IETF Open Standard (RFC 5798) | Master router forwards; one or more Backup routers monitor. | `00-00-5E-00-01-XX` (IPv4) / `00-00-5E-00-02-XX` (IPv6) | Enabled by default |
| **GLBP** | Cisco Proprietary | Active Virtual Gateway (AVG) answers ARPs; up to 4 Active Virtual Forwarders (AVFs) forward simultaneously. | `0007.b400.XXYY` | Balances traffic via round-robin, host-dependent, or weighted algorithms |

### Disaster Recovery Site Classifications
| Site Classification | Facilities & Equipment Readiness | Data Synchronization State | RTO Profile | RPO Profile | Relative Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cold Site** | Space, power, cooling ready; no hardware installed | No data pre-loaded; requires full restoration from backup archives | Extended: Days to Weeks | High data loss window: Days to Weeks | Low capital expenditure |
| **Warm Site** | Hardware, switches, and servers pre-racked and connected | Periodic backup sync; lacks live database mirroring | Moderate: Hours to Days | Moderate: Hours to 1 Day | Moderate ongoing operational cost |
| **Hot Site (Active-Passive)** | Fully provisioned operational infrastructure on standby | Near-real-time data replication | Minutes to 1 Hour | Seconds to Minutes | High ongoing maintenance cost |
| **Hot Site (Active-Active)** | Redundant, load-balanced production clusters across sites | Real-time synchronous replication across both environments | Near-zero: Instantaneous automated failover | Near-zero: Zero transactional data loss | Maximum capital & operational investment |
