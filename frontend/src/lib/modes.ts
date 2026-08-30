/** The swipe formats. One entry here is everything the hub, the routes and the
 * feed need to know about a mode, so adding a fourth is a single object. */

export type ModeId = "sorular" | "kelime" | "bosluk";

export type Mode = {
  id: ModeId;
  title: string;
  blurb: string;
  meta: string;
  /** which looping demo the hub card shows */
  demo: "ask" | "spell" | "gap";
  /** label above the card content inside the feed */
  prompt: string;
};

export const MODES: Mode[] = [
  {
    id: "sorular",
    title: "Soru akışı",
    blurb: "20-30 saniyelik bir kayıt dinle, tek soruyu cevapla, kaydır. Takıldığın yerde sor.",
    meta: "kart başına ~40 sn",
    demo: "ask",
    prompt: "Kaydı dinle",
  },
  {
    id: "kelime",
    title: "Kelime akışı",
    blurb: "Kısa bir metinde bir kelime yanlış yazılmış. Hangisi olduğunu bul.",
    meta: "kart başına ~20 sn",
    demo: "spell",
    prompt: "Metni oku",
  },
  {
    id: "bosluk",
    title: "Boşluk doldurma",
    blurb: "Cümlede bir kelime eksik. Dört seçenekten doğru olanı yerine koy.",
    meta: "kart başına ~15 sn",
    demo: "gap",
    prompt: "Boşluğu tamamla",
  },
];

export const DEFAULT_MODE: ModeId = "sorular";

export function modeById(id: string | undefined): Mode | null {
  return MODES.find((m) => m.id === id) ?? null;
}

export function modeTitle(id: string | undefined): string {
  return modeById(id)?.title ?? "Akış";
}
