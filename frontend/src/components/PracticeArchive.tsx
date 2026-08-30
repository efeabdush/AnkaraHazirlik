"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, type TestSummary } from "@/lib/api";
import { practiceHref, practiceLibrary, type PracticeKind } from "@/lib/practiceLibrary";

export function PracticeArchive({ kind }: { kind: PracticeKind }) {
  const meta = practiceLibrary[kind];
  const [tests, setTests] = useState<TestSummary[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api<TestSummary[]>(`/api/tests?kind=${kind}`)
      .then(setTests)
      .catch((caught) => setError(caught instanceof Error ? caught.message : "Çalışmalar alınamadı"));
  }, [kind]);

  return (
    <div className="space-y-8">
      <header className="space-y-4">
        <Link href={meta.backHref} className="inline-flex items-center gap-2 text-sm font-semibold text-[var(--navy)] hover:underline">
          ← {meta.backLabel}
        </Link>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-3xl">
            <p className="eyebrow">{meta.eyebrow}</p>
            <h1 className="mt-2 font-serif text-4xl tracking-tight text-[var(--navy)]">{meta.label}</h1>
            <p className="prose-quiet mt-3">{meta.description}</p>
          </div>
          <span className="badge badge-gold">{tests?.length ?? 25} çalışma</span>
        </div>
      </header>

      {error ? <p className="rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">{error}</p> : null}
      {tests === null && !error ? (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{Array.from({ length: 6 }, (_, index) => <div key={index} className="card pulse-soft h-32" />)}</div>
      ) : null}
      {tests ? (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {tests.map((test, index) => (
            <Link key={test.id} href={practiceHref(kind, test.id)} className="card card-lift group flex min-h-32 flex-col justify-between p-5">
              <span>
                <span className="eyebrow">Çalışma {String(index + 1).padStart(2, "0")}</span>
                <span className="mt-2 block font-serif text-xl leading-snug text-[var(--navy)]">{test.title}</span>
              </span>
              <span className="mt-4 flex items-center justify-between text-xs text-[var(--ink-2)]">
                <span>{test.cefr} · özgün çalışma</span>
                <span className="text-base text-[var(--gold)] transition-transform group-hover:translate-x-1">→</span>
              </span>
            </Link>
          ))}
        </div>
      ) : null}
    </div>
  );
}
