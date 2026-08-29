export type GlossaryEntry = { en: string; tr: string };
export type WordBank = Record<string, string>;
export type Hit = {
  en: string;
  tr: string;
  kind: "word" | "phrase" | "sentence" | "words";
  parts?: { en: string; tr: string }[];
};

const WORD_RE = /[A-Za-z][A-Za-z'\-]*/g;
const EDGE = /^[\s"'“”‘’()[\]{}.,;:!?…\-–—]+|[\s"'“”‘’()[\]{}.,;:!?…\-–—]+$/g;

export function normalize(text: string): string {
  return text
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201c\u201d]/g, '"')
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

export function cleanSelection(text: string): string {
  return normalize(text).replace(EDGE, "");
}

function wordForms(word: string): string[] {
  const w = word.replace(EDGE, "");
  const forms = [w];
  if (w.endsWith("'s") || w.endsWith("s'")) forms.push(w.slice(0, -2));
  if (w.length > 3 && w.endsWith("ies")) forms.push(`${w.slice(0, -3)}y`);
  if (w.length > 3 && w.endsWith("es")) forms.push(w.slice(0, -2));
  if (w.length > 3 && w.endsWith("s") && !w.endsWith("ss")) forms.push(w.slice(0, -1));
  if (w.length > 4 && w.endsWith("ing")) forms.push(w.slice(0, -3), `${w.slice(0, -3)}e`);
  if (w.length > 3 && w.endsWith("ed")) forms.push(w.slice(0, -2), w.slice(0, -1), `${w.slice(0, -2)}e`);
  if (w.length > 4 && w.endsWith("ly")) forms.push(w.slice(0, -2));
  for (const f of [...forms]) {
    if (f.length > 2 && f[f.length - 1] === f[f.length - 2]) forms.push(f.slice(0, -1));
  }
  return forms.filter((f, i) => f && forms.indexOf(f) === i);
}

export function wordGloss(word: string, words: WordBank): string | null {
  const key = normalize(word);
  for (const form of wordForms(key)) {
    const hit = words[form];
    if (hit) return hit;
  }
  return null;
}

export function lookup(entries: GlossaryEntry[], selected: string, words: WordBank = {}): Hit | null {
  const needle = cleanSelection(selected);
  if (!needle) return null;

  const cleaned = entries.filter((e) => e?.en?.trim().length >= 2 && e?.tr?.trim());
  const byKey = new Map<string, GlossaryEntry>();
  for (const e of cleaned) {
    const key = cleanSelection(e.en);
    if (!byKey.has(key)) byKey.set(key, e);
  }

  const tokens = needle.match(WORD_RE) ?? [];
  const shown = selected.replace(/\s+/g, " ").trim();

  const exact = byKey.get(needle);
  if (exact) return { en: shown, tr: exact.tr, kind: tokens.length > 1 ? "phrase" : "word" };

  if (tokens.length <= 1) {
    const gloss = wordGloss(needle, words);
    if (gloss) return { en: shown, tr: gloss, kind: "word" };
    const short = cleaned
      .filter((e) => {
        const key = cleanSelection(e.en);
        return (key.match(WORD_RE) ?? []).length <= 3 && key.includes(needle);
      })
      .sort((a, b) => cleanSelection(a.en).length - cleanSelection(b.en).length);
    if (short[0]) return { en: short[0].en, tr: short[0].tr, kind: "phrase" };
    return null;
  }

  const covering = cleaned
    .filter((e) => cleanSelection(e.en).includes(needle))
    .sort((a, b) => cleanSelection(a.en).length - cleanSelection(b.en).length);
  for (const e of covering) {
    const hay = cleanSelection(e.en);
    if (needle.length / hay.length >= 0.8) return { en: e.en, tr: e.tr, kind: "sentence" };
  }

  const parts = tokens.map((t) => ({ en: t, tr: wordGloss(t, words) ?? "?" }));
  const known = parts.filter((p) => p.tr !== "?");
  if (!known.length) return null;
  return { en: shown, tr: known.map((p) => p.tr).join(" · "), kind: "words", parts };
}
