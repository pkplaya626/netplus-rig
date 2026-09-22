/**
 * Flashcard Review Controller (Anki / SM-2 Engine)
 * Manages deck loading, queue filtering, keyboard controls (Space/Enter, 1-4),
 * card flip animations, and Git state exports.
 */

import { calculateSM2, Quality, mapRatingToQuality } from './sm2.js';
import { TelemetryManager } from './telemetry.js';

export class FlashcardController {
  constructor() {
    this.telemetry = window.Telemetry || new TelemetryManager();
    this.cards = [];
    this.queue = [];
    this.currentIndex = 0;
    this.isFlipped = false;
    this.activeFilter = 'all'; // 'all', 'due', or domain
    this.sessionReviewedCount = 0;
  }

  async init() {
    await this.loadCardDeck();
    this.buildQueue();
    this.setupKeyboardListeners();
    this.renderCurrentCard();
    this.updateStatsBar();
  }

  async loadCardDeck() {
    const paths = ['data/cards.json', '../data/cards.json', './data/cards.json'];
    let loaded = false;

    for (const p of paths) {
      try {
        const resp = await fetch(p);
        if (resp.ok) {
          this.cards = await resp.json();
          loaded = true;
          break;
        }
      } catch (e) {
        // try next path
      }
    }

    if (!loaded) {
      console.warn('Could not fetch cards.json directly. Checking inline seed fallback.');
      this.cards = [];
    }

    // Try to load initial reviews.json if localStorage is empty
    if (Object.keys(this.telemetry.reviews.cards).length === 0) {
      for (const p of ['data/reviews.json', '../data/reviews.json']) {
        try {
          const resp = await fetch(p);
          if (resp.ok) {
            const revData = await resp.json();
            this.telemetry.mergeInitialReviews(revData);
            break;
          }
        } catch (e) {}
      }
    }
  }

  buildQueue() {
    const today = new Date().toISOString().split('T')[0];
    let filtered = [...this.cards];

    if (this.activeFilter === 'due') {
      filtered = filtered.filter(card => {
        const rev = this.telemetry.reviews.cards[card.id];
        if (!rev) return true; // new card is due
        return rev.dueDate <= today;
      });
    } else if (this.activeFilter.startsWith('domain:')) {
      const dName = this.activeFilter.replace('domain:', '');
      filtered = filtered.filter(card => card.domain.startsWith(dName));
    }

    // Shuffle queue for varied retention
    this.queue = filtered.sort(() => Math.random() - 0.5);
    this.currentIndex = 0;
    this.isFlipped = false;
  }

  setFilter(filterName) {
    this.activeFilter = filterName;
    this.buildQueue();
    this.renderCurrentCard();
    this.updateStatsBar();
  }

  getCurrentCard() {
    if (this.queue.length === 0 || this.currentIndex >= this.queue.length) {
      return null;
    }
    return this.queue[this.currentIndex];
  }

  getCardReviewState(cardId) {
    const today = new Date().toISOString().split('T')[0];
    return this.telemetry.reviews.cards[cardId] || {
      repetitions: 0,
      interval: 1,
      easeFactor: 2.5,
      dueDate: today
    };
  }

  flipCard() {
    if (!this.getCurrentCard()) return;
    this.isFlipped = !this.isFlipped;
    const cardEl = document.getElementById('flashcard');
    if (cardEl) {
      cardEl.classList.toggle('flipped', this.isFlipped);
    }
    const actionsEl = document.getElementById('rating-actions');
    const flipHint = document.getElementById('flip-hint');
    if (actionsEl) {
      actionsEl.style.display = this.isFlipped ? 'grid' : 'none';
    }
    if (flipHint) {
      flipHint.style.display = this.isFlipped ? 'none' : 'block';
    }
  }

