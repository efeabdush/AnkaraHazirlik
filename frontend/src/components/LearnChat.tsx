"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { ClipPlayer } from "@/components/ClipPlayer";
import { api, akisAudioUrl, type AnswerResult, type ChatStatus, type ReelCard as Card } from "@/lib/api";
import { levelClass, levelNote } from "@/lib/levels";
import { Markdown } from "@/lib/markdown";
import { type ModeId } from "@/lib/modes";
import { DEFAULT_SPEED, loadSpeed, saveSpeed } from "@/lib/settings";
import {
  MIX_SCOPE,
  clearThread,
  loadFeedState,
  loadThread,
  saveThread,
  type ChatItem,
} from "@/lib/session";

/** Same blank rendering as the feed, so the question looks identical here. */
function ChatCardText({ body }: { body: string }) {
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

const PRESETS = [
  "Bu cevap neden doğru?",
  "Benim seçtiğim neden yanlış?",
  "Kayıttaki cümleyi açıklar mısın?",
  "Buradaki dil bilgisi kuralı ne?",
];

type Props = { reelId: string; choice: string; pack?: string; mode: ModeId };

export function LearnChat({ reelId, choice, pack, mode }: Props) {
  // The card travels back in the URL, so returning always lands on the exact
  // question that was asked about, whatever the feed did in the meantime.
  const backHref =
    (pack ? `/akis/${mode}?pack=${encodeURIComponent(pack)}&` : `/akis/${mode}?`) +
    `card=${encodeURIComponent(reelId)}`;
  const endRef = useRef<HTMLDivElement>(null);
  const seenCountRef = useRef(-1);
  const [card, setCard] = useState<Card | null>(null);
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [items, setItems] = useState<ChatItem[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ready, setReady] = useState<boolean | null>(null);
  const [showScript, setShowScript] = useState(false);
  const [speed, setSpeed] = useState(DEFAULT_SPEED);

  const changeSpeed = useCallback((value: number) => {
    setSpeed(value);
    saveSpeed(value);
  }, []);

  useEffect(() => {
    api<Card>(`/api/akis/reels/${reelId}`)
      .then((data) => {
        setCard(data);
        setSpeed(loadSpeed());
        // the answer lives in the scope the learner came from: a pack, or the mix
        setResult(loadFeedState(`${mode}:${pack || MIX_SCOPE}`).results[reelId] ?? null);
        setItems(loadThread(reelId));
      })
      .catch((e) => {
        setItems(loadThread(reelId));
        setError(e instanceof Error ? e.message : "Kart bulunamadı");
      });
    api<ChatStatus>("/api/akis/chat/status")
      .then((s) => setReady(s.ready))
      .catch(() => setReady(false));
  }, [reelId, pack, mode]);

  // Jump to the newest message only when one actually arrives. On entry the
  // view stays at the top, on the question - that is the reason it is there.
  useEffect(() => {
    const count = items.length;
    if (seenCountRef.current < 0) {
      seenCountRef.current = count;
      return;
    }
    if (count === seenCountRef.current && !busy) return;
    seenCountRef.current = count;
    const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    endRef.current?.scrollIntoView({ block: "end", behavior: still ? "auto" : "smooth" });
  }, [items, busy]);

  async function send(text?: string) {
    const content = (text ?? input).trim();
    if (!content || busy) return;
    const next: ChatItem[] = [...items, { role: "user", content }];
    setItems(next);
    saveThread(reelId, next);
    setInput("");
    setBusy(true);
    setError("");
    try {
      const payload = next.slice(-24).map(({ role, content: c }) => ({ role, content: c }));
      const data = await api<{ reply: string }>("/api/akis/chat", {
        method: "POST",
        body: JSON.stringify({ reel_id: reelId, choice, messages: payload }),
      });
      const withReply: ChatItem[] = [...next, { role: "assistant", content: data.reply }];
      setItems(withReply);
      saveThread(reelId, withReply);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Yanıt alınamadı");
    } finally {
      setBusy(false);
    }
  }

  const messageCount = items.length;

  return (
    <div className="flex h-[100dvh] flex-col bg-[var(--bg)]">
      {/* thin bar: the way out and where you are */}
      <header className="flex-none border-b border-[var(--line)] bg-[rgba(253,251,247,0.92)] backdrop-blur">
        <div className="mx-auto flex w-full max-w-2xl items-center justify-between gap-3 px-3 pt-[max(0.6rem,env(safe-area-inset-top))] pb-2.5 sm:px-4">
          <Link href={backHref} className="btn btn-outline text-sm">
            ← Soru çözmeye dön
          </Link>
          {card ? (
            <span className={levelClass(card.level)}>
              {card.level}
              <small>{levelNote[card.level] ?? ""}</small>
            </span>
          ) : null}
        </div>
      </header>

      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto w-full max-w-2xl space-y-2.5 px-3 py-4 sm:px-4">
          {/* The whole question sits above the conversation: the clip can be
              replayed and the options re-read without leaving the chat. */}
          {card ? (
            <section className="card p-4 sm:p-5">
              <p className="eyebrow">Sorduğun soru</p>
              <h1 className="mt-1 font-serif text-xl leading-tight text-[var(--navy)]">{card.title}</h1>

              <div className="mt-3">
                {card.kind === "sorular" ? (
                  <ClipPlayer
                    src={akisAudioUrl(card.id)}
                    active
                    unlocked={false}
                    onUnlock={() => {}}
                    onFinished={() => {}}
                    fallbackSeconds={card.seconds}
                    speed={speed}
                    onSpeedChange={changeSpeed}
                  />
                ) : (
                  <ChatCardText body={card.body} />
                )}
              </div>

              <p className="mt-4 font-medium leading-relaxed text-[var(--navy)]">{card.stem}</p>

              <div className="mt-2.5 grid gap-1.5">
                {Object.keys(card.options)
                  .sort()
                  .map((letter) => {
                    const isKey = result?.answer === letter;
                    const isPick = result?.chosen === letter;
                    const cls = !result
                      ? "opt"
                      : isKey
                        ? "opt opt-correct"
                        : isPick
                          ? "opt opt-wrong"
                          : "opt opt-dim";
                    return (
                      <div key={letter} className={`${cls} cursor-default`}>
                        <span className="opt-letter">{letter}</span>
                        <span className="text-sm leading-relaxed">{card.options[letter]}</span>
                        {isKey ? <span className="badge badge-green ml-auto flex-none">doğru</span> : null}
                        {isPick && !isKey ? (
                          <span className="badge badge-warn ml-auto flex-none">senin</span>
                        ) : null}
                      </div>
                    );
                  })}
              </div>

              {result ? (
                <div
                  className={`mt-3 rounded-xl border p-3 ${
                    result.correct
                      ? "border-[rgba(47,107,81,0.4)] bg-[rgba(47,107,81,0.07)]"
                      : "border-[rgba(176,81,44,0.4)] bg-[rgba(176,81,44,0.06)]"
                  }`}
                >
                  <p
                    className={`text-sm font-semibold ${
                      result.correct ? "text-[var(--green)]" : "text-[var(--terracotta)]"
                    }`}
                  >
                    {result.correct ? "Doğru cevapladın" : `Yanlış — doğrusu ${result.answer}`}
                  </p>
                  <Markdown className="mt-1 text-sm leading-relaxed" text={result.explain_tr} />
                  {result.key_line ? (
                    <p className="mt-2 border-l-2 border-[var(--gold)] pl-3 text-sm italic leading-relaxed text-[var(--ink-2)]">
                      “{result.key_line}”
                    </p>
                  ) : null}
                </div>
              ) : (
                <p className="mt-3 text-xs text-[var(--ink-3)]">Bu soruyu henüz cevaplamadın.</p>
              )}

              {result?.script?.length ? (
                <>
                  <button
                    type="button"
                    className="btn btn-quiet mt-2 text-sm"
                    onClick={() => setShowScript((v) => !v)}
                  >
                    {showScript ? "Kaydı gizle" : "Kaydı oku"}
                  </button>
                  {showScript ? (
                    <div className="mt-1 space-y-1.5 rounded-xl border border-[var(--line)] bg-[rgba(28,61,90,0.03)] p-3 text-sm leading-7">
                      {result.script.map((line, i) => (
                        <p key={i}>
                          <span className="mr-2 font-medium capitalize text-[var(--navy)]">
                            {line.speaker}:
                          </span>
                          {line.text}
                        </p>
                      ))}
                    </div>
                  ) : null}
                </>
              ) : null}
            </section>
          ) : (
            <div className="card pulse-soft h-64" />
          )}

          {ready === false ? (
            <div className="card p-4 text-sm leading-relaxed text-[var(--ink-2)]">
              Sohbet şu an kapalı: site sahibi panelden bir API anahtarı ve model seçmemiş. Kartları
              çözmeye devam edebilirsin.
            </div>
          ) : null}

          {messageCount === 0 ? (
            <div className="card p-5">
              <p className="font-serif text-xl text-[var(--navy)]">Ne takıldı?</p>
              <p className="prose-quiet mt-1.5 text-sm">
                Kaydı ve soruyu görüyorum. İstediğini sor. Bu sohbet yalnızca bu soruya ait: başka
                bir soruya geçtiğinde orada tertemiz bir sayfa açılır, buraya dönersen konuştuğumuz
                yerden devam ederiz.
              </p>
            </div>
          ) : null}

          {items.map((item, i) => (
            <div key={i} className={`bubble ${item.role === "user" ? "bubble-you" : "bubble-ai"}`}>
              {item.role === "user" ? (
                <span className="bubble-plain block">{item.content}</span>
              ) : (
                <Markdown text={item.content} />
              )}
            </div>
          ))}

          {busy ? (
            <div className="bubble bubble-ai">
              <span className="typing">
                <i />
                <i />
                <i />
              </span>
            </div>
          ) : null}

          {error ? (
            <p className="rounded-xl border border-[var(--terracotta)] bg-[rgba(176,81,44,0.06)] p-3 text-sm text-[var(--terracotta)]">
              {error}
            </p>
          ) : null}

          <div ref={endRef} />
        </div>
      </div>

      <footer className="flex-none border-t border-[var(--line)] bg-[rgba(253,251,247,0.92)] backdrop-blur">
        <div className="mx-auto w-full max-w-2xl px-3 pt-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] sm:px-4">
          {/* one swipeable row on a phone, wrapped chips on wider screens */}
          <div className="-mx-3 flex gap-1.5 overflow-x-auto px-3 pb-1 sm:mx-0 sm:flex-wrap sm:overflow-visible sm:px-0">
            {PRESETS.map((p) => (
              <button
                key={p}
                type="button"
                disabled={busy || ready === false}
                className="badge shrink-0 whitespace-nowrap hover:border-[var(--navy)] hover:text-[var(--navy)] disabled:opacity-50"
                onClick={() => void send(p)}
              >
                {p}
              </button>
            ))}
          </div>

          <form
            className="mt-2.5 flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              void send();
            }}
          >
            <input
              className="input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Sorunu yaz…"
              disabled={ready === false}
            />
            <button type="submit" className="btn btn-primary" disabled={busy || !input.trim()}>
              Gönder
            </button>
          </form>

          <div className="mt-1.5 flex items-center justify-between text-[0.7rem] text-[var(--ink-3)]">
            <span>{messageCount ? `${messageCount} mesaj` : "sohbet boş"}</span>
            {messageCount ? (
              <button
                type="button"
                className="tap-link hover:text-[var(--navy)]"
                onClick={() => {
                  clearThread(reelId);
                  setItems([]);
                }}
              >
                sohbeti temizle
              </button>
            ) : null}
          </div>
        </div>
      </footer>
    </div>
  );
}
