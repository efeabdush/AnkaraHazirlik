export const EXAM_PROGRESS_KEY = "ankara-hazirlik-full-exam-v1";
export const EXAM_PROGRESS_EVENT = "ankara-hazirlik-progress";

export type ExamProgress = {
  session1?: { score: number; breakdown: Record<string, number>; completedAt: string };
  writing?: { score: number; completedAt: string };
  speaking?: { score: number; completedAt: string };
};

export function loadExamProgress(): ExamProgress {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(window.localStorage.getItem(EXAM_PROGRESS_KEY) ?? "{}") as ExamProgress;
  } catch {
    return {};
  }
}

export function saveExamProgress(update: Partial<ExamProgress>) {
  if (typeof window === "undefined") return;
  const next = { ...loadExamProgress(), ...update };
  window.localStorage.setItem(EXAM_PROGRESS_KEY, JSON.stringify(next));
  window.dispatchEvent(new Event(EXAM_PROGRESS_EVENT));
}

export function clearExamProgress() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(EXAM_PROGRESS_KEY);
  window.dispatchEvent(new Event(EXAM_PROGRESS_EVENT));
}
