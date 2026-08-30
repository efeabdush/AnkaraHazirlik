"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { QuestionList } from "@/components/QuestionList";
import { api, type AttemptDetail, type TestDetail } from "@/lib/api";
import { markPracticeCompleted } from "@/lib/practiceProgress";

function MarkedText({ text }: { text: string }) {
  const parts = text.split(/(\[\[\d+\]\])/g);
  return (
    <>
      {parts.map((part, i) => {
        const hit = part.match(/^\[\[(\d+)\]\]$/);
        return hit ? <span key={i} className="mx-1 inline-flex min-w-10 justify-center rounded-md border border-[var(--gold)] bg-[rgba(176,139,63,0.1)] px-2 py-0.5 font-semibold text-[var(--navy)]">{hit[1]}</span> : part;
      })}
    </>
  );
}

export function AcademicContent({ test }: { test: Pick<TestDetail, "kind" | "content"> }) {
  const content = test.content;
  if (test.kind === "reading_standard") {
    return <div className="space-y-5 text-[0.98rem] leading-8 text-[var(--ink)]">{((content.paragraphs as string[]) ?? []).map((p, i) => <p key={i}>{p}</p>)}</div>;
  }
  if (test.kind === "reading_insertion") {
    const options = (content.sentence_options as Record<string, string>) ?? {};
    return (
      <div className="space-y-6">
        <div className="space-y-5 text-[0.98rem] leading-8">{((content.paragraphs as string[]) ?? []).map((p, i) => <p key={i}><MarkedText text={p} /></p>)}</div>
        <div className="rounded-xl border border-[var(--line)] bg-[rgba(28,61,90,0.04)] p-4">
          <p className="eyebrow">Cümle havuzu · bir cümle fazla</p>
          <div className="mt-3 space-y-2">{Object.entries(options).map(([key, value]) => <p key={key} className="text-sm leading-6"><b className="mr-2 text-[var(--navy)]">{key}</b>{value}</p>)}</div>
        </div>
      </div>
    );
  }
  if (test.kind === "cloze") return <p className="text-[0.98rem] leading-8"><MarkedText text={String(content.text ?? "")} /></p>;
  if (test.kind === "restatement") return <p className="prose-quiet">{String(content.intro ?? "")}</p>;
  return null;
}

export function AcademicPracticeSession({ testId, onBack }: { testId: string; onBack?: () => void }) {
  const router = useRouter();
  const [test, setTest] = useState<TestDetail | null>(null);
  const [mode, setMode] = useState<"exam" | "practice">("practice");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    api<TestDetail>(`/api/tests/${testId}`).then(setTest).catch((e) => setError(e.message));
  }, [testId]);

  const backHref = useMemo(() => test?.kind.startsWith("reading") ? "/reading" : "/use-of-english", [test?.kind]);

  async function submit() {
    if (!test) return;
    setSending(true);
    setError("");
    try {
      const result = await api<AttemptDetail>("/api/attempts", {
        method: "POST",
        body: JSON.stringify({ test_id: test.id, mode, answers, notes: "", plays_used: 0 }),
      });
      markPracticeCompleted(test.id, test.kind);
      router.push(`/results/${result.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gönderilemedi");
      setSending(false);
    }
  }

  if (error && !test) return <p className="text-[var(--terracotta)]">{error}</p>;
  if (!test) return <div className="space-y-4"><div className="card pulse-soft h-28" /><div className="card pulse-soft h-80" /></div>;
  const answered = Object.keys(answers).length;

  return (
    <div className="space-y-7">
      <nav className="text-xs text-[var(--ink-2)]">{onBack ? <button type="button" onClick={onBack} className="hover:text-[var(--navy)]">← Dil çalışmalarına dön</button> : <Link href={backHref} className="hover:text-[var(--navy)]">← Bölüme dön</Link>}</nav>
      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-2"><span className="badge badge-navy">1. oturum</span><span className="badge">B1+ · özgün</span></div>
        <h1 className="font-serif text-3xl text-[var(--navy)] md:text-4xl">{test.title}</h1>
        <p className="prose-quiet max-w-3xl">{test.instructions}</p>
        <div className="inline-flex rounded-xl border border-[var(--line)] bg-[var(--paper)] p-1">
          {(["practice", "exam"] as const).map((value) => <button key={value} type="button" onClick={() => setMode(value)} className={`rounded-lg px-4 py-2 text-sm ${mode === value ? "bg-[var(--navy)] text-white" : "text-[var(--ink-2)]"}`}>{value === "practice" ? "Pratik" : "Sınav"}</button>)}
        </div>
      </header>
      <section className="card p-5 sm:p-7"><AcademicContent test={test} /></section>
      <QuestionList
        questions={test.questions}
        answers={answers}
        onChange={(id, letter) => setAnswers((old) => ({ ...old, [id]: letter }))}
        compactLanguage={test.kind === "cloze" || test.kind === "restatement"}
      />
      <section className="sticky bottom-4 z-20 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-[rgba(253,251,247,0.94)] p-4 shadow-lg backdrop-blur">
        <p className="text-sm text-[var(--ink-2)]">{answered}/{test.questions.length} cevaplandı</p>
        <button type="button" className="btn btn-primary" disabled={sending} onClick={() => void submit()}>{sending ? "Gönderiliyor…" : "Cevapları gönder"}</button>
      </section>
      {error ? <p className="text-sm text-[var(--terracotta)]">{error}</p> : null}
    </div>
  );
}
