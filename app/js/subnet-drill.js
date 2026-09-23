/**
 * Subnetting Time Trial Engine
 * Generates random IPv4 & CIDR prefixes (/24 to /30, and /16 to /23),
 * calculates ground truth, manages 30-second target timer, and validates answers.
 */

export class SubnetDrill {
  constructor() {
    this.currentProblem = null;
    this.startTime = null;
    this.timerInterval = null;
    this.elapsedSeconds = 0;
    this.targetSeconds = 30.0;
    this.streak = 0;
  }

  /**
   * Converts 32-bit unsigned integer to dotted-decimal IPv4 string.
   */
  intToIp(intVal) {
    const u = intVal >>> 0;
    return [
      (u >>> 24) & 255,
      (u >>> 16) & 255,
      (u >>> 8) & 255,
      u & 255
    ].join('.');
  }

  /**
   * Converts dotted-decimal IPv4 string to 32-bit unsigned integer.
   */
  ipToInt(ipStr) {
    const octets = ipStr.trim().split('.').map(Number);
    if (octets.length !== 4 || octets.some(o => isNaN(o) || o < 0 || o > 255)) {
      return null;
    }
    return (((octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]) >>> 0);
  }

  /**
   * Generates a new random IPv4 and CIDR prefix.
   */
  generateRandomProblem(tier = 'all') {
    // Select CIDR
    let cidrList = [];
    if (tier === 'tier1') {
      cidrList = [24, 25, 26, 27, 28, 29, 30];
    } else if (tier === 'tier2') {
      cidrList = [16, 17, 18, 19, 20, 21, 22, 23];
    } else {
      cidrList = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];
    }

    const cidr = cidrList[Math.floor(Math.random() * cidrList.length)];

    // Generate realistic base IPs (RFC 1918 or standard public class ranges)
    const baseRanges = [
      () => `10.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254) + 1}`,
      () => `172.${16 + Math.floor(Math.random() * 16)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254) + 1}`,
      () => `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254) + 1}`,
      () => `${Math.floor(Math.random() * 120) + 11}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254) + 1}`
    ];

    const ipStr = baseRanges[Math.floor(Math.random() * baseRanges.length)]();
    return this.calculateSolution(ipStr, cidr);
  }

  calculateSolution(ipStr, cidr) {
    const ipInt = this.ipToInt(ipStr);
    const hostBits = 32 - cidr;
    const maskInt = (cidr === 0 ? 0 : (~0 << hostBits)) >>> 0;
    const networkInt = (ipInt & maskInt) >>> 0;
    const broadcastInt = (networkInt | (~maskInt >>> 0)) >>> 0;

    let firstUsableInt = networkInt + 1;
    let lastUsableInt = broadcastInt - 1;

    // Boundary for /31 or /32 edge cases (though we cap at /30)
    if (cidr === 31 || cidr === 32) {
      firstUsableInt = networkInt;
      lastUsableInt = broadcastInt;
    }

    const totalAddresses = Math.pow(2, hostBits);
    const usableHosts = cidr <= 30 ? totalAddresses - 2 : totalAddresses;

    // Determine which octet the subnet boundary falls in (1-indexed)
    // For /24 -> octet 4 (host bits are in 4th octet), /25 -> octet 4, /16 -> octet 3
    const interestingOctet = cidr % 8 === 0
      ? Math.floor(cidr / 8) + 1
      : Math.floor(cidr / 8) + 1;
    const bitsInOctet = cidr % 8 === 0 ? 0 : cidr % 8;
    const blockSize = Math.pow(2, 8 - bitsInOctet);

    this.currentProblem = {
      ip: ipStr,
      cidr: cidr,
      subnetMask: this.intToIp(maskInt),
      networkId: this.intToIp(networkInt),
      firstUsable: this.intToIp(firstUsableInt),
      lastUsable: this.intToIp(lastUsableInt),
      broadcast: this.intToIp(broadcastInt),
      totalAddresses,
      usableHosts,
      blockSize,
      interestingOctet
    };

    return this.currentProblem;
  }

  startTimer(onTick) {
    this.stopTimer();
    this.startTime = Date.now();
    this.elapsedSeconds = 0;
    this.timerInterval = setInterval(() => {
      const now = Date.now();
      this.elapsedSeconds = Number(((now - this.startTime) / 1000).toFixed(1));
      if (onTick) onTick(this.elapsedSeconds);
    }, 100);
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  validateSubmission(userAnswers) {
    this.stopTimer();
    const p = this.currentProblem;
    if (!p) return null;

    const results = {
      networkId: {
        expected: p.networkId,
        actual: userAnswers.networkId?.trim(),
        correct: userAnswers.networkId?.trim() === p.networkId
      },
      firstUsable: {
        expected: p.firstUsable,
        actual: userAnswers.firstUsable?.trim(),
        correct: userAnswers.firstUsable?.trim() === p.firstUsable
      },
      lastUsable: {
        expected: p.lastUsable,
        actual: userAnswers.lastUsable?.trim(),
        correct: userAnswers.lastUsable?.trim() === p.lastUsable
      },
      broadcast: {
        expected: p.broadcast,
        actual: userAnswers.broadcast?.trim(),
        correct: userAnswers.broadcast?.trim() === p.broadcast
      },
      elapsedSeconds: this.elapsedSeconds,
      passedTarget: this.elapsedSeconds <= this.targetSeconds
    };

    results.allCorrect = results.networkId.correct &&
                         results.firstUsable.correct &&
                         results.lastUsable.correct &&
                         results.broadcast.correct;

    if (results.allCorrect) {
      this.streak += 1;
    } else {
      this.streak = 0;
    }
    results.streak = this.streak;

    // Record telemetry if available
    if (window.Telemetry) {
      window.Telemetry.recordSubnetDrill(this.elapsedSeconds, results.allCorrect);
    }

    return results;
  }
}

// Global browser fallback
if (typeof window !== 'undefined') {
  window.SubnetDrill = SubnetDrill;
}
