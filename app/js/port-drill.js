/**
 * Port Speed Trial Engine for CompTIA Network+ (N10-009)
 * Covers all required ports from the Comprehensive Knowledge Architecture,
 * reaction latency in milliseconds, and high-accuracy rapid-fire matching.
 */

export const CORE_PORTS = [
  { port: 20, proto: "TCP", service: "FTP Data", desc: "File Transfer Protocol (Active Data Channel)" },
  { port: 21, proto: "TCP", service: "FTP Control", desc: "File Transfer Protocol (Bidirectional Command & Control Channel)" },
  { port: 22, proto: "TCP/UDP", service: "SSH / SFTP", desc: "Secure Shell / Secure FTP (Asymmetric encryption for CLI & transfer)" },
  { port: 23, proto: "TCP", service: "Telnet", desc: "Clear-text unencrypted remote terminal emulation; superseded by SSH" },
  { port: 25, proto: "TCP", service: "SMTP", desc: "Simple Mail Transfer Protocol (Server-to-server mail relay routing)" },
  { port: 53, proto: "TCP/UDP", service: "DNS", desc: "Domain Name System (Queries UDP 53, Zone transfers/large payloads TCP 53)" },
  { port: 67, proto: "UDP", service: "DHCP Server", desc: "Dynamic Host Configuration Protocol (Server/relay listener in DORA process)" },
  { port: 68, proto: "UDP", service: "DHCP Client", desc: "Dynamic Host Configuration Protocol (Client endpoint listener in DORA process)" },
  { port: 69, proto: "UDP", service: "TFTP", desc: "Trivial File Transfer Protocol (Connectionless UDP, bootstrap/firmware imaging)" },
  { port: 80, proto: "TCP", service: "HTTP", desc: "Hypertext Transfer Protocol (Clear-text World Wide Web document transport)" },
  { port: 88, proto: "TCP/UDP", service: "Kerberos", desc: "Enterprise authentication via symmetric keys & KDC tickets (Active Directory default)" },
  { port: 110, proto: "TCP", service: "POP3", desc: "Post Office Protocol v3 (Clear-text mail retrieval, deletes from server by default)" },
  { port: 123, proto: "UDP", service: "NTP", desc: "Network Time Protocol (Clock synchronization across hierarchical stratum architecture)" },
  { port: 143, proto: "TCP", service: "IMAP", desc: "Internet Message Access Protocol (Server-synced mail keeping headers centralized)" },
  { port: 161, proto: "UDP", service: "SNMP Polls", desc: "Simple Network Management Protocol (Management queries and polling commands)" },
  { port: 162, proto: "UDP", service: "SNMP Traps", desc: "Simple Network Management Protocol (Unsolicited asynchronous agent alerts)" },
  { port: 389, proto: "TCP/UDP", service: "LDAP", desc: "Lightweight Directory Access Protocol (Unencrypted corporate directory querying)" },
  { port: 443, proto: "TCP", service: "HTTPS", desc: "Hypertext Transfer Protocol Secure (HTTP wrapped inside cryptographic TLS session)" },
  { port: 445, proto: "TCP", service: "SMB", desc: "Server Message Block (Network file system & print sharing native over TCP/IP)" },
  { port: 514, proto: "UDP", service: "Syslog", desc: "Standard system log collection forwarding notifications to central SIEM collector" },
  { port: 587, proto: "TCP", service: "SMTPS / Submission", desc: "Simple Mail Transfer Protocol Secure (Enforces mandatory TLS for client submission)" },
  { port: 636, proto: "TCP", service: "LDAPS", desc: "LDAP over SSL/TLS (Directory query mechanism in TLS cryptographic tunnel)" },
  { port: 993, proto: "TCP", service: "IMAPS", desc: "IMAP over SSL/TLS (Encrypted email synchronization over dedicated secure socket)" },
  { port: 995, proto: "TCP", service: "POP3S", desc: "POP3 over SSL/TLS (Encrypted email retrieval over dedicated secure socket)" },
  { port: 1433, proto: "TCP", service: "Microsoft SQL Server", desc: "Relational database client query protocol for structured data operations" },
  { port: 3389, proto: "TCP/UDP", service: "RDP", desc: "Remote Desktop Protocol (Microsoft proprietary graphical desktop management)" },
  { port: 5060, proto: "TCP/UDP", service: "SIP (Clear-text)", desc: "Session Initiation Protocol (VoIP signaling, call setup & teardown in cleartext)" },
  { port: 5061, proto: "TCP/UDP", service: "SIP over TLS", desc: "Session Initiation Protocol Secure (VoIP signaling encapsulated over TLS)" }
];

