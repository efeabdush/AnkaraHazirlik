"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AudioPlayer } from "@/components/AudioPlayer";
import { QuestionList } from "@/components/QuestionList";
import { api, audioUrl, type TestDetail } from "@/lib/api";

type Props = { testId: string; kind: "conversation" | "lecture" };

export function ListeningSession({ testId, kind }: Props) {
  const router = useRouter();
  const [test, setTest] = useState<TestDetail | null>(null);
  const [error, setError] = useState("");
  const [examMode, setExamMode] = useState(true);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [notes, setNotes] = useState("");
  const [plays, setPlays] = useState(0);
  const [manualDone, setManualDone] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api<TestDetail>(`/api/tests/${testId}`)
      .then(setTest)
      .catch((e) => setError(e.message));
  }, [testId]);

  const showQuestions = kind === "conversation" || !examMode || plays >= 2 || manualDone;

  if (error) {
    return (
      <div className="card border-[rgba(176,81,44,0.4)] bg-[rgba(176,81,44,0.05)] p-6">
        <p className="font-medium text-[var(--terracotta)]">Test yüklenemedi</p>
        <p className="prose-quiet mt-1 text-sm">{error}</p>
        <Link href="/listening" className="btn btn-outline mt-4">
          Dinleme listesine dön
        </Link>
      </div>
    );
  }

  if (!test) {
    return (
      <div className="space-y-4">
        <div className="card pulse-soft h-24" />
        <div className="card pulse-soft h-32" />
      </div>
    );
  }

  const answered = test.questions.filter((q) => answers[q.id]).length;
  const total = test.questions.length;

  async function submit() {
    setBusy(true);
    try {
      const attempt = await api<{ id: string }>("/api/attempts", {
        method: "POST",
        body: JSON.stringify({
          test_id: testId,
          mode: examMode ? "exam" : "practice",
          answers,
          notes,
          plays_used: plays,
        }),
      });
      router.push(`/results/${attempt.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gönderilemedi");
      setBusy(false);
    }
  }

  return (
    <div className="space-y-7">
      <nav className="text-xs text-[var(--ink-2)]">
        <Link href="/listening" className="hover:text-[var(--navy)]">
          Dinleme
        </Link>
        <span className="mx-2 text-[var(--line)]">/</span>
        <span>{kind === "conversation" ? "Diyalog" : "Not almalı ders"}</span>
      </nav>

      <header className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <span className={kind === "conversation" ? "badge badge-navy" : "badge badge-gold"}>
            {kind === "conversation" ? "Tracks I–III" : "Track IV · not alma"}
          </span>
          <h1 className="font-serif text-3xl leading-tight tracking-tight text-[var(--navy)] md:text-4xl">
            {test.title}
          </h1>
        </div>

        <div className="card flex items-center gap-3 p-1.5">
          <button
            type="button"
            onClick={() => setExamMode(true)}
            className={`rounded-lg px-3 py-1.5 text-sm transition ${
              examMode ? "bg-[var(--navy)] text-[#f6f1e6]" : "text-[var(--ink-2)] hover:text-[var(--navy)]"
            }`}
          >
            Sınav
          </button>
          <button
            type="button"
            onClick={() => setExamMode(false)}
            className={`rounded-lg px-3 py-1.5 text-sm transition ${
              !examMode ? "bg-[var(--navy)] text-[#f6f1e6]" : "text-[var(--ink-2)] hover:text-[var(--navy)]"
            }`}
          >
            Pratik
          </button>
        </div>
      </header>

      <div className="card border-l-4 border-l-[var(--gold)] p-5">
        <p className="eyebrow">Yönerge</p>
        <p className="mt-2 text-sm leading-relaxed">
          {kind === "conversation" ? (
            <>
              Bir konuşmayı dinle. Kaydı <strong>iki kez</strong> duyacaksın. Her soru için doğru seçeneği işaretle.
              Sorular dinleme sırasında açıktır.
            </>
          ) : (
            <>
              Bir dersi dinle ve not al. Notların <strong>puanlanmaz</strong>. Kaydı <strong>iki kez</strong>
              duyacaksın; sorular dinleme bittikten sonra ayrı sayfa gibi açılır.
            </>
          )}
        </p>
      </div>

      <AudioPlayer src={audioUrl(test.id)} examMode={examMode} onPlaysChange={setPlays} />

      {kind === "lecture" ? (
        <section className="space-y-2">
          <div className="flex items-center justify-between">
            <label htmlFor="notes" className="text-sm font-medium text-[var(--navy)]">
              Notların
            </label>
            <span className="badge">puanlanmaz</span>
          </div>
          <textarea
            id="notes"
            className="ruled w-full rounded-2xl border border-[var(--line)] px-4 py-3 text-sm focus:border-[var(--navy)] focus:outline-none"
            rows={8}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Ana fikir · üç nokta · nedenler · örnekler"
          />
        </section>
      ) : null}

      {showQuestions ? (
        <section className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="font-serif text-2xl text-[var(--navy)]">Sorular</h2>
            <div className="flex items-center gap-3">
              <div className="h-1.5 w-28 overflow-hidden rounded-full bg-[var(--line-soft)]">
                <div
                  className="h-full rounded-full bg-[var(--green)] transition-[width]"
                  style={{ width: `${(answered / total) * 100}%` }}
                />
              </div>
              <span className="text-xs text-[var(--ink-2)]">
                {answered}/{total} işaretli
              </span>
            </div>
          </div>

          <QuestionList
            questions={test.questions}
            answers={answers}
            onChange={(id, letter) => setAnswers((prev) => ({ ...prev, [id]: letter }))}
          />

          <div className="card flex flex-wrap items-center justify-between gap-4 p-5">
            <p className="text-sm text-[var(--ink-2)]">
              {answered < total ? `${total - answered} soru boş. Boş bırakabilirsin.` : "Tüm sorular işaretli."}
            </p>
            <button type="button" disabled={busy} onClick={submit} className="btn btn-primary">
              {busy ? "Gönderiliyor…" : "Cevapları bitir"}
            </button>
          </div>
        </section>
      ) : (
        <section className="card border-dashed p-6 text-center">
          <p className="font-serif text-xl text-[var(--navy)]">Sorular henüz kapalı</p>
          <p className="prose-quiet mx-auto mt-2 max-w-md text-sm">
            Gerçek sınavda soru kitapçığı dinleme bittikten sonra veriliyor. İkinci dinlemeden sonra otomatik açılır.
          </p>
          <button type="button" className="btn btn-outline mt-4" onClick={() => setManualDone(true)}>
            Dinlemeyi bitirdim, soruları aç
          </button>
        </section>
      )}
    </div>
  );
}
