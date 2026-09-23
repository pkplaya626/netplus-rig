/**
 * Telemetry & Metrics Aggregator for CompTIA Network+ Rig
 * Handles LocalStorage persistence, session statistics, and Git export payloads.
 */

const STORAGE_KEY_REVIEWS = 'netplus_reviews_v1';
const STORAGE_KEY_PROGRESS = 'netplus_progress_v1';
const STORAGE_KEY_SESSIONS = 'netplus_drill_sessions_v1';

export class TelemetryManager {
  constructor() {
    this.reviews = this.loadReviews();
    this.progress = this.loadProgress();
  }

  loadReviews() {
    try {
      const data = localStorage.getItem(STORAGE_KEY_REVIEWS);
      return data ? JSON.parse(data) : { version: '1.0', lastSynced: new Date().toISOString(), cards: {} };
    } catch (e) {
      console.error('Error loading reviews from localStorage:', e);
      return { version: '1.0', lastSynced: new Date().toISOString(), cards: {} };
    }
  }

  saveReviews() {
    try {
      this.reviews.lastSynced = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY_REVIEWS, JSON.stringify(this.reviews));
    } catch (e) {
      console.error('Error saving reviews to localStorage:', e);
    }
  }

  loadProgress() {
    try {
      const data = localStorage.getItem(STORAGE_KEY_PROGRESS);
      if (data) return JSON.parse(data);
    } catch (e) {
      console.error('Error loading progress from localStorage:', e);
    }
    return {
      lastUpdated: new Date().toISOString(),
      currentDay: 1,
      totalDays: 30,
      dailyLogs: {},
      aggregateStats: {
        totalCardsReviewed: 0,
        totalQuestionsAnswered: 0,
        questionsCorrect: 0,
        overallAccuracy: 100.0,
        avgSubnetTimeSeconds: 0,
        bestSubnetTimeSeconds: 999,
        avgPortLatencyMs: 0,
        bestPortAccuracyPercent: 100.0
      },
      domainMastery: {
        "1.0 Networking Concepts": { cleared: 0, total: 24, pct: 0 },
        "2.0 Network Implementation": { cleared: 0, total: 20, pct: 0 },
        "3.0 Network Operations": { cleared: 0, total: 16, pct: 0 },
        "4.0 Network Security": { cleared: 0, total: 18, pct: 0 },
        "5.0 Network Troubleshooting": { cleared: 0, total: 18, pct: 0 }
      }
    };
  }

  saveProgress() {
    try {
      this.progress.lastUpdated = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY_PROGRESS, JSON.stringify(this.progress));
    } catch (e) {
      console.error('Error saving progress to localStorage:', e);
    }
  }

  /**
   * Merges server seed reviews with local modifications.
   */
  mergeInitialReviews(serverReviews) {
    if (!serverReviews || !serverReviews.cards) return;
    let modified = false;
    for (const [cardId, state] of Object.entries(serverReviews.cards)) {
      if (!this.reviews.cards[cardId]) {
        this.reviews.cards[cardId] = state;
        modified = true;
      }
    }
    if (modified) {
      this.saveReviews();
    }
  }

  getTodayKey() {
    return new Date().toISOString().split('T')[0];
  }

  getTodayLog() {
    const today = this.getTodayKey();
    const dayIndex = this.progress.currentDay || 1;
    const dayKey = String(dayIndex);

    if (!this.progress.dailyLogs[dayKey]) {
      this.progress.dailyLogs[dayKey] = {
        date: today,
        status: "GREEN",
        synthesisFile: `artifacts/day-${String(dayIndex).padStart(2, '0')}-*.md`,
        wordCount: 0,
        cardsReviewed: 0,
        questionsCleared: 0,
        subnetDrill: { attempts: 0, correct: 0, avgTimeSeconds: 0, bestTimeSeconds: 999 },
        portDrill: { attempts: 0, correct: 0, avgLatencyMs: 0, accuracyPercent: 100.0 }
      };
    }
    return this.progress.dailyLogs[dayKey];
  }

  recordCardReview(cardId, sm2Result, rating) {
    const today = this.getTodayKey();
    if (!this.reviews.cards[cardId]) {
      this.reviews.cards[cardId] = {
        repetitions: 0,
        interval: 1,
        easeFactor: 2.5,
        dueDate: today,
        history: []
      };
    }

    const card = this.reviews.cards[cardId];
    card.repetitions = sm2Result.repetitions;
    card.interval = sm2Result.interval;
    card.easeFactor = sm2Result.easeFactor;
    card.dueDate = sm2Result.dueDate;
    card.lastReviewed = today;
    if (!card.history) card.history = [];
    card.history.push({
      date: today,
      rating,
      interval: sm2Result.interval,
      easeFactor: sm2Result.easeFactor
    });

    this.saveReviews();

    // Log progress
    const log = this.getTodayLog();
    log.cardsReviewed = (log.cardsReviewed || 0) + 1;
    this.progress.aggregateStats.totalCardsReviewed = (this.progress.aggregateStats.totalCardsReviewed || 0) + 1;
    this.saveProgress();
  }

  recordSubnetDrill(seconds, isCorrect) {
    const log = this.getTodayLog();
    const sd = log.subnetDrill;
    sd.attempts = (sd.attempts || 0) + 1;
    if (isCorrect) {
      sd.correct = (sd.correct || 0) + 1;
      if (seconds < (sd.bestTimeSeconds || 999)) {
        sd.bestTimeSeconds = Number(seconds.toFixed(1));
      }
    }
    // Running average
    sd.avgTimeSeconds = sd.avgTimeSeconds === 0 
      ? Number(seconds.toFixed(1)) 
      : Number(((sd.avgTimeSeconds * (sd.attempts - 1) + seconds) / sd.attempts).toFixed(1));

    // Update aggregate
    const agg = this.progress.aggregateStats;
    agg.avgSubnetTimeSeconds = sd.avgTimeSeconds;
    if (isCorrect && seconds < (agg.bestSubnetTimeSeconds || 999)) {
      agg.bestSubnetTimeSeconds = Number(seconds.toFixed(1));
    }
    this.saveProgress();
  }

  recordPortTrial(latencyMs, isCorrect) {
    const log = this.getTodayLog();
    const pd = log.portDrill;
    pd.attempts = (pd.attempts || 0) + 1;
    if (isCorrect) {
      pd.correct = (pd.correct || 0) + 1;
    }
    pd.avgLatencyMs = pd.avgLatencyMs === 0
      ? Math.round(latencyMs)
      : Math.round((pd.avgLatencyMs * (pd.attempts - 1) + latencyMs) / pd.attempts);
    pd.accuracyPercent = Number(((pd.correct / pd.attempts) * 100).toFixed(1));

    const agg = this.progress.aggregateStats;
    agg.avgPortLatencyMs = pd.avgLatencyMs;
    agg.bestPortAccuracyPercent = pd.accuracyPercent;
    this.saveProgress();
  }

  recordQuizAnswer(questionId, domain, isCorrect) {
    const log = this.getTodayLog();
    log.questionsCleared = (log.questionsCleared || 0) + 1;

    const agg = this.progress.aggregateStats;
    agg.totalQuestionsAnswered = (agg.totalQuestionsAnswered || 0) + 1;
    if (isCorrect) {
      agg.questionsCorrect = (agg.questionsCorrect || 0) + 1;
    }
    agg.overallAccuracy = Number(((agg.questionsCorrect / agg.totalQuestionsAnswered) * 100).toFixed(1));

    // Update domain mastery using unique question tracking
    if (this.progress.domainMastery[domain]) {
      const dm = this.progress.domainMastery[domain];
      if (!dm.clearedIds) dm.clearedIds = [];
      if (isCorrect && !dm.clearedIds.includes(questionId)) {
        dm.clearedIds.push(questionId);
      } else if (!isCorrect) {
        dm.clearedIds = dm.clearedIds.filter(id => id !== questionId);
      }
      dm.cleared = Math.min(dm.total, dm.clearedIds.length);
      dm.pct = Math.round((dm.cleared / dm.total) * 100);
    }
    this.saveProgress();
  }

  exportReviewsJson() {
    return JSON.stringify(this.reviews, null, 2);
  }

  exportProgressJson() {
    return JSON.stringify(this.progress, null, 2);
  }

  downloadJsonFile(filename, jsonContent) {
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}

// Global instance fallback
if (typeof window !== 'undefined') {
  window.Telemetry = new TelemetryManager();
}
