"use client";

/** Site-wide listening preferences. Chosen once, used by every card.
 * localStorage, not sessionStorage: the choice should survive a new tab. */

const SPEED_KEY = "akis-speed";

/** 0.5x to 2x in even quarter steps. */
export const SPEEDS = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2] as const;

export const DEFAULT_SPEED = 1;

export function loadSpeed(): number {
  if (typeof window === "undefined") return DEFAULT_SPEED;
  try {
    const raw = Number(window.localStorage.getItem(SPEED_KEY));
    return (SPEEDS as readonly number[]).includes(raw) ? raw : DEFAULT_SPEED;
  } catch {
    return DEFAULT_SPEED;
  }
}

export function saveSpeed(value: number) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(SPEED_KEY, String(value));
  } catch {
    /* private mode: the setting just does not persist */
  }
}

/** Autoplay permission belongs to the document, not to a component. Kept in
 * module scope so remounting the feed (a new pack) does not lose it, while a
 * full page reload correctly requires a fresh tap. */
let audioUnlocked = false;

export function isAudioUnlocked() {
  return audioUnlocked;
}

export function markAudioUnlocked() {
  audioUnlocked = true;
}

/** "1x" reads better than "1.00x", and "0.75x" must keep its decimals. */
export function speedLabel(value: number) {
  return `${Number.isInteger(value) ? value : value.toString().replace(/0+$/, "")}×`;
}
