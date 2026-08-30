"use client";

import { useState } from "react";
import Link from "next/link";
import { ClipPlayer } from "@/components/ClipPlayer";
import { akisAudioUrl, type AnswerResult, type ReelCard as Card } from "@/lib/api";
import { levelClass, levelColor, levelNote } from "@/lib/levels";
import { Markdown } from "@/lib/markdown";

type Props = {
  card: Card;
  index: number;
  total: number;
  active: boolean;
  result: AnswerResult | null;
  busy: boolean;
  unlocked: boolean;
  onUnlock: () => void;
  onAnswer: (choice: string) => void;
  onNext: () => void;
  /** carried into the chat so "geri dön" lands back in the same pack */
  pack?: string;
  mode: string;
  speed: number;
  onSpeedChange: (value: number) => void;
};

/** The reading formats show their text where the player would be. A gap is
 * marked with ___ in the data and drawn as a real blank here. */
function CardText({ body }: { body: string }) {
  const parts = body.split("___");
  return (
    <div className="rounded-2xl border border-[var(--line)] bg-[rgba(28,61,90,0.03)] p-4 text-[1.02rem] leading-8 text-[var(--ink)]">
      {parts.map((part, i) => (
        <span key={i}>
          {part}
          {i < parts.length - 1 ? (
            <span className="mx-1 inline-block h-[1.15em] w-16 translate-y-[0.2em] rounded border-b-2 border-[var(--gold)] bg-[rgba(176,139,63,0.12)] align-baseline" />
          ) : null}
        </span>
      ))}
    </div>
  );
}

