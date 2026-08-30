export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const HUMAN_TOKEN_KEY = "hazirlik-human-token";
const HUMAN_TOKEN_EXPIRY_KEY = "hazirlik-human-token-expiry";

export function getHumanToken() {
  if (typeof window === "undefined") return "";
  const expiresAt = Number(window.sessionStorage.getItem(HUMAN_TOKEN_EXPIRY_KEY) ?? 0);
  if (!expiresAt || Date.now() >= expiresAt * 1000) {
    clearHumanToken();
    return "";
  }
  return window.sessionStorage.getItem(HUMAN_TOKEN_KEY) ?? "";
}

export function setHumanToken(token: string, expiresAt: number) {
  window.sessionStorage.setItem(HUMAN_TOKEN_KEY, token);
  window.sessionStorage.setItem(HUMAN_TOKEN_EXPIRY_KEY, String(expiresAt));
}

export function clearHumanToken() {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(HUMAN_TOKEN_KEY);
  window.sessionStorage.removeItem(HUMAN_TOKEN_EXPIRY_KEY);
}

export type TestSummary = {
  id: string;
  kind: string;
  title: string;
  topic: string;
  cefr: string;
  duration_sec: number;
  source: string;
};

export type QuestionPublic = {
  id: string;
  order: number;
  stem: string;
  options: Record<string, string>;
  points: number;
};

export type TestDetail = TestSummary & {
  instructions: string;
  content: Record<string, unknown>;
  questions: QuestionPublic[];
};

export type GradedQuestion = QuestionPublic & {
  chosen: string;
  answer: string;
  correct: boolean;
  rationale: string;
};

export type AttemptDetail = {
  id: string;
  test_id: string;
  kind: string;
  title: string;
  mode: string;
  score: number;
  max_score: number;
  notes: string;
  content: Record<string, unknown>;
  transcript: { speaker: string; text: string }[];
  note_scaffold: string;
  glossary: { en: string; tr: string }[];
  words: Record<string, string>;
  questions: GradedQuestion[];
};

export type Level = "A1" | "A2" | "B1" | "B1+";

export type ReelCard = {
  id: string;
  kind: "sorular" | "kelime" | "bosluk";
  level: Level;
  title: string;
  topic: string;
  seconds: number;
  body: string;
  stem: string;
  options: Record<string, string>;
};

export type AnswerResult = {
  id: string;
  kind: ReelCard["kind"];
  chosen: string;
  answer: string;
  correct: boolean;
  explain_tr: string;
  key_line: string;
  script: { speaker: string; text: string }[];
};

export type LevelSummary = {
  kind: ReelCard["kind"];
  level: Level;
  cards: number;
  packs: number;
  pack_size: number;
};

export type Pack = {
  id: string;
  kind: ReelCard["kind"];
  level: Level;
  index: number;
  title: string;
  size: number;
  pack_size: number;
  full: boolean;
};

export type ChatStatus = {
  ready: boolean;
  active: { provider: string | null; provider_label: string | null; model: string | null; ready: boolean };
};

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const isFormData = typeof FormData !== "undefined" && init?.body instanceof FormData;
  const humanToken = getHumanToken();
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(humanToken ? { "X-Human-Token": humanToken } : {}),
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) {
    if (res.status === 403 && res.headers.get("X-Human-Verification") === "required") {
      clearHumanToken();
      if (typeof window !== "undefined") window.dispatchEvent(new Event("human-verification-required"));
    }
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export function audioUrl(testId: string) {
  return `${API_URL}/api/audio/${testId}`;
}

export function akisAudioUrl(reelId: string) {
  return `${API_URL}/api/akis/audio/${reelId}`;
}

export function adminHeaders(secret: string) {
  return { "X-Admin-Secret": secret };
}
