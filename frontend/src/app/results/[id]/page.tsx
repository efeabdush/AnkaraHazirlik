"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ExplainChat } from "@/components/ExplainChat";
import { AcademicContent } from "@/components/AcademicPracticeSession";
import { SelectTranslate } from "@/components/SelectTranslate";
import { api, type AttemptDetail } from "@/lib/api";
import { isPracticeKind } from "@/lib/practiceLibrary";
import { markPracticeCompleted } from "@/lib/practiceProgress";

export default function ResultsPage({ params }: { params: Promise<{ id: string }> }) {
  const [attempt, setAttempt] = useState<AttemptDetail | null>(null);
  const [error, setError] = useState("");
  const [id, setId] = useState("");
  const [showTranscript, setShowTranscript] = useState(false);

  useEffect(() => {
    params.then(({ id: value }) => {
      setId(value);
      api<AttemptDetail>(`/api/attempts/${value}`)
        .then((result) => {
          markPracticeCompleted(result.test_id, result.kind);
          setAttempt(result);
        })
        .catch((e) => setError(e.message));
    });
  }, [params]);

  if (error) return <p className="text-[var(--terracotta)]">{error}</p>;

  if (!attempt) {
    return (
      <div className="space-y-4">
        <div className="card pulse-soft h-32" />
        <div className="card pulse-soft h-40" />
      </div>
    );
  }

  const pct = attempt.max_score ? Math.round((attempt.score / attempt.max_score) * 100) : 0;
  const correctCount = attempt.questions.filter((q) => q.correct).length;
  const glossary = attempt.glossary ?? [];
  const words = attempt.words ?? {};
  const aidsReady = glossary.length > 0 || Object.keys(words).length > 0;
  const isListening = attempt.kind === "conversation" || attempt.kind === "lecture";
  const sectionHref = attempt.kind.startsWith("reading")
    ? "/reading"
    : attempt.kind === "cloze" || attempt.kind === "restatement"
      ? "/use-of-english"
      : "/listening";
  const sectionLabel = attempt.kind.startsWith("reading")
    ? "Okuma"
    : attempt.kind === "cloze" || attempt.kind === "restatement"
      ? "Dil kullanımı"
      : "Dinleme";
  const discoveryHref = isPracticeKind(attempt.kind)
    ? `/practice-library/${attempt.kind}`
    : sectionHref;

  return (
    <div className="space-y-8">
      <nav className="text-xs text-[var(--ink-2)]">
        <Link href={sectionHref} className="hover:text-[var(--navy)]">
          {sectionLabel}
        </Link>
        <span className="mx-2 text-[var(--line)]">/</span>
        <span>Sonuç</span>
      </nav>

      <section className="card rise flex flex-wrap items-center justify-between gap-6 p-7">
        <div className="space-y-2">
          <span className="badge">{attempt.mode === "exam" ? "Sınav modu" : "Pratik modu"}</span>
          <h1 className="font-serif text-3xl leading-tight text-[var(--navy)]">{attempt.title}</h1>
          <p className="prose-quiet text-sm">
            {correctCount}/{attempt.questions.length} soru doğru
          </p>
        </div>

        <div className="flex items-center gap-5">
          <div
            className="grid h-24 w-24 place-items-center rounded-full"
            style={{
              background: `conic-gradient(var(--navy) ${pct}%, var(--line-soft) ${pct}% 100%)`,
            }}
          >
            <div className="grid h-[76px] w-[76px] place-items-center rounded-full bg-[var(--paper)]">
              <span className="font-serif text-2xl text-[var(--navy)]">{pct}%</span>
            </div>
          </div>
          <div>
            <p className="font-serif text-4xl text-[var(--navy)]">
              {attempt.score}
              <span className="text-xl text-[var(--ink-3)]">/{attempt.max_score}</span>
            </p>
            <p className="text-xs text-[var(--ink-2)]">puan</p>
          </div>
        </div>
      </section>

      {aidsReady ? (
        <p className="rounded-xl border border-[var(--line)] bg-[var(--paper)] px-4 py-3 text-sm text-[var(--ink-2)]">
          Tek bir kelimeye tıkla, sadece o kelimenin Türkçesi çıkar. Bir kelime grubu seçersen grubun karşılığı, tüm
          cümleyi seçersen cümlenin çevirisi görünür. Hepsi test hazırlanırken kaydedilir, seçince yapay zeka
          çağrılmaz.
        </p>
      ) : null}

      {!isListening && Object.keys(attempt.content ?? {}).length ? (
        <section className="card p-5 sm:p-7">
          <p className="eyebrow mb-4">Kaynak metin</p>
          <SelectTranslate glossary={glossary} words={words}>
            <AcademicContent test={attempt} />
          </SelectTranslate>
        </section>
      ) : null}

      <section className="space-y-4">
        <h2 className="font-serif text-2xl text-[var(--navy)]">Soru çözümleri</h2>
        <ol className="space-y-4">
          {attempt.questions.map((q) => (
            <li key={q.id} className={`card p-5 ${q.correct ? "border-l-4 border-l-[var(--green)]" : "border-l-4 border-l-[var(--terracotta)]"}`}>
              <SelectTranslate glossary={glossary} words={words}>
                <div className="flex items-start justify-between gap-4">
                  <p className="font-medium leading-relaxed text-[var(--navy)]">
                    <span className="mr-2 font-serif text-[var(--gold)]">{q.order}.</span>
                    {q.stem}
                  </p>
                  <span className={q.correct ? "badge badge-green flex-none" : "badge badge-warn flex-none"}>
                    {q.correct ? `+${q.points}` : "0"}
                  </span>
                </div>

                <div className="mt-4 grid gap-2">
                  {Object.keys(q.options).sort().map((letter) => {
                    const isKey = q.answer === letter;
                    const isPick = q.chosen === letter;
                    const cls = isKey ? "choice choice-correct" : isPick ? "choice choice-wrong" : "choice";
                    return (
                      <div key={letter} className={`${cls} cursor-default`}>
                        <span className="choice-letter">{letter}</span>
                        <span className="text-sm leading-relaxed">{q.options[letter]}</span>
                        {isKey ? <span className="badge badge-green ml-auto flex-none">doğru</span> : null}
                        {isPick && !isKey ? <span className="badge badge-warn ml-auto flex-none">senin</span> : null}
                      </div>
                    );
                  })}
                </div>

                {q.rationale ? (
                  <div className="mt-4 rounded-xl bg-[rgba(28,61,90,0.05)] p-4">
                    <p className="eyebrow">Neden</p>
                    <p className="mt-1 text-sm leading-relaxed">{q.rationale}</p>
                  </div>
                ) : null}
              </SelectTranslate>

              {id ? (
                <div className="no-translate">
                  <ExplainChat attemptId={id} questionId={q.id} />
                </div>
              ) : null}
            </li>
          ))}
        </ol>
      </section>

      {attempt.notes ? (
        <section className="card p-6">
          <h2 className="font-serif text-xl text-[var(--navy)]">Notların</h2>
          <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-[var(--ink-2)]">{attempt.notes}</p>
        </section>
      ) : null}

      {isListening ? <section className="card overflow-hidden">
        <button
          type="button"
          onClick={() => setShowTranscript((v) => !v)}
          className="flex w-full items-center justify-between gap-4 p-6 text-left"
        >
          <div>
            <h2 className="font-serif text-xl text-[var(--navy)]">Kayıt metni</h2>
            <p className="prose-quiet mt-1 text-sm">Puanı gördükten sonra açılır. Kelimeye tıklayınca Türkçesi çıkar.</p>
          </div>
          <span className="badge">{showTranscript ? "kapat" : "göster"}</span>
        </button>
        {showTranscript ? (
          <SelectTranslate glossary={glossary} words={words}>
            <div className="space-y-3 border-t border-[var(--line)] p-6 text-sm leading-7">
              {attempt.transcript.map((line, i) => (
                <p key={i}>
                  <span className="mr-2 font-medium capitalize text-[var(--navy)]">{line.speaker}:</span>
                  {line.text}
                </p>
              ))}
            </div>
          </SelectTranslate>
        ) : null}
      </section> : null}

      <div className="flex flex-wrap gap-3">
        <Link href={discoveryHref} className="btn btn-primary">
          Başka test çöz
        </Link>
        <Link href={isListening ? `/listening/${attempt.kind === "lecture" ? "lecture" : "conversation"}/${attempt.test_id}` : `/practice/${attempt.test_id}`} className="btn btn-outline">
          Bu testi tekrar çöz
        </Link>
      </div>
    </div>
  );
}
