"use client";

import { useEffect, useRef, useState } from "react";
import { SPEEDS, speedLabel } from "@/lib/settings";

type Props = {
  src: string;
  active: boolean;
  /** true once the visitor has pressed play at least once anywhere in the feed,
   * which is what lets later cards start on their own. */
  unlocked: boolean;
  onUnlock: () => void;
  onFinished: () => void;
  fallbackSeconds: number;
  /** site-wide playback rate, shared by every card */
  speed: number;
  onSpeedChange: (value: number) => void;
};

const BARS = 34;

/** Fixed pseudo-waveform: deterministic so the bars do not jump on re-render. */
const HEIGHTS = Array.from({ length: BARS }, (_, i) => {
  const a = Math.sin(i * 1.7) * 0.5 + 0.5;
  const b = Math.sin(i * 0.6 + 1.2) * 0.5 + 0.5;
  return 0.28 + (a * 0.45 + b * 0.55) * 0.72;
});

function fmt(sec: number) {
  if (!Number.isFinite(sec) || sec < 0) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function ClipPlayer({
  src,
  active,
  unlocked,
  onUnlock,
  onFinished,
  fallbackSeconds,
  speed,
  onSpeedChange,
}: Props) {
  const ref = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [plays, setPlays] = useState(0);
  const [failed, setFailed] = useState(false);

  // Leaving a card always stops its sound; arriving on one starts it when the
  // browser already trusts us with audio.
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (!active) {
      el.pause();
      // the seek fires timeupdate, which resets the displayed position
      el.currentTime = 0;
      return;
    }
    if (unlocked && plays === 0) {
      void el.play().catch(() => {
        /* autoplay refused: the play button is still there */
      });
    }
    // plays is deliberately not a dependency: replays must stay manual.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active, unlocked]);

  // A rate set before the source loads is lost, so it is reapplied on every
  // change and again once the browser has the metadata.
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.preservesPitch = true;
    el.playbackRate = speed;
  }, [speed]);

  function toggle() {
    const el = ref.current;
    if (!el) return;
    if (el.paused) {
      onUnlock();
      void el.play().catch(() => setFailed(true));
    } else {
      el.pause();
    }
  }

  const total = duration || fallbackSeconds || 0;
  const progress = total ? Math.min(1, time / total) : 0;
  const filled = Math.round(progress * BARS);

  return (
    <div className="rounded-2xl border border-[var(--line)] bg-[rgba(28,61,90,0.03)] p-3.5">
      <div className="flex items-center gap-3.5">
        <button
          type="button"
          onClick={toggle}
          className="play-btn"
          aria-label={playing ? "Duraklat" : "Kaydı çal"}
        >
          {playing ? (
            <svg width="17" height="17" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <rect x="3" y="2" width="3.5" height="12" rx="1" />
              <rect x="9.5" y="2" width="3.5" height="12" rx="1" />
            </svg>
          ) : (
            <svg width="17" height="17" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path d="M4 2.5v11l9.5-5.5z" />
            </svg>
          )}
        </button>

        <div className="min-w-0 flex-1">
          <div className={`wave ${playing ? "on" : ""}`} aria-hidden="true">
            {HEIGHTS.map((h, i) => (
              <i
                key={i}
                style={{
                  height: `${Math.round(h * 100)}%`,
                  animationDelay: `${(i % 7) * 0.09}s`,
                  background: i < filled ? "var(--navy)" : undefined,
                  opacity: i < filled ? 1 : 0.55,
                }}
              />
            ))}
          </div>
          <div className="mt-1.5 flex items-center justify-between text-[0.7rem] text-[var(--ink-2)]">
            <span>
              {fmt(time)} / {fmt(total)}
            </span>
            <span>
              {failed
                ? "ses açılamadı"
                : plays === 0
                  ? "önce dinle"
                  : plays === 1
                    ? "1 kez dinledin"
                    : `${plays} kez dinledin`}
            </span>
          </div>
        </div>
      </div>

      <input
        type="range"
        min={0}
        max={total || 0}
        step={0.1}
        value={Math.min(time, total || 0)}
        onChange={(e) => {
          const el = ref.current;
          if (!el) return;
          el.currentTime = Number(e.target.value);
          setTime(Number(e.target.value));
        }}
        className="seek mt-1.5"
        aria-label="Kayıtta ilerle"
      />

      {/* Site-wide, not per card: set once and every clip follows. */}
      <div className="mt-2 border-t border-[var(--line-soft)] pt-2">
        <div className="flex items-center gap-2">
          <span className="flex-none text-[0.66rem] font-semibold uppercase tracking-[0.12em] text-[var(--ink-3)]">
            hız
          </span>
          <div className="flex flex-1 gap-1" role="group" aria-label="Kayıt hızı">
            {SPEEDS.map((value) => {
              const on = value === speed;
              return (
                <button
                  key={value}
                  type="button"
                  aria-pressed={on}
                  onClick={() => onSpeedChange(value)}
                  className={`speed-btn min-w-0 flex-1 rounded-lg border py-1 text-[0.68rem] font-semibold tabular-nums transition ${
                    on
                      ? "border-[var(--navy)] bg-[var(--navy)] text-[#f6f1e6]"
                      : "border-[var(--line)] bg-white text-[var(--ink-2)] hover:border-[var(--navy)] hover:text-[var(--navy)]"
                  }`}
                >
                  {speedLabel(value)}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <audio
        ref={ref}
        src={src}
        preload="none"
        onPlay={() => {
          setPlaying(true);
          const el = ref.current;
          if (el && el.currentTime < 0.4) setPlays((p) => p + 1);
        }}
        onPause={() => setPlaying(false)}
        onEnded={() => {
          setPlaying(false);
          onFinished();
        }}
        onTimeUpdate={() => setTime(ref.current?.currentTime ?? 0)}
        onLoadedMetadata={() => {
          const el = ref.current;
          if (!el) return;
          el.playbackRate = speed;
          setDuration(el.duration ?? 0);
        }}
        onError={() => setFailed(true)}
      />
    </div>
  );
}
