"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { saveExamProgress } from "@/lib/examProgress";
import { writingTopics, type WritingTopic } from "@/data/writingTopics";
import { MarkdownText } from "@/components/MarkdownText";

type WritingResult = {
  scores: Record<string, number>;
  raw_total_10: number;
  session_score_20: number;
  word_count: number;
  minimum_met: boolean;
  level_summary_tr: string;
  strengths_tr: string[];
  priorities_tr: string[];
  sentence_fixes: { original: string; improved: string; reason_tr: string }[];
  next_practice_tr: string[];
  disclaimer_tr: string;
};

const labels: Record<string, string> = {
  task_completion: "Görevi tamamlama",
  grammar: "Dil bilgisi",
  vocabulary: "Kelime",
  coherence_cohesion: "Tutarlılık ve bağlaşıklık",
};

function formatTime(seconds: number) {
  const safe = Math.max(0, seconds);
  return `${Math.floor(safe / 60).toString().padStart(2, "0")}:${(safe % 60).toString().padStart(2, "0")}`;
}

export function WritingPractice() {
  const [selected, setSelected] = useState<WritingTopic | null>(null);
  const [rolling, setRolling] = useState(false);
  const [rollingTheme, setRollingTheme] = useState("Tema havuzu hazır");
  const [essay, setEssay] = useState("");
  const [remaining, setRemaining] = useState(60 * 60);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<WritingResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!running) return;
    const timer = window.setInterval(() => setRemaining((value) => {
      if (value <= 1) { setRunning(false); return 0; }
      return value - 1;
    }), 1000);
    return () => window.clearInterval(timer);
  }, [running]);

  const wordCount = useMemo(() => essay.trim().match(/[A-Za-z]+(?:['’-][A-Za-z]+)?/g)?.length ?? 0, [essay]);
  const prompt = selected?.prompt ?? "";

  async function evaluate() {
    if (!prompt || essay.trim().length < 20) return;
    setBusy(true); setError(""); setResult(null); setRunning(false);
    try {
      const evaluation = await api<WritingResult>("/api/evaluate/writing", { method: "POST", body: JSON.stringify({ prompt, essay }) });
      setResult(evaluation);
      saveExamProgress({ writing: { score: evaluation.session_score_20, completedAt: new Date().toISOString() } });
    } catch (e) { setError(e instanceof Error ? e.message : "Değerlendirilemedi"); }
    finally { setBusy(false); }
  }

  function resetEssay() { setEssay(""); setResult(null); setRemaining(3600); setRunning(false); setError(""); }

  function drawTopic() {
    if (rolling) return;
    resetEssay(); setSelected(null); setRolling(true); let tick = 0;
    const interval = window.setInterval(() => { setRollingTheme(writingTopics[tick % writingTopics.length].theme); tick += 1; }, 75);
    window.setTimeout(() => {
      window.clearInterval(interval);
      const pool = writingTopics.filter((topic) => topic.id !== selected?.id);
      const chosen = pool[Math.floor(Math.random() * pool.length)] ?? writingTopics[0];
      setRollingTheme(chosen.theme); setSelected(chosen); setRolling(false);
    }, 1500);
  }

  return (
    <div className="space-y-8">
      <header className="space-y-3">
        <div className="flex flex-wrap gap-2"><span className="badge badge-gold">2. oturum · 20 puan</span><span className="badge">60 dakika</span></div>
        <h1 className="font-serif text-4xl text-[var(--navy)]">Yazma</h1>
        <p className="prose-quiet max-w-3xl">En az 250 kelimelik bir opinion essay yaz. Değerlendirme resmî ölçütlerin dört başlığını izler; verilen puan çalışma amaçlı AI tahminidir.</p>
      </header>

      <section className="grid gap-4 lg:grid-cols-[0.72fr_1.28fr]">
        <aside className="space-y-4">
          <div className="card p-5">
            <div className="flex items-center justify-between gap-3"><span className="eyebrow">Tema çekilişi</span><span className="badge">50 özgün tema</span></div>
            <div className={`mt-4 grid min-h-28 place-items-center rounded-xl border border-[var(--line)] bg-[linear-gradient(150deg,rgba(28,61,90,.05),rgba(176,139,63,.1))] p-4 text-center ${rolling ? "pulse-soft" : ""}`}><p className="font-serif text-2xl leading-tight text-[var(--navy)]">{rollingTheme}</p></div>
            <button type="button" className="btn btn-primary mt-4 w-full" disabled={rolling} onClick={drawTopic}>{rolling ? "Temalar geçiyor…" : selected ? "Başka tema çek" : "Konu temasını çek"}</button>
            {selected && !rolling ? <div className="rise mt-5 border-t border-[var(--line)] pt-5"><p className="eyebrow">Bu temanın sorusu</p><p className="mt-2 font-serif text-xl leading-7 text-[var(--navy)]">{prompt}</p></div> : <p className="prose-quiet mt-4 text-xs">Önce tema belirlenir; yazacağın soru tema durduktan sonra açılır.</p>}
          </div>
          <div className="card p-5">
            <div className="flex items-center justify-between"><span className="eyebrow">Süre</span><span className={`font-serif text-3xl ${remaining < 600 ? "text-[var(--terracotta)]" : "text-[var(--navy)]"}`}>{formatTime(remaining)}</span></div>
            <button type="button" className="btn btn-outline mt-4 w-full" onClick={() => setRunning((v) => !v)}>{running ? "Sayacı durdur" : remaining === 3600 ? "60 dakikayı başlat" : "Sayacı sürdür"}</button>
          </div>
          <div className="rounded-xl border border-[var(--line)] p-4 text-xs leading-6 text-[var(--ink-2)]"><b className="text-[var(--navy)]">Dört ölçüt:</b> görevi tamamlama, dil bilgisi, kelime, tutarlılık-bağlaşıklık.</div>
        </aside>

        <div className="card overflow-hidden">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--line)] px-5 py-3"><span className="eyebrow">Kompozisyonun</span><span className={wordCount >= 250 ? "badge badge-green" : "badge badge-warn"}>{wordCount} / 250+ kelime</span></div>
          <textarea className="min-h-[34rem] w-full resize-y bg-[var(--paper)] p-5 text-[1rem] leading-8 outline-none disabled:cursor-not-allowed disabled:opacity-55 sm:p-7" value={essay} onChange={(e) => setEssay(e.target.value)} placeholder={selected ? "Write your opinion essay here…" : "Önce soldan bir konu teması çek…"} spellCheck="true" disabled={!selected || rolling} />
          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-[var(--line)] p-4"><button type="button" className="btn btn-quiet" onClick={resetEssay}>Metni temizle</button><button type="button" className="btn btn-primary" disabled={busy || !selected || essay.trim().length < 20} onClick={() => void evaluate()}>{busy ? "Rubrik uygulanıyor…" : "Yazımı değerlendir"}</button></div>
        </div>
      </section>

      {error ? <p className="rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">{error}</p> : null}
      {result ? (
        <section className="space-y-5">
          {!result.minimum_met ? <div className="rounded-xl border border-[var(--terracotta)] bg-[rgba(176,81,44,0.06)] p-4 text-sm text-[var(--terracotta)]">250 kelime sınırının altındasın. Gerçek sınav beklentisini henüz karşılamıyor.</div> : null}
          <div className="card grid gap-5 p-6 md:grid-cols-[0.35fr_0.65fr] md:p-7">
            <div><p className="eyebrow">Çalışma puanı</p><p className="mt-2 font-serif text-5xl text-[var(--navy)]">{result.session_score_20}<span className="text-xl text-[var(--ink-3)]">/20</span></p><MarkdownText className="prose-quiet mt-3 text-sm">{result.level_summary_tr}</MarkdownText></div>
            <div className="grid gap-3 sm:grid-cols-2">{Object.entries(result.scores).map(([key, value]) => <div key={key} className="rounded-xl border border-[var(--line)] p-4"><p className="text-xs text-[var(--ink-2)]">{labels[key] ?? key}</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{value}<span className="text-sm text-[var(--ink-3)]">/2.5</span></p></div>)}</div>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Önce bunları düzelt</h2><ul className="mt-3 space-y-2 text-sm leading-6">{result.priorities_tr.map((x, i) => <li key={i} className="flex gap-2"><span className="text-[var(--gold)]">{i + 1}.</span><MarkdownText className="min-w-0">{x}</MarkdownText></li>)}</ul></div>
            <div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Sonraki çalışma</h2><ul className="mt-3 space-y-2 text-sm leading-6">{result.next_practice_tr.map((x, i) => <li key={i} className="flex gap-2"><span className="text-[var(--green)]">✓</span><MarkdownText className="min-w-0">{x}</MarkdownText></li>)}</ul></div>
          </div>
          {result.sentence_fixes.length ? <div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Somut düzeltmeler</h2><div className="mt-4 space-y-4">{result.sentence_fixes.map((fix, i) => <div key={i} className="border-l-2 border-[var(--gold)] pl-4 text-sm"><MarkdownText className="text-[var(--terracotta)] line-through decoration-[rgba(176,81,44,0.45)]">{fix.original}</MarkdownText><MarkdownText className="mt-1 font-medium text-[var(--green)]">{fix.improved}</MarkdownText><MarkdownText className="prose-quiet mt-1 text-xs">{fix.reason_tr}</MarkdownText></div>)}</div></div> : null}
          <MarkdownText className="text-xs text-[var(--ink-3)]">{result.disclaimer_tr}</MarkdownText>
          <div className="flex flex-wrap gap-3"><Link href="/speaking" className="btn btn-primary">3. oturuma geç</Link><Link href="/exam" className="btn btn-outline">Sınav puanlarını gör</Link></div>
        </section>
      ) : null}
    </div>
  );
}
