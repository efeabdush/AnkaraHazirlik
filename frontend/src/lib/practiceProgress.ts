"use client";

import { useEffect, useState } from "react";
import { isPracticeKind } from "@/lib/practiceLibrary";

const PRACTICE_PROGRESS_KEY = "ankara-hazirlik-practice-progress-v1";
const PRACTICE_PROGRESS_EVENT = "ankara-hazirlik-practice-progress";

type PracticeProgress = Record<string, { completedAt: string }>;

function loadPracticeProgress(): PracticeProgress {
  if (typeof window === "undefined") return {};

  try {
    const stored = JSON.parse(window.localStorage.getItem(PRACTICE_PROGRESS_KEY) ?? "{}");
    return stored && typeof stored === "object" && !Array.isArray(stored) ? stored as PracticeProgress : {};
  } catch {
    return {};
  }
}

export function markPracticeCompleted(testId: string, kind: string) {
  if (typeof window === "undefined" || !testId || !isPracticeKind(kind)) return;

  try {
    const current = loadPracticeProgress();
    if (current[testId]) return;

    window.localStorage.setItem(
      PRACTICE_PROGRESS_KEY,
      JSON.stringify({ ...current, [testId]: { completedAt: new Date().toISOString() } }),
    );
    window.dispatchEvent(new Event(PRACTICE_PROGRESS_EVENT));
  } catch {
    // Gizli gezinme veya kapalı tarayıcı depolaması test akışını engellemesin.
  }
}

export function useCompletedPracticeIds() {
  const [completedIds, setCompletedIds] = useState<Set<string>>(() => new Set());

  useEffect(() => {
    function refresh() {
      setCompletedIds(new Set(Object.keys(loadPracticeProgress())));
    }

    function handleStorage(event: StorageEvent) {
      if (event.key === PRACTICE_PROGRESS_KEY) refresh();
    }

    refresh();
    window.addEventListener(PRACTICE_PROGRESS_EVENT, refresh);
    window.addEventListener("storage", handleStorage);
    return () => {
      window.removeEventListener(PRACTICE_PROGRESS_EVENT, refresh);
      window.removeEventListener("storage", handleStorage);
    };
  }, []);

  return completedIds;
}
