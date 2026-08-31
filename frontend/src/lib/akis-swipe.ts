export const AKIS_SWIPE_THRESHOLD = 48;
export const AKIS_SWIPE_DURATION_MS = 190;

export type SwipeStart = {
  y: number;
  index: number;
  canMoveBack: boolean;
  canMoveForward: boolean;
};

/** Returns one neighbouring slide, or null when the gesture belongs to the
 * card's own scroll area (or is too small to count as a swipe). */
export function akisSwipeDestination(
  start: SwipeStart,
  endY: number,
  maxIndex: number,
): number | null {
  const distance = start.y - endY;
  if (Math.abs(distance) < AKIS_SWIPE_THRESHOLD) return null;

  const direction = distance > 0 ? 1 : -1;
  const consumedByCard = direction > 0 ? start.canMoveForward : start.canMoveBack;
  if (consumedByCard) return null;

  return Math.max(0, Math.min(maxIndex, start.index + direction));
}
