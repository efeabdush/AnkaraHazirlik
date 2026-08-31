"use client";

import { useCallback, useEffect, useMemo, useRef, useState, type TouchEvent } from "react";
import Link from "next/link";
import { ReelCard } from "@/components/ReelCard";
import { api, type AnswerResult, type Level, type Pack, type ReelCard as Card } from "@/lib/api";
import {
  AKIS_SWIPE_DURATION_MS,
  AKIS_SWIPE_LOCK_MS,
  akisSwipeDestination,
  type SwipeStart,
} from "@/lib/akis-swipe";
import { LEVELS, levelColor, levelSlug } from "@/lib/levels";
import { modeTitle, type ModeId } from "@/lib/modes";
import { MIX_SCOPE, loadFeedState, loadOrder, saveFeedState, saveOrder } from "@/lib/session";
import { DEFAULT_SPEED, isAudioUnlocked, loadSpeed, markAudioUnlocked, saveSpeed } from "@/lib/settings";

type Filter = "ALL" | Level;

/** Without a pack this is the mixed feed of one format; with one it plays that
 * pack only. Every format keeps its own progress. */
export function ReelFeed({
  kind,
  pack,
  focusCard,
}: {
  kind: ModeId;
  pack?: string;
  focusCard?: string;
}) {
  const scope = `${kind}:${pack || MIX_SCOPE}`;
  const scrollRef = useRef<HTMLDivElement>(null);
  const slideRefs = useRef<(HTMLDivElement | null)[]>([]);
  const offsetsRef = useRef<number[]>([]);
  const heightRef = useRef(0);
  const restoredRef = useRef(false);
  const touchRef = useRef<SwipeStart | null>(null);
  const swipeLockedRef = useRef(false);
  const swipeUnlockRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const scrollAnimationRef = useRef<number | null>(null);

  const [cards, setCards] = useState<Card[] | null>(null);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<Filter>("ALL");
  const [index, setIndex] = useState(0);
  const [results, setResults] = useState<Record<string, AnswerResult>>({});
  const [busyId, setBusyId] = useState("");
  const [unlocked, setUnlocked] = useState(isAudioUnlocked);
  const [packInfo, setPackInfo] = useState<Pack | null>(null);
  const [siblings, setSiblings] = useState<Pack[]>([]);
  // one setting for the whole site; every card's player reads it
  const [speed, setSpeed] = useState(DEFAULT_SPEED);

  const changeSpeed = useCallback((value: number) => {
    setSpeed(value);
    saveSpeed(value);
  }, []);

  useEffect(() => {
    api<Card[]>(
      pack
        ? `/api/akis/reels?kind=${kind}&pack=${encodeURIComponent(pack)}`
        : `/api/akis/reels?kind=${kind}`,
    )
      .then((data) => {
        // read back what a trip to /ogren left behind
        const saved = loadFeedState(scope);
        // a pack always plays in its stored order; only the mixed feed is shuffled
        const order = pack ? [] : loadOrder(scope);
        const ordered = order.length
          ? [...data].sort((a, b) => {
              const ai = order.indexOf(a.id);
              const bi = order.indexOf(b.id);
              return (ai < 0 ? order.length : ai) - (bi < 0 ? order.length : bi);
            })
          : data;
        if (!pack && !order.length) saveOrder(scope, ordered.map((c) => c.id));
        setCards(ordered);
        setResults(saved.results);
        // an explicit card wins over the remembered position
        const asked = focusCard ? ordered.findIndex((c) => c.id === focusCard) : -1;
        setIndex(
          asked >= 0 ? asked : Math.min(saved.index, Math.max(0, ordered.length - 1)),
        );
        setBusyId("");
        setError("");
        setSpeed(loadSpeed());
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Akış yüklenemedi"));
  }, [kind, pack, scope, focusCard]);

  // pack header and the "next pack" link at the end
  useEffect(() => {
    if (!pack) return;
    const level = pack.slice(0, pack.lastIndexOf("-"));
    api<{ packs: Pack[] }>(`/api/akis/packs?kind=${kind}&level=${encodeURIComponent(level)}`)
      .then((data) => {
        setSiblings(data.packs);
        setPackInfo(data.packs.find((p) => p.id === pack) ?? null);
      })
      .catch(() => setSiblings([]));
  }, [kind, pack]);

  const visible = useMemo(() => {
    const all = cards ?? [];
    if (pack || filter === "ALL") return all;
    return all.filter((c) => c.level === filter);
  }, [cards, filter, pack]);

  // Come back from the chat exactly where the learner left off.
  useEffect(() => {
    if (restoredRef.current || !visible.length) return;
    restoredRef.current = true;
    const target = slideRefs.current[Math.min(index, visible.length - 1)];
    target?.scrollIntoView({ block: "start" });
  }, [visible, index]);

  // Only persist once the feed has loaded, otherwise the empty first render
  // would overwrite the state we are about to restore.
  useEffect(() => {
    if (cards === null) return;
    saveFeedState(scope, { index, results });
  }, [cards, index, results, scope]);

  /** Slides grow with their content, so the active card is found from the
   * measured tops rather than a fixed slide height. Re-measured whenever the
   * content height changes (a card grows when it is answered). */
  const measure = useCallback(() => {
    const root = scrollRef.current;
    if (!root) return;
    const rootTop = root.getBoundingClientRect().top;
    offsetsRef.current = slideRefs.current.map((el) =>
      el ? el.getBoundingClientRect().top - rootTop + root.scrollTop : 0,
    );
    heightRef.current = root.scrollHeight;
  }, []);

  useEffect(() => {
    const root = scrollRef.current;
    if (!root || !visible.length) return;
    measure();
    let last = -1;
    const pick = () => {
      if (root.scrollHeight !== heightRef.current) measure();
      const line = root.scrollTop + root.clientHeight * 0.35;
      const offsets = offsetsRef.current;
      let at = 0;
      for (let i = 0; i < visible.length; i += 1) {
        if (offsets[i] !== undefined && offsets[i] <= line) at = i;
      }
      if (at === last) return;
      last = at;
      setIndex(at);
    };
    root.addEventListener("scroll", pick, { passive: true });
    window.addEventListener("resize", measure);
    return () => {
      root.removeEventListener("scroll", pick);
      window.removeEventListener("resize", measure);
    };
  }, [visible, measure]);

  const goTo = useCallback(
    (to: number) => {
      const root = scrollRef.current;
      const el = slideRefs.current[to];
      if (!root || !el) return;
      measure();
      const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      const target = offsetsRef.current[to] ?? 0;
      const touchDevice = window.matchMedia("(hover: none) and (pointer: coarse)").matches;
      if (scrollAnimationRef.current !== null) {
        cancelAnimationFrame(scrollAnimationRef.current);
        scrollAnimationRef.current = null;
      }

      if (still || !touchDevice) {
        root.scrollTo({ top: target, behavior: still ? "auto" : "smooth" });
        return;
      }

      const from = root.scrollTop;
      const distance = target - from;
      if (Math.abs(distance) < 1) return;
      const started = performance.now();
      const tick = (now: number) => {
        const progress = Math.min(1, (now - started) / AKIS_SWIPE_DURATION_MS);
        const eased = 1 - Math.pow(1 - progress, 3);
        root.scrollTop = from + distance * eased;
        if (progress < 1) {
          scrollAnimationRef.current = requestAnimationFrame(tick);
        } else {
          root.scrollTop = target;
          scrollAnimationRef.current = null;
        }
      };
      scrollAnimationRef.current = requestAnimationFrame(tick);
    },
    [measure],
  );

  const beginSwipe = useCallback((event: TouchEvent<HTMLDivElement>) => {
    if (
      swipeLockedRef.current ||
      !window.matchMedia("(hover: none) and (pointer: coarse)").matches
    ) return;
    const touch = event.touches[0];
    const target = event.target as HTMLElement;
    const slide = target.closest<HTMLElement>(".feed-slide");
    const touchedCardScroll = target.closest<HTMLElement>(".feed-card-scroll");
    const cardScroll =
      touchedCardScroll && slide?.contains(touchedCardScroll)
        ? touchedCardScroll
        : slide?.querySelector<HTMLElement>(".feed-card-scroll");
    if (!touch || !slide || !cardScroll) return;

    const slideIndex = Number(slide.dataset.index);
    if (!Number.isInteger(slideIndex)) return;
    touchRef.current = {
      y: touch.clientY,
      index: slideIndex,
      // If the card itself has content left in this direction, this gesture
      // belongs to the card rather than to the surrounding feed.
      canMoveBack: cardScroll.scrollTop > 2,
      canMoveForward:
        cardScroll.scrollTop + cardScroll.clientHeight < cardScroll.scrollHeight - 2,
    };
  }, []);

  const finishSwipe = useCallback(
    (event: TouchEvent<HTMLDivElement>) => {
      const start = touchRef.current;
      touchRef.current = null;
      const touch = event.changedTouches[0];
      if (!start || !touch) return;

      const destination = akisSwipeDestination(start, touch.clientY, visible.length);
      if (destination !== null) {
        swipeLockedRef.current = true;
        if (swipeUnlockRef.current) clearTimeout(swipeUnlockRef.current);
        goTo(destination);
        swipeUnlockRef.current = setTimeout(() => {
          swipeLockedRef.current = false;
          swipeUnlockRef.current = null;
        }, AKIS_SWIPE_LOCK_MS);
      }
    },
    [goTo, visible.length],
  );

  const cancelSwipe = useCallback(() => {
    touchRef.current = null;
  }, []);

  useEffect(() => () => {
    if (swipeUnlockRef.current) clearTimeout(swipeUnlockRef.current);
    if (scrollAnimationRef.current !== null) cancelAnimationFrame(scrollAnimationRef.current);
  }, []);

  const answer = useCallback(
    async (card: Card, choice: string) => {
      if (results[card.id]) return;
      setBusyId(card.id);
      try {
        const result = await api<AnswerResult>(`/api/akis/reels/${card.id}/answer`, {
          method: "POST",
          body: JSON.stringify({ choice }),
        });
        setResults((old) => ({ ...old, [card.id]: result }));
      } catch (e) {
        setError(e instanceof Error ? e.message : "Cevap gönderilemedi");
      } finally {
        setBusyId("");
      }
    },
    [results],
  );

  // Keyboard: arrows move between cards, A-E answers the open one.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      const card = visible[index];
      if (e.key === "ArrowDown" || e.key === "PageDown") {
        e.preventDefault();
        goTo(Math.min(index + 1, visible.length - 1));
      } else if (e.key === "ArrowUp" || e.key === "PageUp") {
        e.preventDefault();
        goTo(Math.max(index - 1, 0));
      } else if (card && /^[a-eA-E]$/.test(e.key) && !results[card.id]) {
        const letter = e.key.toUpperCase();
        if (letter in card.options) void answer(card, letter);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [visible, index, results, goTo, answer]);

  const answeredCount = visible.filter((c) => results[c.id]).length;
  const correctCount = visible.filter((c) => results[c.id]?.correct).length;
  const nextPack = packInfo ? siblings.find((p) => p.index === packInfo.index + 1) ?? null : null;

  return (
    <div className="feed-stage relative flex h-[100dvh] flex-col">
      <header className="flex-none px-3 pb-2 pt-[max(0.75rem,env(safe-area-inset-top))] sm:px-4">
        <div className="mx-auto flex max-w-xl items-center justify-between gap-3">
          {pack ? (
            <Link
              href={`/akis/${kind}/seviye/${levelSlug(packInfo?.level ?? pack.slice(0, pack.lastIndexOf("-")))}`}
              className="tap-link min-w-0 gap-2 text-[#f4efe4]"
            >
              <span aria-hidden="true">←</span>
              <span className="truncate font-serif text-lg">
                {packInfo?.title ?? "Paket"}
              </span>
            </Link>
          ) : (
            <Link href="/akis" className="font-serif text-lg text-[#f4efe4]">
              {modeTitle(kind)}
            </Link>
          )}
          <div className="flex flex-none items-center gap-2 text-[0.72rem] text-[rgba(244,239,228,0.75)]">
            <span>
              {answeredCount ? `${correctCount}/${answeredCount} doğru` : "henüz cevap yok"}
            </span>
            {pack ? null : <Link href="/akis" className="rounded-lg px-2 py-1 hover:bg-[rgba(255,255,255,0.1)]">biçimler</Link>}
          </div>
        </div>

        <div className={`mx-auto mt-2 max-w-xl flex-wrap items-center gap-1.5 ${pack ? "hidden" : "flex"}`}>
          {(["ALL", ...LEVELS] as Filter[]).map((value) => {
            const on = filter === value;
            return (
              <button
                key={value}
                type="button"
                onClick={() => {
                  setFilter(value);
                  setIndex(0);
                  restoredRef.current = false;
                }}
                className="min-h-8 rounded-full border px-3 py-1 text-[0.72rem] font-semibold transition"
                style={{
                  color: on ? "#12212f" : "rgba(244,239,228,0.8)",
                  borderColor: value === "ALL" ? "rgba(244,239,228,0.35)" : levelColor(value),
                  background: on
                    ? value === "ALL"
                      ? "#f4efe4"
                      : levelColor(value)
                    : "transparent",
                }}
              >
                {value === "ALL" ? "hepsi" : value}
              </button>
            );
          })}
        </div>

        <div className="mx-auto mt-2 h-1 max-w-xl overflow-hidden rounded-full bg-[rgba(244,239,228,0.16)]">
          <div
            className="h-full rounded-full bg-[#dcc79a] transition-[width] duration-300"
            style={{ width: visible.length ? `${((index + 1) / visible.length) * 100}%` : "0%" }}
          />
        </div>
      </header>

      <div
        ref={scrollRef}
        className="feed-scroll flex-1"
        onTouchStart={beginSwipe}
        onTouchEnd={finishSwipe}
        onTouchCancel={cancelSwipe}
      >
        {error && !cards ? (
          <div className="flex h-full items-center justify-center p-6">
            <div className="card max-w-sm p-6 text-center">
              <p className="font-serif text-xl text-[var(--terracotta)]">Akış yüklenemedi</p>
              <p className="prose-quiet mt-2 text-sm">{error}</p>
              <p className="prose-quiet mt-2 text-xs">
                Bağlantıyı yenileyip tekrar deneyebilirsin.
              </p>
            </div>
          </div>
        ) : null}

        {cards === null && !error ? (
          <div className="flex h-full items-center justify-center p-6">
            <div className="card pulse-soft h-72 w-full max-w-xl" />
          </div>
        ) : null}

        {visible.map((card, i) => (
          <div
            key={card.id}
            data-index={i}
            ref={(el) => {
              slideRefs.current[i] = el;
            }}
            className="feed-slide flex min-h-full items-center justify-center px-3 py-4 sm:px-4"
          >
            <div className="feed-card-scroll w-full max-w-xl">
              <ReelCard
                card={card}
                index={i}
                total={visible.length}
                active={i === index}
                result={results[card.id] ?? null}
                busy={busyId === card.id}
                unlocked={unlocked}
                onUnlock={() => {
                  markAudioUnlocked();
                  setUnlocked(true);
                }}
                onAnswer={(choice) => void answer(card, choice)}
                onNext={() => goTo(i + 1)}
                pack={pack}
                mode={kind}
                speed={speed}
                onSpeedChange={changeSpeed}
              />
              {i === 0 && !results[card.id] ? (
                <p className="nudge mt-3 text-center text-xs text-[rgba(244,239,228,0.7)]">
                  <span className="lg:hidden">yukarı kaydır ↓</span>
                  <span className="hidden lg:inline">kaydır, ok tuşlarını ya da sağdaki düğmeleri kullan</span>
                </p>
              ) : null}
            </div>
          </div>
        ))}

        {cards !== null && visible.length === 0 ? (
          <div className="flex h-full items-center justify-center p-6">
            <div className="card max-w-sm p-6 text-center">
              <p className="font-serif text-xl text-[var(--navy)]">Bu seviyede kart yok</p>
              <button type="button" className="btn btn-outline mt-3" onClick={() => setFilter("ALL")}>
                Hepsini göster
              </button>
            </div>
          </div>
        ) : null}

        {visible.length ? (
          <div
            data-index={visible.length}
            ref={(el) => {
              slideRefs.current[visible.length] = el;
            }}
            className="feed-slide flex min-h-full items-center justify-center px-3 py-4 sm:px-4"
          >
            <div className="feed-card-scroll w-full max-w-sm">
              <div className="card w-full p-7 text-center">
                <p className="font-serif text-2xl text-[var(--navy)]">
                  {pack ? "Paket bitti" : "Akışın sonu"}
                </p>
                <p className="prose-quiet mt-2 text-sm">
                  {answeredCount
                    ? `${visible.length} karttan ${answeredCount} tanesini cevapladın, ${correctCount} doğru.`
                    : "Henüz soru cevaplamadın."}
                </p>
                <div className="mt-4 flex flex-col gap-2">
                  {nextPack ? (
                    <Link href={`/akis/${kind}?pack=${encodeURIComponent(nextPack.id)}`} className="btn btn-primary">
                      {nextPack.title} →
                    </Link>
                  ) : (
                    <button type="button" className="btn btn-primary" onClick={() => goTo(0)}>
                      Başa dön
                    </button>
                  )}
                  {pack ? (
                    <Link
                      href={`/akis/${kind}/seviye/${levelSlug(packInfo?.level ?? pack.slice(0, pack.lastIndexOf("-")))}`}
                      className="btn btn-outline"
                    >
                      Paketler
                    </Link>
                  ) : (
                    <Link href="/akis" className="btn btn-outline">
                      Biçimler
                    </Link>
                  )}
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </div>

      {/* Mouse users get real buttons instead of hunting with the wheel. */}
      {visible.length ? (
        <div className="pointer-events-none absolute inset-y-0 right-4 hidden items-center lg:flex xl:right-8">
          <div className="pointer-events-auto flex flex-col gap-2">
            <button
              type="button"
              aria-label="Önceki kart"
              disabled={index === 0}
              onClick={() => goTo(Math.max(index - 1, 0))}
              className="grid h-11 w-11 place-items-center rounded-full border border-[rgba(244,239,228,0.3)] text-lg text-[#f4efe4] transition hover:bg-[rgba(244,239,228,0.14)] disabled:opacity-30"
            >
              ↑
            </button>
            <button
              type="button"
              aria-label="Sonraki kart"
              disabled={index >= visible.length - 1}
              onClick={() => goTo(Math.min(index + 1, visible.length - 1))}
              className="grid h-11 w-11 place-items-center rounded-full border border-[rgba(244,239,228,0.3)] text-lg text-[#f4efe4] transition hover:bg-[rgba(244,239,228,0.14)] disabled:opacity-30"
            >
              ↓
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
