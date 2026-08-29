"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AcademicContent } from "@/components/AcademicPracticeSession";
import { AudioPlayer } from "@/components/AudioPlayer";
import { QuestionList } from "@/components/QuestionList";
import { api, audioUrl, type AttemptDetail, type TestDetail, type TestSummary } from "@/lib/api";
import { saveExamProgress } from "@/lib/examProgress";

type ExamItem = TestDetail & { section: "listening" | "reading" | "use"; label: string };
type ResultItem = { id: string; section: ExamItem["section"]; score: number; max_score: number; title: string };
const labels = { listening: "Dinleme", reading: "Okuma", use: "Dil Kullanımı" };
const EXPECTED_ITEMS: Record<string, number> = { conversation: 3, lecture: 1, reading_standard: 2, reading_insertion: 1, cloze: 3, restatement: 1 };
const fmt = (sec: number) => `${Math.floor(Math.max(0, sec) / 60).toString().padStart(2, "0")}:${(Math.max(0, sec) % 60).toString().padStart(2, "0")}`;

export function FullSessionOne() {
  const [items, setItems] = useState<ExamItem[]>([]); const [loading, setLoading] = useState(true); const [started, setStarted] = useState(false); const [index, setIndex] = useState(0); const [remaining, setRemaining] = useState(7200);
  const [answers, setAnswers] = useState<Record<string, Record<string, string>>>({}); const [notes, setNotes] = useState<Record<string, string>>({}); const [plays, setPlays] = useState<Record<string, number>>({}); const [lectureOpen, setLectureOpen] = useState(false);
  const [sending, setSending] = useState(false); const [results, setResults] = useState<ResultItem[]>([]); const [error, setError] = useState("");

  useEffect(() => {
    const kinds = ["conversation", "lecture", "reading_standard", "reading_insertion", "cloze", "restatement"];
    Promise.all(kinds.map((kind) => api<TestSummary[]>(`/api/tests?kind=${kind}`))).then(async ([convs, lectures, readings, insertions, clozes, restatements]) => {
      const chosen = [
        ...convs.slice(0, 3).map((x, i) => ({ ...x, section: "listening" as const, label: `Track ${["I", "II", "III"][i]}` })),
        ...lectures.slice(0, 1).map((x) => ({ ...x, section: "listening" as const, label: "Track IV · Not alma" })),
        ...readings.slice(0, 2).map((x, i) => ({ ...x, section: "reading" as const, label: `Passage ${["I", "II"][i]}` })),
        ...insertions.slice(0, 1).map((x) => ({ ...x, section: "reading" as const, label: "Passage III · Cümle yerleştirme" })),
        ...clozes.slice(0, 3).map((x, i) => ({ ...x, section: "use" as const, label: `Cloze Text ${["I", "II", "III"][i]}` })),
        ...restatements.slice(0, 1).map((x) => ({ ...x, section: "use" as const, label: "Restatement" })),
      ];
      const details = await Promise.all(chosen.map(async (x) => ({ ...(await api<TestDetail>(`/api/tests/${x.id}`)), section: x.section, label: x.label })));
      setItems(details); setLoading(false);
    }).catch((e) => { setError(e.message); setLoading(false); });
  }, []);

  useEffect(() => { if (!started || results.length) return; const t = window.setInterval(() => setRemaining((v) => Math.max(0, v - 1)), 1000); return () => window.clearInterval(t); }, [started, results.length]);
  const current = items[index];
  const missing = useMemo(() => Object.entries(EXPECTED_ITEMS).filter(([kind, n]) => items.filter((x) => x.kind === kind).length < n).map(([kind]) => kind), [items]);

  async function finishExam() {
    setSending(true); setError("");
    try {
      const graded = await Promise.all(items.map(async (item) => {
        const attempt = await api<AttemptDetail>("/api/attempts", { method: "POST", body: JSON.stringify({ test_id: item.id, mode: "exam", answers: answers[item.id] ?? {}, notes: notes[item.id] ?? "", plays_used: plays[item.id] ?? 0 }) });
        return { id: attempt.id, section: item.section, score: attempt.score, max_score: attempt.max_score, title: item.title };
      }));
      setResults(graded);
      const breakdown = Object.fromEntries(Object.keys(labels).map((section) => [section, graded.filter((r) => r.section === section).reduce((sum, r) => sum + r.score, 0)]));
      saveExamProgress({ session1: { score: Object.values(breakdown).reduce((sum, score) => sum + Number(score), 0), breakdown, completedAt: new Date().toISOString() } });
    } catch (e) { setError(e instanceof Error ? e.message : "Oturum gönderilemedi"); } finally { setSending(false); }
  }

  if (loading) return <div className="space-y-4"><div className="card pulse-soft h-32" /><div className="card pulse-soft h-80" /></div>;
  if (!started) return <div className="space-y-8"><header className="space-y-3"><span className="badge badge-navy">1. oturum · tam deneme</span><h1 className="font-serif text-4xl text-[var(--navy)]">Dinleme, Okuma, Dil Kullanımı</h1><p className="prose-quiet max-w-3xl">120 dakika, toplam 60 puan. İçerikler gerçek sınavın bölüm ve puan dağılımını izler; tamamı özgündür.</p></header><section className="card p-6"><div className="grid gap-4 sm:grid-cols-3">{Object.entries(labels).map(([key, label]) => <div key={key} className="rounded-xl border border-[var(--line)] p-4"><p className="font-serif text-xl text-[var(--navy)]">{label}</p><p className="mt-1 text-sm text-[var(--ink-2)]">20 puan</p></div>)}</div>{missing.length ? <p className="mt-5 rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">Tam oturum için içerik havuzu henüz yüklenmedi: {missing.join(", ")}. Uygulamayı yeniden başlatınca başlangıç paketleri eklenir.</p> : null}<button type="button" className="btn btn-primary mt-6" disabled={Boolean(missing.length)} onClick={() => setStarted(true)}>120 dakikalık oturumu başlat</button></section><Link href="/exam" className="btn btn-outline">Sınav merkezine dön</Link></div>;

  if (results.length) {
    const sectionScores = Object.fromEntries(Object.keys(labels).map((section) => [section, results.filter((r) => r.section === section).reduce((sum, r) => sum + r.score, 0)])); const total = Object.values(sectionScores).reduce((a, b) => Number(a) + Number(b), 0); const enough = total >= 29.5;
    return <div className="space-y-7"><header className="space-y-2"><span className="badge badge-navy">1. oturum sonucu</span><h1 className="font-serif text-4xl text-[var(--navy)]">{total}<span className="text-2xl text-[var(--ink-3)]">/60</span></h1><p className={enough ? "text-[var(--green)]" : "text-[var(--terracotta)]"}>{enough ? "Gerçek sınavdaki 29,5 puanlık oturum barajını geçebilecek düzeydesin." : "Bu sonuç gerçek sınavdaki 29,5 puanlık oturum barajı için yetersiz. Diğer oturumları çalışmaya devam edebilirsin."}</p></header><section className="grid gap-4 sm:grid-cols-3">{Object.entries(labels).map(([key, label]) => <div key={key} className="card p-5"><p className="eyebrow">{label}</p><p className="mt-2 font-serif text-3xl text-[var(--navy)]">{sectionScores[key]}<span className="text-base text-[var(--ink-3)]">/20</span></p></div>)}</section><section className="card divide-y divide-[var(--line-soft)]">{results.map((r) => <div key={r.id} className="flex flex-wrap items-center justify-between gap-3 p-4"><span className="text-sm">{r.title}</span><span className="flex items-center gap-3"><b className="text-[var(--navy)]">{r.score}/{r.max_score}</b><Link href={`/results/${r.id}`} className="btn btn-outline text-xs">Çözümler</Link></span></div>)}</section><div className="flex flex-wrap gap-3"><Link href="/writing" className="btn btn-primary">2. oturum: Yazma</Link><Link href="/speaking" className="btn btn-outline">3. oturum: Konuşma</Link></div></div>;
  }

  const isListening = current.kind === "conversation" || current.kind === "lecture"; const isLecture = current.kind === "lecture"; const showQuestions = !isLecture || lectureOpen;
  return <div className="space-y-6"><header className="sticky top-[7.2rem] z-20 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-[rgba(253,251,247,.95)] p-4 shadow-sm backdrop-blur sm:top-20"><div><p className="eyebrow">{labels[current.section]} · {current.label}</p><p className="font-medium text-[var(--navy)]">{index + 1}/{items.length} · {current.title}</p></div><span className={`font-serif text-2xl ${remaining < 900 ? "text-[var(--terracotta)]" : "text-[var(--navy)]"}`}>{fmt(remaining)}</span></header>{isListening ? <><AudioPlayer key={current.id} src={audioUrl(current.id)} examMode onPlaysChange={(n) => setPlays((old) => ({ ...old, [current.id]: n }))} />{isLecture ? <section className="card p-5"><p className="eyebrow">Notların · puanlanmaz</p><textarea className="ruled mt-3 min-h-52 w-full resize-y bg-transparent p-2 outline-none" value={notes[current.id] ?? ""} onChange={(e) => setNotes((old) => ({ ...old, [current.id]: e.target.value }))} />{!lectureOpen ? <button type="button" className="btn btn-outline mt-3" onClick={() => setLectureOpen(true)}>Dinlemeyi bitirdim, soruları aç</button> : null}</section> : null}</> : <section className="card p-5 sm:p-7"><AcademicContent test={current} /></section>}{showQuestions ? <QuestionList questions={current.questions} answers={answers[current.id] ?? {}} onChange={(id, letter) => setAnswers((old) => ({ ...old, [current.id]: { ...(old[current.id] ?? {}), [id]: letter } }))} /> : <div className="card border-dashed p-6 text-sm text-[var(--ink-2)]">Track IV soruları kayıt ve not alma tamamlanınca açılır.</div>}<div className="flex flex-wrap items-center justify-between gap-3"><p className="text-sm text-[var(--ink-2)]">{Object.keys(answers[current.id] ?? {}).length}/{current.questions.length} cevaplandı</p>{index < items.length - 1 ? <button type="button" className="btn btn-primary" disabled={!showQuestions} onClick={() => { setIndex((v) => v + 1); setLectureOpen(false); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Sonraki bölüm →</button> : <button type="button" className="btn btn-primary" disabled={sending} onClick={() => void finishExam()}>{sending ? "Puanlanıyor…" : "1. oturumu bitir"}</button>}</div>{error ? <p className="text-sm text-[var(--terracotta)]">{error}</p> : null}</div>;
}
