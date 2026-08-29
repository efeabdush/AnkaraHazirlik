"use client";

import { useEffect, useMemo, useState } from "react";
import { clearExamProgress, EXAM_PROGRESS_EVENT, loadExamProgress, type ExamProgress } from "@/lib/examProgress";

const parts: Array<{ key: keyof ExamProgress; label: string; max: number }> = [
  { key: "session1", label: "1. oturum", max: 60 },
  { key: "writing", label: "2. oturum", max: 20 },
  { key: "speaking", label: "3. oturum", max: 20 },
];

export function ExamProgressSummary() {
  const [progress, setProgress] = useState<ExamProgress>({});
  useEffect(() => {
    const sync = () => setProgress(loadExamProgress());
    sync(); window.addEventListener(EXAM_PROGRESS_EVENT, sync); window.addEventListener("storage", sync);
    return () => { window.removeEventListener(EXAM_PROGRESS_EVENT, sync); window.removeEventListener("storage", sync); };
  }, []);
  const completed = parts.filter((x) => progress[x.key]);
  const total = useMemo(() => parts.reduce((sum, x) => sum + (progress[x.key]?.score ?? 0), 0), [progress]);
  if (!completed.length) return null;
  return <section className="card p-6 sm:p-7"><div className="flex flex-wrap items-start justify-between gap-4"><div><p className="eyebrow">Bu cihazdaki tam sınav ilerlemesi</p><p className="mt-2 font-serif text-4xl text-[var(--navy)]">{total}<span className="text-xl text-[var(--ink-3)]">/100</span></p><p className="prose-quiet mt-2 text-sm">{completed.length === 3 ? (total >= 70 ? "Çalışma tahmininde 70 puan eşiğinin üzerindesin." : "Çalışma tahmininde 70 puan eşiğinin altındasın; bölüm sonuçlarına göre tekrar planla.") : `${completed.length}/3 oturum tamamlandı. Toplam puan bütün oturumlar bitince anlamlıdır.`}</p></div><button type="button" className="btn btn-quiet text-xs" onClick={() => { if (window.confirm("Bu cihazdaki tam sınav ilerlemesi silinsin mi?")) clearExamProgress(); }}>İlerlemeyi sıfırla</button></div><div className="mt-5 grid gap-3 sm:grid-cols-3">{parts.map((part) => { const entry = progress[part.key]; return <div key={part.key} className="rounded-xl border border-[var(--line)] p-4"><p className="text-xs text-[var(--ink-2)]">{part.label}</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{entry ? entry.score : "—"}<span className="text-sm text-[var(--ink-3)]">/{part.max}</span></p></div>; })}</div><p className="mt-4 text-xs text-[var(--ink-3)]">Sonuçlar yalnızca bu tarayıcıda tutulur; sunucuya bir profil kaydı olarak yazılmaz.</p></section>;
}
