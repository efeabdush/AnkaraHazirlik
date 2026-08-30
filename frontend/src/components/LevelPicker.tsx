"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type LevelSummary } from "@/lib/api";
import { modeTitle, type ModeId } from "@/lib/modes";
import { levelBlurb, levelClass, levelColor, levelNote, levelSlug } from "@/lib/levels";

export function LevelPicker({ mode }: { mode: ModeId }) {
  const [levels, setLevels] = useState<LevelSummary[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api<LevelSummary[]>(`/api/akis/levels?kind=${mode}`)
      .then(setLevels)
      .catch((e) => setError(e instanceof Error ? e.message : "Seviyeler alınamadı"));
  }, [mode]);

  return (
    <div className="mx-auto w-full max-w-3xl">
      <nav className="text-xs text-[var(--ink-2)]">
        <Link href="/akis" className="tap-link hover:text-[var(--navy)]">
          ← Akış biçimleri
        </Link>
      </nav>

      <header className="mt-4 space-y-2">
        <p className="eyebrow">{modeTitle(mode)} · seviyene göre ilerle</p>
        <h1 className="font-serif text-3xl tracking-tight text-[var(--navy)] sm:text-4xl">
          Hangi seviyeden başlamak istersin?
        </h1>
        <p className="prose-quiet max-w-xl text-sm">
          Her seviyenin kartları numaralı paketlere bölünür. Bir paketi bitirip diğerine geçersin;
          nerede kaldığın hatırlanır.
        </p>
      </header>

      {error ? (
        <p className="mt-6 rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">
          {error}
        </p>
      ) : null}

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        {levels === null && !error
          ? [0, 1, 2, 3].map((i) => <div key={i} className="card pulse-soft h-36" />)
          : (levels ?? []).map((item) => {
              const empty = item.cards === 0;
              const body = (
                <>
                  <div className="flex items-start justify-between gap-3">
                    <span className={levelClass(item.level)}>
                      {item.level}
                      <small>{levelNote[item.level]}</small>
                    </span>
                    <span className="text-xs text-[var(--ink-2)]">
                      {empty ? "kart yok" : `${item.packs} paket · ${item.cards} kart`}
                    </span>
                  </div>
                  <p className="prose-quiet mt-3 text-sm">{levelBlurb[item.level]}</p>
                  <p className="mt-3 text-sm font-medium" style={{ color: levelColor(item.level) }}>
                    {empty ? "Henüz içerik eklenmedi" : "Paketleri gör →"}
                  </p>
                </>
              );

              return empty ? (
                <div key={item.level} className="card p-5 opacity-60">
                  {body}
                </div>
              ) : (
                <Link
                  key={item.level}
                  href={`/akis/${mode}/seviye/${levelSlug(item.level)}`}
                  className="card card-lift block p-5"
                >
                  {body}
                </Link>
              );
            })}
      </div>

      <p className="mt-8 text-sm text-[var(--ink-2)]">
        Seviye seçmeden çalışmak istersen{" "}
        <Link href={`/akis/${mode}`} className="tap-link underline underline-offset-4 hover:text-[var(--navy)]">
          karışık akışa
        </Link>{" "}
        girebilirsin.
      </p>
    </div>
  );
}
