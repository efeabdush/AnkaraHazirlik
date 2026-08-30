"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Level, type Pack } from "@/lib/api";
import { modeTitle, type ModeId } from "@/lib/modes";
import { levelBlurb, levelClass, levelColor, levelNote } from "@/lib/levels";
import { packProgress } from "@/lib/session";

type Progress = Record<string, { answered: number; correct: number }>;

export function PackList({ mode, level }: { mode: ModeId; level: Level }) {
  const [packs, setPacks] = useState<Pack[] | null>(null);
  const [progress, setProgress] = useState<Progress>({});
  const [error, setError] = useState("");

  useEffect(() => {
    api<{ packs: Pack[] }>(`/api/akis/packs?kind=${mode}&level=${encodeURIComponent(level)}`)
      .then((data) => {
        setPacks(data.packs);
        const seen: Progress = {};
        for (const p of data.packs) seen[p.id] = packProgress(`${mode}:${p.id}`);
        setProgress(seen);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Paketler alınamadı"));
  }, [mode, level]);

  return (
    <div className="mx-auto w-full max-w-3xl">
      <nav className="text-xs text-[var(--ink-2)]">
        <Link href={`/akis/${mode}/seviye`} className="tap-link hover:text-[var(--navy)]">
          ← Seviyeler
        </Link>
      </nav>

      <header className="mt-4 flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-2">
          <span className={levelClass(level)}>
            {level}
            <small>{levelNote[level]}</small>
          </span>
          <h1 className="font-serif text-3xl tracking-tight text-[var(--navy)] sm:text-4xl">
            {modeTitle(mode)} · {level}
          </h1>
          <p className="prose-quiet max-w-xl text-sm">{levelBlurb[level]}</p>
        </div>
      </header>

      {error ? (
        <p className="mt-6 rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">
          {error}
        </p>
      ) : null}

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        {packs === null && !error
          ? [0, 1].map((i) => <div key={i} className="card pulse-soft h-28" />)
          : (packs ?? []).map((p) => {
              const done = progress[p.id]?.answered ?? 0;
              const right = progress[p.id]?.correct ?? 0;
              const pct = p.size ? Math.round((done / p.size) * 100) : 0;
              return (
                <Link
                  key={p.id}
                  href={`/akis/${mode}?pack=${encodeURIComponent(p.id)}`}
                  className="card card-lift block p-5"
                >
                  <div className="flex items-baseline justify-between gap-3">
                    <span className="font-serif text-xl text-[var(--navy)]">{p.title}</span>
                    <span className="text-xs text-[var(--ink-2)]">
                      {p.size} soru
                      {p.full ? "" : " · eksik"}
                    </span>
                  </div>

                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-[var(--line-soft)]">
                    <div
                      className="h-full rounded-full transition-[width]"
                      style={{ width: `${pct}%`, background: levelColor(level) }}
                    />
                  </div>

                  <p className="mt-2 text-xs text-[var(--ink-2)]">
                    {done ? `${done}/${p.size} cevaplandı · ${right} doğru` : "Henüz başlamadın"}
                  </p>
                </Link>
              );
            })}
      </div>

      {packs !== null && packs.length === 0 ? (
        <div className="card mt-6 border-dashed p-6">
          <p className="font-serif text-xl text-[var(--navy)]">Bu seviyede henüz kart yok</p>
          <p className="prose-quiet mt-2 text-sm">
            Panelden bu seviyeye kart üretince paketler kendiliğinden oluşur.
          </p>
          <Link href="/akis" className="btn btn-outline mt-4">Akış biçimleri</Link>
        </div>
      ) : null}

      {packs !== null && packs.some((p) => !p.full) ? (
        <p className="mt-6 text-xs leading-relaxed text-[var(--ink-3)]">
          &ldquo;eksik&rdquo; işaretli paket, tam {packs[0]?.pack_size} karta henüz ulaşmamış demek.
          Yeni kart üretildikçe o paket dolar, dolduktan sonra bir sonraki paket açılır.
        </p>
      ) : null}
    </div>
  );
}
