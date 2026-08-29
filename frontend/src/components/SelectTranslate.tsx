"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { lookup, type GlossaryEntry, type Hit, type WordBank } from "@/lib/glossary";

type Pop = { x: number; y: number; below: boolean; en: string; hit: Hit | null };

const kindLabel: Record<Hit["kind"], string> = {
  word: "Kelime",
  phrase: "Kelime grubu",
  sentence: "Cümle",
  words: "Kelime kelime",
};

export function SelectTranslate({
  glossary,
  words,
  children,
}: {
  glossary: GlossaryEntry[];
  words: WordBank;
  children: React.ReactNode;
}) {
  const rootRef = useRef<HTMLDivElement>(null);
  const [pop, setPop] = useState<Pop | null>(null);

  const close = useCallback(() => setPop(null), []);

  useEffect(() => {
    const onDown = (e: MouseEvent) => {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) close();
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    document.addEventListener("scroll", close, true);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("scroll", close, true);
    };
  }, [close]);

  function show(text: string, rect: DOMRect) {
    const below = rect.top <= 150;
    setPop({
      x: Math.min(Math.max(rect.left + rect.width / 2, 150), window.innerWidth - 150),
      y: below ? rect.bottom : rect.top,
      below,
      en: text.replace(/\s+/g, " ").trim(),
      hit: lookup(glossary, text, words),
    });
  }

  function onMouseUp(e: React.MouseEvent) {
    const target = e.target as HTMLElement | null;
    if (target?.closest("button, textarea, input, a, .no-translate")) return;
    const sel = window.getSelection();
    const root = rootRef.current;
    if (!sel || !root) return;

    if (sel.isCollapsed) {
      // A plain click still resolves the single word under the cursor.
      const word = expandToWord(sel);
      if (!word || !root.contains(word.node)) {
        close();
        return;
      }
      show(word.text, word.rect);
      return;
    }

    const text = sel.toString();
    if (text.trim().length < 2 || !sel.anchorNode || !root.contains(sel.anchorNode)) return;
    show(text, sel.getRangeAt(0).getBoundingClientRect());
  }

  return (
    <div ref={rootRef} onMouseUp={onMouseUp} className="select-translate">
      {children}
      {pop ? (
        <div
          className={`translate-pop ${pop.below ? "translate-pop-below" : ""}`}
          style={{ left: pop.x, top: pop.y }}
          role="status"
        >
          <p className="translate-pop-kicker">{pop.hit ? kindLabel[pop.hit.kind] : "Türkçe"}</p>
          {pop.hit ? (
            <>
              <p className="translate-pop-tr">{pop.hit.tr}</p>
              {pop.hit.parts ? (
                <ul className="translate-pop-parts">
                  {pop.hit.parts.map((part, i) => (
                    <li key={`${part.en}-${i}`}>
                      <span className="translate-pop-part-en">{part.en}</span>
                      <span className="translate-pop-part-tr">
                        {part.tr === "?" ? "karşılık yok" : part.tr}
                      </span>
                    </li>
                  ))}
                </ul>
              ) : null}
            </>
          ) : (
            <p className="translate-pop-miss">Bu seçim için hazır karşılık yok.</p>
          )}
          <p className="translate-pop-en">{pop.en}</p>
        </div>
      ) : null}
    </div>
  );
}

function expandToWord(sel: Selection): { text: string; rect: DOMRect; node: Node } | null {
  const node = sel.anchorNode;
  if (!node || node.nodeType !== Node.TEXT_NODE) return null;
  const text = node.textContent ?? "";
  const offset = sel.anchorOffset;
  const isWord = (c: string) => /[A-Za-z'’\-]/.test(c);
  if (!text || (!isWord(text[offset] ?? "") && !isWord(text[offset - 1] ?? ""))) return null;

  let start = offset;
  let end = offset;
  while (start > 0 && isWord(text[start - 1])) start -= 1;
  while (end < text.length && isWord(text[end])) end += 1;
  if (end - start < 2) return null;

  const range = document.createRange();
  range.setStart(node, start);
  range.setEnd(node, end);
  sel.removeAllRanges();
  sel.addRange(range);
  return { text: text.slice(start, end), rect: range.getBoundingClientRect(), node };
}
