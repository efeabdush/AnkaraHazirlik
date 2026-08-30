import type { Level } from "@/lib/api";

/** Level colours climb from calm green to warm terracotta, so difficulty is
 * readable at a glance while a card scrolls past. */
export const LEVELS: Level[] = ["A1", "A2", "B1", "B1+"];

export const levelNote: Record<Level, string> = {
  A1: "başlangıç",
  A2: "temel",
  B1: "orta",
  "B1+": "sınav düzeyi",
};

export const levelBlurb: Record<Level, string> = {
  A1: "Tek bir bilgi: fiyat, yer, saat. Kısa cümleler, yavaş konuşma.",
  A2: "Geçmiş zaman, basit sebepler, günlük kampüs işleri.",
  B1: "Plan değişir, karşılaştırma çıkar. Cevap bir adım düşünmeyi ister.",
  "B1+": "İma ve tutum. Sınavdaki dinleme parçalarının kısa hali.",
};

/** "B1+" cannot sit in a URL path, so levels travel as slugs. */
export function levelSlug(level: string) {
  return level.toLowerCase().replace("+", "-plus");
}

export function levelFromSlug(slug: string): Level | null {
  const found = LEVELS.find((l) => levelSlug(l) === slug.toLowerCase());
  return found ?? null;
}

/** The raw colour, for rails and dots that are not chips. */
export function levelColor(level: string) {
  switch (level) {
    case "A1":
      return "var(--lv-a1)";
    case "A2":
      return "var(--lv-a2)";
    case "B1":
      return "var(--lv-b1)";
    case "B1+":
      return "var(--lv-b1plus)";
    default:
      return "var(--line)";
  }
}

export function levelClass(level: string) {
  switch (level) {
    case "A1":
      return "lv lv-a1";
    case "A2":
      return "lv lv-a2";
    case "B1":
      return "lv lv-b1";
    case "B1+":
      return "lv lv-b1plus";
    default:
      return "lv";
  }
}