export class PortDrill {
  constructor() {
    this.ports = [...CORE_PORTS];
    this.currentQuestion = null;
    this.questionStartTime = 0;
    this.attempts = 0;
    this.correctCount = 0;
    this.streak = 0;
    this.latencies = [];
  }

  /**
   * Generates a new rapid-fire multiple choice question.
   * Mode: 'port_to_service' or 'service_to_port'
   */
  generateQuestion(mode = 'random') {
    if (mode === 'random') {
      mode = Math.random() > 0.5 ? 'port_to_service' : 'service_to_port';
    }

    const targetIndex = Math.floor(Math.random() * this.ports.length);
    const target = this.ports[targetIndex];

    // Pick 3 unique distractors
    const distractors = [];
    const pool = this.ports.filter((_, idx) => idx !== targetIndex);
    while (distractors.length < 3 && pool.length > 0) {
      const randIdx = Math.floor(Math.random() * pool.length);
      distractors.push(pool.splice(randIdx, 1)[0]);
    }

    // Combine and shuffle choices
    const choices = [target, ...distractors].sort(() => Math.random() - 0.5);

    this.currentQuestion = {
      mode,
      target,
      prompt: mode === 'port_to_service'
        ? `Port ${target.port} (${target.proto})`
        : `${target.service} (${target.proto})`,
      questionText: mode === 'port_to_service'
        ? `What protocol operates on Port ${target.port}?`
        : `What port is standard for ${target.service}?`,
      choices: choices.map(c => ({
        label: mode === 'port_to_service' ? c.service : `Port ${c.port}`,
        targetRef: c,
        isCorrect: c.port === target.port
      }))
    };

    this.questionStartTime = performance.now();
    return this.currentQuestion;
  }

  submitAnswer(choiceIndex) {
    if (!this.currentQuestion || choiceIndex < 0 || choiceIndex >= this.currentQuestion.choices.length) {
      return null;
    }

    const latencyMs = Math.round(performance.now() - this.questionStartTime);
    const choice = this.currentQuestion.choices[choiceIndex];
    const isCorrect = choice.isCorrect;

    this.attempts += 1;
    if (isCorrect) {
      this.correctCount += 1;
      this.streak += 1;
      this.latencies.push(latencyMs);
    } else {
      this.streak = 0;
    }

    const accuracy = Number(((this.correctCount / this.attempts) * 100).toFixed(1));
    const avgLatency = this.latencies.length > 0
      ? Math.round(this.latencies.reduce((a, b) => a + b, 0) / this.latencies.length)
      : latencyMs;

    // Record telemetry
    if (window.Telemetry) {
      window.Telemetry.recordPortTrial(latencyMs, isCorrect);
    }

    return {
      isCorrect,
      latencyMs,
      accuracy,
      avgLatency,
      streak: this.streak,
      attempts: this.attempts,
      target: this.currentQuestion.target
    };
  }

  resetStats() {
    this.attempts = 0;
    this.correctCount = 0;
    this.streak = 0;
    this.latencies = [];
  }
}

// Global browser fallback
if (typeof window !== 'undefined') {
  window.PortDrill = PortDrill;
  window.CORE_PORTS = CORE_PORTS;
}
