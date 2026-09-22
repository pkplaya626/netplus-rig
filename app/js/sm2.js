/**
 * SuperMemo SM-2 Spaced Repetition Algorithm Implementation
 * Pure vanilla ES6 client-side module.
 */

export const Quality = {
  AGAIN: 1, // q = 1 (Blackout / Failure)
  HARD: 2,  // q = 3 (Correct with hesitation)
  GOOD: 3,  // q = 4 (Correct after hesitation)
  EASY: 4   // q = 5 (Perfect instant recall)
};

/**
 * Maps 1-4 UI button rating to standard SM-2 0-5 quality score.
 */
export function mapRatingToQuality(rating) {
  switch (rating) {
    case 1: return 1; // Again
    case 2: return 3; // Hard
    case 3: return 4; // Good
    case 4: return 5; // Easy
    default: return 3;
  }
}

/**
 * Calculates updated SM-2 interval, repetitions, ease factor, and due date.
 *
 * @param {Object} current - Current card state { repetitions, interval, easeFactor }
 * @param {number} quality - SM-2 quality (0 to 5)
 * @param {Date} [baseDate=new Date()] - Reference date for calculation
 * @returns {Object} Updated card state
 */
export function calculateSM2(current, quality, baseDate = new Date()) {
  let repetitions = current.repetitions || 0;
  let interval = current.interval || 1;
  let easeFactor = current.easeFactor || 2.5;

  // Validate bounds
  if (quality < 0) quality = 0;
  if (quality > 5) quality = 5;

  if (quality < 3) {
    // Failed recall: reset repetitions and schedule for tomorrow
    repetitions = 0;
    interval = 1;
  } else {
    // Successful recall
    if (repetitions === 0) {
      interval = 1;
    } else if (repetitions === 1) {
      interval = 6;
    } else {
      interval = Math.round(interval * easeFactor);
    }
    repetitions += 1;
  }

  // Update Ease Factor (EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
  const delta = 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02);
  easeFactor = easeFactor + delta;

  // Minimum Ease Factor threshold is 1.3
  if (easeFactor < 1.3) {
    easeFactor = 1.3;
  }

  // Round easeFactor to 2 decimal places for clean storage
  easeFactor = Math.round(easeFactor * 100) / 100;

  // Calculate new due date
  const nextDueDate = new Date(baseDate.getTime());
  nextDueDate.setDate(nextDueDate.getDate() + interval);
  const dueDateStr = nextDueDate.toISOString().split('T')[0];

  return {
    repetitions,
    interval,
    easeFactor,
    dueDate: dueDateStr
  };
}

// Global browser fallback if modules aren't used
if (typeof window !== 'undefined') {
  window.SM2 = {
    Quality,
    mapRatingToQuality,
    calculateSM2
  };
}
