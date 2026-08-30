"use client";

/** Everything the feed and the chat need to survive a jump to /ogren and back.
 * sessionStorage only: it dies with the tab, nothing is sent anywhere. */

import type { AnswerResult } from "@/lib/api";

/** One thread per question. Asking about a new card must never show what was
 * said about a different one. */
const chatKey = (reelId: string) => `akis-chat-thread:${reelId}`;

/** Each pack keeps its own position and answers; the mixed feed uses "mix". */
export const MIX_SCOPE = "mix";

const feedKey = (scope: string) => `akis-feed-state:${scope}`;
const orderKey = (scope: string) => `akis-feed-order:${scope}`;

export type FeedState = {
  index: number;
  results: Record<string, AnswerResult>;
};

export type ChatItem = { role: "user" | "assistant"; content: string };

function read<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = window.sessionStorage.getItem(key);
    return raw ? ({ ...fallback, ...JSON.parse(raw) } as T) : fallback;
  } catch {
    return fallback;
  }
}

function write(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* private mode: the feature simply does not persist */
  }
}

export function loadFeedState(scope: string = MIX_SCOPE): FeedState {
  return read<FeedState>(feedKey(scope), { index: 0, results: {} });
}

export function saveFeedState(scope: string, state: FeedState) {
  write(feedKey(scope), state);
}

/** How far a pack has been taken, for the pack list. */
export function packProgress(scope: string): { answered: number; correct: number } {
  const results = Object.values(loadFeedState(scope).results);
  return { answered: results.length, correct: results.filter((r) => r.correct).length };
}

/** The server shuffles on every request; freezing the order for the tab is what
 * makes "come back to the card you left" mean anything. */
export function loadOrder(scope: string = MIX_SCOPE): string[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.sessionStorage.getItem(orderKey(scope));
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? (parsed as string[]) : [];
  } catch {
    return [];
  }
}

export function saveOrder(scope: string, ids: string[]) {
  write(orderKey(scope), ids);
}

export function loadThread(reelId: string): ChatItem[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.sessionStorage.getItem(chatKey(reelId));
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed)
      ? (parsed as ChatItem[]).filter(
          (m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string",
        )
      : [];
  } catch {
    return [];
  }
}

export function saveThread(reelId: string, items: ChatItem[]) {
  write(chatKey(reelId), items);
}

export function clearThread(reelId: string) {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.removeItem(chatKey(reelId));
  } catch {
    /* ignore */
  }
}