export function ReelCard({
  card,
  index,
  total,
  active,
  result,
  busy,
  unlocked,
  onUnlock,
  onAnswer,
  onNext,
  pack,
  mode,
  speed,
  onSpeedChange,
}: Props) {
  const [listened, setListened] = useState(false);
  const [showScript, setShowScript] = useState(false);
  const letters = Object.keys(card.options).sort();
  // Reading cards have nothing to wait for: the text is already on screen.
  // Only the listening format hides its options until the clip has played.
  const open = card.kind !== "sorular" || listened || Boolean(result);
  // reading formats keep their text on screen, so there is nothing to reveal
  const hasScript = Boolean(result?.script?.length);

  function optionClass(letter: string) {
    if (!result) return "opt";
    if (letter === result.answer) return "opt opt-correct";
    if (letter === result.chosen) return "opt opt-wrong";
    return "opt opt-dim";
  }

  return (
    <article className="card w-full p-4 sm:p-6">
      <header className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className={`${levelClass(card.level)} self-start`}>
            {card.level}
            <small>{levelNote[card.level] ?? ""}</small>
          </span>
          {card.seconds ? (
            <span className="text-[0.7rem] text-[var(--ink-3)]">~{card.seconds} sn</span>
          ) : null}
        </div>
        <span className="text-[0.72rem] font-semibold text-[var(--ink-3)]">
          {index + 1} / {total}
        </span>
      </header>

      <div className="mt-3 flex items-stretch gap-3">
        <span className="lv-rail" style={{ background: levelColor(card.level) }} aria-hidden="true" />
        <div className="min-w-0">
          <h2 className="font-serif text-xl leading-tight text-[var(--navy)] sm:text-2xl">{card.title}</h2>
          {card.topic ? <p className="mt-0.5 text-xs text-[var(--ink-3)] capitalize">{card.topic}</p> : null}
        </div>
      </div>

      <div className="mt-4">
        {card.kind === "sorular" ? (
          <ClipPlayer
            src={akisAudioUrl(card.id)}
            active={active}
            unlocked={unlocked}
            onUnlock={onUnlock}
            onFinished={() => setListened(true)}
            fallbackSeconds={card.seconds}
            speed={speed}
            onSpeedChange={onSpeedChange}
          />
        ) : (
          <CardText body={card.body} />
        )}
      </div>

      {!open ? (
        <div className="mt-5 rounded-2xl border border-dashed border-[var(--line)] p-5 text-center">
          <p className="font-serif text-lg text-[var(--navy)]">Önce kaydı dinle</p>
          <p className="prose-quiet mx-auto mt-1 max-w-xs text-sm">
            Kayıt bitince soru ve şıklar burada açılır.
          </p>
          <button type="button" className="btn btn-quiet mt-2 text-xs" onClick={() => setListened(true)}>
            Şıkları şimdi aç
          </button>
        </div>
      ) : (
        <div className="mt-5 rise">
          <p className="font-medium leading-relaxed text-[var(--navy)]">{card.stem}</p>

          <div className="mt-3 grid gap-2">
            {letters.map((letter) => (
              <button
                key={letter}
                type="button"
                disabled={Boolean(result) || busy}
                onClick={() => onAnswer(letter)}
                className={optionClass(letter)}
              >
                <span className="opt-letter">{letter}</span>
                <span className="text-sm leading-relaxed">{card.options[letter]}</span>
                {result && letter === result.answer ? (
                  <span className="badge badge-green ml-auto flex-none">doğru</span>
                ) : null}
                {result && letter === result.chosen && letter !== result.answer ? (
                  <span className="badge badge-warn ml-auto flex-none">senin</span>
                ) : null}
              </button>
            ))}
          </div>
        </div>
      )}

      {result ? (
        <div className="mt-4 rise">
          <div
            className={`rounded-2xl border p-4 ${
              result.correct
                ? "border-[rgba(47,107,81,0.4)] bg-[rgba(47,107,81,0.07)]"
                : "border-[rgba(176,81,44,0.4)] bg-[rgba(176,81,44,0.06)]"
            }`}
          >
            <p
              className={`font-serif text-lg ${
                result.correct ? "text-[var(--green)]" : "text-[var(--terracotta)]"
              }`}
            >
              {result.correct ? "Doğru" : `Yanlış — doğrusu ${result.answer}`}
            </p>
            <Markdown className="mt-1.5 text-sm leading-relaxed text-[var(--ink)]" text={result.explain_tr} />
            {result.key_line ? (
              <p className="mt-2.5 border-l-2 border-[var(--gold)] pl-3 text-sm italic leading-relaxed text-[var(--ink-2)]">
                “{result.key_line}”
              </p>
            ) : null}
          </div>

          {/* only the listening format has a transcript to open */}
          {hasScript && showScript ? (
            <div className="mt-3 space-y-1.5 rounded-2xl border border-[var(--line)] bg-[rgba(28,61,90,0.03)] p-4 text-sm leading-7">
              {result.script.map((line, i) => (
                <p key={i}>
                  <span className="mr-2 font-medium capitalize text-[var(--navy)]">{line.speaker}:</span>
                  {line.text}
                </p>
              ))}
            </div>
          ) : null}

          {/* stacked on a phone so nothing wraps, one row from tablet up */}
          <div className="card-actions mt-3 flex flex-col gap-2 pt-3 sm:flex-row sm:flex-wrap sm:items-center">
            <Link
              href={
                `/akis/ogren?reel=${encodeURIComponent(card.id)}&choice=${encodeURIComponent(result.chosen)}` +
                `&mode=${encodeURIComponent(mode)}` +
                (pack ? `&pack=${encodeURIComponent(pack)}` : "")
              }
              className="btn btn-primary text-sm"
            >
              Soruyu öğren
            </Link>
            <div className="flex gap-2">
              <button type="button" className="btn btn-outline flex-1 text-sm sm:flex-none" onClick={onNext}>
                Sonraki kart ↓
              </button>
              {hasScript ? (
                <button
                  type="button"
                  className="btn btn-quiet flex-none text-sm"
                  onClick={() => setShowScript((v) => !v)}
                >
                  {showScript ? "Kaydı gizle" : "Kaydı oku"}
                </button>
              ) : null}
            </div>
          </div>
        </div>
      ) : null}
    </article>
  );
}
