export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

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

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const isFormData = typeof FormData !== "undefined" && init?.body instanceof FormData;
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) {
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

export function adminHeaders(secret: string) {
  return { "X-Admin-Secret": secret };
}
