"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type TestSummary } from "@/lib/api";
import { PracticeMoreCard } from "@/components/PracticeMoreCard";

export default function ListeningPage() {
  const [tests, setTests] = useState<TestSummary[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api<TestSummary[]>("/api/tests?kind=conversation"),
      api<TestSummary[]>("/api/tests?kind=lecture"),
    ])
      .then((groups) => setTests(groups.flat()))
      .catch((e) => setError(e instanceof Error ? e.message : "İçerikler alınamadı"));
  }, []);

  const conv = tests?.filter((t) => t.kind === "conversation") ?? [];
  const lect = tests?.filter((t) => t.kind === "lecture") ?? [];

  return (
    <div className="space-y-12">
      <header className="space-y-3">
        <p className="eyebrow">1. oturum · 20 puan</p>
        <h1 className="font-serif text-4xl tracking-tight text-[var(--navy)]">Dinleme</h1>
        <p className="prose-quiet max-w-2xl">
          Gerçek sınavda dinleme bölümü <strong className="text-[var(--navy)]">dört kayıttan</strong> oluşur: ilk üçü
          kısa diyalog, dördüncüsü not almalı ders. Burada ikisini de aynı düzende çalışırsın.
        </p>
      </header>

      {/* format explainer */}
      <div className="grid gap-3 sm:grid-cols-2">
        <div className="card flex items-start gap-4 p-5">
          <span className="grid h-10 w-10 flex-none place-items-center rounded-xl bg-[rgba(28,61,90,0.08)] font-serif text-sm font-semibold text-[var(--navy)]">
            I–III
          </span>
          <div>
            <p className="font-medium text-[var(--navy)]">Diyalog kayıtları</p>
            <p className="prose-quiet mt-1 text-sm">
              Kısa kampüs konuşmaları. Sorular dinlerken önünde açıktır, kayıt sürerken işaretlersin.
            </p>
          </div>
        </div>
        <div className="card flex items-start gap-4 p-5">
          <span className="grid h-10 w-10 flex-none place-items-center rounded-xl bg-[rgba(176,139,63,0.14)] font-serif text-sm font-semibold text-[#7d6027]">
            IV
          </span>
          <div>
            <p className="font-medium text-[var(--navy)]">Not almalı ders</p>
            <p className="prose-quiet mt-1 text-sm">
              Beş dakikalık ders. Önce not alırsın; sorular kayıt bittikten sonra açılır. Notlar puanlanmaz.
            </p>
          </div>
        </div>
      </div>

      {error ? (
        <div className="card border-[rgba(176,81,44,0.4)] bg-[rgba(176,81,44,0.05)] p-5">
          <p className="font-medium text-[var(--terracotta)]">Sunucuya ulaşılamadı</p>
          <p className="prose-quiet mt-1 text-sm">
            {error}. Backend’in <code className="rounded bg-white px-1.5 py-0.5">localhost:8000</code> üzerinde açık
            olduğundan emin ol.
          </p>
        </div>
      ) : null}

      <Section
        badge="Track I–III"
        tone="badge-navy"
        title="Diyalog"
        desc="Kısa kampüs konuşması. Dört soru, her biri 1 puan; dinlerken işaretlenir."
        tests={conv}
        loading={tests === null && !error}
        href={(id) => `/listening/conversation/${id}`}
        archiveHref="/practice-library/conversation"
      />

      <Section
        badge="Track IV"
        tone="badge-gold"
        title="Not almalı ders"
        desc="Yaklaşık beş dakika. Çizgili deftere not al; sorular dinleme bitince gelir."
        tests={lect}
        loading={tests === null && !error}
        href={(id) => `/listening/lecture/${id}`}
        archiveHref="/practice-library/lecture"
      />
    </div>
  );
}

function Section({
  badge,
  tone,
  title,
  desc,
  tests,
  loading,
  href,
  archiveHref,
}: {
  badge: string;
  tone: string;
  title: string;
  desc: string;
  tests: TestSummary[];
  loading: boolean;
  href: (id: string) => string;
  archiveHref: string;
}) {
  return (
    <section className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <span className={tone}>{badge}</span>
        <h2 className="font-serif text-2xl text-[var(--navy)]">{title}</h2>
      </div>
      <p className="prose-quiet max-w-2xl text-sm">{desc}</p>

      {loading ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {[0, 1].map((i) => (
            <div key={i} className="card pulse-soft h-28 p-5" />
          ))}
        </div>
      ) : tests.length === 0 ? (
        <div className="card border-dashed p-6 text-sm text-[var(--ink-2)]">Henüz yayımlanmış test yok.</div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {tests.slice(0, 2).map((t) => (
            <Link
              key={t.id}
              href={href(t.id)}
              className="card card-lift group relative flex flex-col gap-3 overflow-hidden p-5 pl-6"
            >
              <span className="absolute inset-y-0 left-0 w-1 bg-gradient-to-b from-[var(--navy)] to-[var(--gold)] opacity-70 transition-opacity group-hover:opacity-100" />
              <div className="flex items-start justify-between gap-3">
                <h3 className="font-serif text-lg leading-snug text-[var(--navy)]">{t.title}</h3>
                <span className="badge">{t.cefr}</span>
              </div>
              <div className="mt-auto flex items-center justify-between text-xs text-[var(--ink-2)]">
                <span className="capitalize">{t.topic}</span>
                <span className="flex items-center gap-3">
                  <span>~{Math.max(1, Math.round(t.duration_sec / 60))} dk</span>
                  <span className="grid h-6 w-6 place-items-center rounded-full bg-[rgba(28,61,90,0.08)] text-[var(--navy)] transition-all group-hover:bg-[var(--navy)] group-hover:text-[#f6f1e6]">
                    ▶
                  </span>
                </span>
              </div>
            </Link>
          ))}
          <PracticeMoreCard href={archiveHref} count={tests.length} label={title} />
        </div>
      )}
    </section>
  );
}
