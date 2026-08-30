import type { Metadata } from "next";
import { SectionCatalog } from "@/components/SectionCatalog";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "Ankara Üniversitesi Hazırlık Okuma Pratiği",
  "Ankara Üniversitesi hazırlık muafiyet sınavı için B1+ okuma metinleri, ana fikir, ayrıntı, çıkarım ve cümle yerleştirme soruları çöz.",
  "/reading",
);

const groups = [
  { kind: "reading_standard", label: "Passage I–II", note: "Ana fikir, ayrıntı, çıkarım ve bağlamdan sözcük soruları · 6 soru" },
  { kind: "reading_insertion", label: "Passage III", note: "Dört boşluğa beş seçenekten uygun cümleyi yerleştir · 4 soru" },
];

export default function ReadingPage() {
  return (
    <div className="space-y-10">
      <header className="space-y-3"><p className="eyebrow">1. oturum · 20 puan</p><h1 className="font-serif text-4xl text-[var(--navy)]">Okuma</h1><p className="prose-quiet max-w-2xl">İki uzun metin ve bir cümle yerleştirme metni. Tüm içerikler B1+ düzeyinde ve özgündür.</p></header>
      <SectionCatalog groups={groups} />
    </div>
  );
}