  rateCard(rating) {
    const card = this.getCurrentCard();
    if (!card) return;

    const currentState = this.getCardReviewState(card.id);
    const quality = mapRatingToQuality(rating);
    const sm2Result = calculateSM2(currentState, quality);

    // Save to telemetry
    this.telemetry.recordCardReview(card.id, sm2Result, rating);
    this.sessionReviewedCount += 1;

    // Advance to next card
    this.currentIndex += 1;
    this.isFlipped = false;
    this.renderCurrentCard();
    this.updateStatsBar();
  }

  renderCurrentCard() {
    const card = this.getCurrentCard();
    const container = document.getElementById('card-stage');
    if (!container) return;

    if (!card) {
      container.innerHTML = `
        <div class="empty-queue-card">
          <div class="terminal-badge pulse">DECK COMPLETE</div>
          <h2>All scheduled cards reviewed!</h2>
          <p>You have cleared all queued cards for this session. Great retention work.</p>
          <div class="deck-complete-actions">
            <button class="btn btn-primary" id="restart-deck-btn">Study All 55 Cards Again</button>
            <button class="btn btn-secondary" id="export-git-btn-finish">Export Review State to Git</button>
          </div>
        </div>
      `;
      const restartBtn = document.getElementById('restart-deck-btn');
      if (restartBtn) {
        restartBtn.addEventListener('click', () => {
          this.setFilter('all');
        });
      }
      const expBtn = document.getElementById('export-git-btn-finish');
      if (expBtn) {
        expBtn.addEventListener('click', () => this.showExportModal());
      }
      return;
    }

    const state = this.getCardReviewState(card.id);
    // Interval previews for ratings
    const againPreview = calculateSM2(state, Quality.AGAIN).interval;
    const hardPreview = calculateSM2(state, Quality.HARD).interval;
    const goodPreview = calculateSM2(state, Quality.GOOD).interval;
    const easyPreview = calculateSM2(state, Quality.EASY).interval;

    container.innerHTML = `
      <div class="flashcard-container" id="flashcard-container">
        <div class="flashcard" id="flashcard">
          <div class="card-face card-front">
            <div class="card-meta">
              <span class="badge domain-badge">${card.domain}</span>
              <span class="badge subdomain-badge">${card.subdomain}</span>
              <span class="badge id-badge">${card.id}</span>
            </div>
            <div class="card-prompt">
              <h3>${card.front}</h3>
            </div>
            <div class="flip-hint" id="flip-hint">
              <kbd>Space</kbd> or <kbd>Enter</kbd> to reveal answer
            </div>
          </div>
          
          <div class="card-face card-back">
            <div class="card-meta">
              <span class="badge answer-badge">ANSWER / EXPLANATION</span>
              <span class="sm2-stats-pill">Reps: ${state.repetitions} | Interval: ${state.interval}d | EF: ${state.easeFactor.toFixed(2)}</span>
            </div>
            <div class="card-solution">
              <p>${card.back.replace(/\n/g, '<br>')}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="rating-actions" id="rating-actions" style="display: none;">
        <button class="btn btn-rating btn-again" data-rating="1">
          <span class="key-indicator">1</span>
          <span class="rating-label">Again</span>
          <span class="interval-hint">&lt; ${againPreview}d</span>
        </button>
        <button class="btn btn-rating btn-hard" data-rating="2">
          <span class="key-indicator">2</span>
          <span class="rating-label">Hard</span>
          <span class="interval-hint">${hardPreview}d</span>
        </button>
        <button class="btn btn-rating btn-good" data-rating="3">
          <span class="key-indicator">3</span>
          <span class="rating-label">Good</span>
          <span class="interval-hint">${goodPreview}d</span>
        </button>
        <button class="btn btn-rating btn-easy" data-rating="4">
          <span class="key-indicator">4</span>
          <span class="rating-label">Easy</span>
          <span class="interval-hint">${easyPreview}d</span>
        </button>
      </div>
    `;

    // Attach click events
    const cardEl = document.getElementById('flashcard');
    if (cardEl) {
      cardEl.addEventListener('click', () => this.flipCard());
    }

    const ratingButtons = document.querySelectorAll('.btn-rating');
    ratingButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = parseInt(btn.getAttribute('data-rating'), 10);
        this.rateCard(rating);
      });
    });
  }

  updateStatsBar() {
    const queueTotalEl = document.getElementById('stat-queue-remaining');
    const reviewedSessionEl = document.getElementById('stat-session-count');
    const totalDeckEl = document.getElementById('stat-deck-total');

    if (queueTotalEl) {
      queueTotalEl.textContent = Math.max(0, this.queue.length - this.currentIndex);
    }
    if (reviewedSessionEl) {
      reviewedSessionEl.textContent = this.sessionReviewedCount;
    }
    if (totalDeckEl) {
      totalDeckEl.textContent = this.cards.length;
    }
  }

  setupKeyboardListeners() {
    window.addEventListener('keydown', (e) => {
      // Ignore if typing in text inputs or modals
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (e.code === 'Space' || e.code === 'Enter') {
        e.preventDefault();
        if (!this.isFlipped) {
          this.flipCard();
        } else {
          // If already flipped, space/enter records 'Good' (3)
          this.rateCard(Quality.GOOD);
        }
      } else if (this.isFlipped) {
        if (e.key === '1') {
          e.preventDefault();
          this.rateCard(Quality.AGAIN);
        } else if (e.key === '2') {
          e.preventDefault();
          this.rateCard(Quality.HARD);
        } else if (e.key === '3') {
          e.preventDefault();
          this.rateCard(Quality.GOOD);
        } else if (e.key === '4') {
          e.preventDefault();
          this.rateCard(Quality.EASY);
        }
      }
    });
  }

  showExportModal() {
    let modal = document.getElementById('git-export-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'git-export-modal';
      modal.className = 'modal-backdrop';
      document.body.appendChild(modal);
    }

    const reviewsJson = this.telemetry.exportReviewsJson();
    const progressJson = this.telemetry.exportProgressJson();

    modal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>📦 Export Review State to Git</h3>
          <button class="close-btn" id="close-export-modal">&times;</button>
        </div>
        <div class="modal-body">
          <p>Sync your local review intervals and SM-2 retention curves directly to your repository.</p>
          
          <div class="export-actions-row">
            <button class="btn btn-primary" id="download-reviews-btn">📥 Download data/reviews.json</button>
            <button class="btn btn-secondary" id="download-progress-btn">📥 Download telemetry/progress.json</button>
          </div>

          <h4>Staging Command (Paste into terminal):</h4>
          <pre class="code-box"><code>git add data/reviews.json telemetry/progress.json
git commit -m "feat(telemetry): sync flashcard reviews and drill metrics"
git push</code></pre>

          <h4>Raw data/reviews.json Payload:</h4>
          <textarea class="json-payload-textarea" id="raw-reviews-box" readonly>${reviewsJson}</textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" id="copy-json-btn">Copy JSON to Clipboard</button>
          <button class="btn btn-primary" id="dismiss-modal-btn">Done</button>
        </div>
      </div>
    `;

    modal.style.display = 'flex';

    document.getElementById('close-export-modal')?.addEventListener('click', () => modal.style.display = 'none');
    document.getElementById('dismiss-modal-btn')?.addEventListener('click', () => modal.style.display = 'none');
    
    document.getElementById('download-reviews-btn')?.addEventListener('click', () => {
      this.telemetry.downloadJsonFile('reviews.json', reviewsJson);
    });

    document.getElementById('download-progress-btn')?.addEventListener('click', () => {
      this.telemetry.downloadJsonFile('progress.json', progressJson);
    });

    document.getElementById('copy-json-btn')?.addEventListener('click', () => {
      navigator.clipboard.writeText(reviewsJson).then(() => {
        alert('Copied reviews.json content to clipboard!');
      });
    });
  }
}

// Global browser fallback
if (typeof window !== 'undefined') {
  window.FlashcardController = FlashcardController;
}
