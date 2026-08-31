import assert from "node:assert/strict";
import {
  AKIS_SWIPE_DURATION_MS,
  AKIS_SWIPE_LOCK_MS,
  akisSwipeDestination,
  type SwipeStart,
} from "../src/lib/akis-swipe.ts";

const gesture = (overrides: Partial<SwipeStart> = {}): SwipeStart => ({
  y: 700,
  index: 4,
  canMoveBack: false,
  canMoveForward: false,
  ...overrides,
});

// Even an extreme fling advances by exactly one slide.
assert.equal(akisSwipeDestination(gesture(), -1200, 30), 5);
assert.equal(akisSwipeDestination(gesture(), 2200, 30), 3);

// Repeated edge cases cannot escape the feed.
assert.equal(akisSwipeDestination(gesture({ index: 0 }), 2200, 30), 0);
assert.equal(akisSwipeDestination(gesture({ index: 30 }), -1200, 30), 30);

// A long card consumes the gesture while it still has content in that direction.
assert.equal(akisSwipeDestination(gesture({ canMoveForward: true }), -1200, 30), null);
assert.equal(akisSwipeDestination(gesture({ canMoveBack: true }), 2200, 30), null);

// Small finger movement is a tap, not navigation.
assert.equal(akisSwipeDestination(gesture(), 660, 30), null);

// The lock protects the animation without making consecutive swipes feel heavy.
assert.ok(AKIS_SWIPE_DURATION_MS >= 150 && AKIS_SWIPE_DURATION_MS <= 220);
assert.ok(AKIS_SWIPE_LOCK_MS >= AKIS_SWIPE_DURATION_MS);
assert.ok(AKIS_SWIPE_LOCK_MS - AKIS_SWIPE_DURATION_MS <= 60);

console.log("Akış swipe regression checks passed");
