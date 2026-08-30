"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type TestSummary } from "@/lib/api";
import { AcademicPracticeSession } from "@/components/AcademicPracticeSession";
import { PracticeMoreCard } from "@/components/PracticeMoreCard";
import { PracticeSolvedBadge } from "@/components/PracticeSolvedBadge";
import { useCompletedPracticeIds } from "@/lib/practiceProgress";

type Group = { kind: string; label: string; note: string };

export function SectionCatalog({ groups, inline = false }: { groups: Group[]; inline?: boolean }) {
  const [tests, setTests] = useState<TestSummary[]>([]);
  const [selectedTestId, setSelectedTestId] = useState("");
  const [error, setError] = useState("");
  const completedIds = useCompletedPracticeIds();
  const kindKey = groups.map((group) => group.kind).join(",");

  useEffect(() => {
    Promise.all(kindKey.split(",").filter(Boolean).map((kind) => api<TestSummary[]>(`/api/tests?kind=${kind}`)))
      .then((sets) => setTests(sets.flat()))
      .catch((e) => setError(e instanceof Error ? e.message : "İçerikler alınamadı"));
  }, [kindKey]);

  if (error) return <p className="rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">{error}</p>;
  if (inline && selectedTestId) return <AcademicPracticeSession testId={selectedTestId} onBack={() => setSelectedTestId("")} />;

  return (
    <div className="space-y-8">
      {groups.map((group) => {
        const items = tests.filter((t) => t.kind === group.kind);
        const completedCount = items.filter((test) => completedIds.has(test.id)).length;
        return (
          <section key={group.kind} className="space-y-3">
            <div className="flex flex-wrap items-end justify-between gap-2">
              <div>
                <h2 className="font-serif text-2xl text-[var(--navy)]">{group.label}</h2>
                <p className="prose-quiet mt-1 text-sm">{group.note}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="badge">{items.length} çalışma</span>
                {completedCount > 0 ? <span className="badge badge-green">✓ {completedCount} çözüldü</span> : null}
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {items.slice(0, 2).map((test, index) => {
                const content = <>
                  <span>
                    <span className="eyebrow">{group.label} · {String(index + 1).padStart(2, "0")}</span>
                    <span className="mt-1 block font-medium text-[var(--navy)]">{test.title}</span>
                    <span className="mt-2 block">
                      {completedIds.has(test.id) ? <PracticeSolvedBadge /> : <span className="text-xs text-[var(--ink-2)]">B1+ · özgün çalışma</span>}
                    </span>
                  </span>
                  <span className="text-xl text-[var(--gold)]">→</span>
                </>;
                return inline
                  ? <button key={test.id} type="button" onClick={() => setSelectedTestId(test.id)} className="card card-lift flex w-full items-center justify-between gap-4 p-5 text-left">{content}</button>
                  : <Link key={test.id} href={`/practice/${test.id}`} className="card card-lift flex items-center justify-between gap-4 p-5">{content}</Link>;
              })}
              {items.length > 2 ? <PracticeMoreCard href={`/practice-library/${group.kind}`} count={items.length} label={group.label} completedCount={completedCount} /> : null}
            </div>
          </section>
        );
      })}
    </div>
  );
}
