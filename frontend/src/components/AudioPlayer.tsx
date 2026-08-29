"use client";

import { useEffect, useRef, useState } from "react";

type Props = {
  src: string;
  examMode: boolean;
  maxPlays?: number;
  onPlaysChange?: (n: number) => void;
};

function fmt(sec: number) {
  if (!Number.isFinite(sec)) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function AudioPlayer({ src, examMode, maxPlays = 2, onPlaysChange }: Props) {
  const ref = useRef<HTMLAudioElement>(null);
  const [plays, setPlays] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const exhausted = examMode && plays >= maxPlays;

  useEffect(() => {
    onPlaysChange?.(plays);
    // parent only needs the count
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [plays]);

  function toggle() {
    const el = ref.current;
    if (!el) return;
    if (el.paused) {
      if (exhausted && el.currentTime === 0) return;
      void el.play();
    } else {
      el.pause();
    }
  }

  function seek(value: number) {
    const el = ref.current;
    if (!el || examMode) return;
    el.currentTime = value;
    setTime(value);
  }

  const pct = duration ? (time / duration) * 100 : 0;

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={toggle}
            disabled={exhausted && !playing}
            aria-label={playing ? "Duraklat" : "Oynat"}
            className="grid h-12 w-12 place-items-center rounded-full bg-[var(--navy)] text-[#f6f1e6] shadow-sm transition hover:bg-[var(--navy-deep)] disabled:opacity-40"
          >
            {playing ? (
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="3" y="2" width="3.5" height="12" rx="1" />
                <rect x="9.5" y="2" width="3.5" height="12" rx="1" />
              </svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M4 2.5v11l9.5-5.5z" />
              </svg>
            )}
          </button>
          <div>
            <p className="text-sm font-medium text-[var(--navy)]">
              {examMode ? "Sınav kaydı" : "Pratik dinleme"}
            </p>
            <p className="text-xs text-[var(--ink-2)]">
              {fmt(time)} / {fmt(duration)}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {examMode ? (
            <div className="flex items-center gap-1.5" title={`${plays}/${maxPlays} dinleme`}>
              {Array.from({ length: maxPlays }).map((_, i) => (
                <span
                  key={i}
                  className={`h-2 w-2 rounded-full ${
                    i < plays ? "bg-[var(--navy)]" : "bg-[var(--line)]"
                  }`}
                />
              ))}
              <span className="ml-1 text-xs text-[var(--ink-2)]">
                {plays}/{maxPlays}
              </span>
            </div>
          ) : (
            <span className="badge">sınırsız</span>
          )}
        </div>
      </div>

      <div className="mt-4">
        <div className="relative h-1.5 overflow-hidden rounded-full bg-[var(--line-soft)]">
          <div className="h-full rounded-full bg-[var(--navy)] transition-[width] duration-200" style={{ width: `${pct}%` }} />
        </div>
        {!examMode ? (
          <input
            type="range"
            min={0}
            max={duration || 0}
            value={time}
            onChange={(e) => seek(Number(e.target.value))}
            className="mt-2 w-full accent-[var(--navy)]"
            aria-label="Kayıtta ilerle"
          />
        ) : null}
      </div>

      <p className="mt-3 text-xs leading-relaxed text-[var(--ink-2)]">
        {exhausted
          ? "İki dinleme hakkın doldu. Gerçek sınavda da kayıt iki kez çalınır."
          : examMode
            ? "Sınav modunda ileri sarma kapalı, kayıt iki kez çalınabilir."
            : "Pratik modunda ileri sarabilir ve tekrar dinleyebilirsin."}
      </p>

      <audio
        ref={ref}
        src={src}
        preload="metadata"
        className="hidden"
        onPlay={() => {
          setPlaying(true);
          const el = ref.current;
          if (el && el.currentTime < 0.4) setPlays((p) => p + 1);
        }}
        onPause={() => setPlaying(false)}
        onEnded={() => setPlaying(false)}
        onTimeUpdate={() => setTime(ref.current?.currentTime ?? 0)}
        onLoadedMetadata={() => setDuration(ref.current?.duration ?? 0)}
      />
    </div>
  );
}
