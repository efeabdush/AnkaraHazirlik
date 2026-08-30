import type { Metadata } from "next";
import { SectionCatalog } from "@/components/SectionCatalog";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "Ankara Üniversitesi Hazırlık Dil Kullanımı",
  "Ankara Üniversitesi İngilizce hazırlık muafiyet sınavı için B1+ cloze text, dil bilgisi, kelime ve restatement soruları çöz.",
  "/use-of-english",
);

const groups = [
  { kind: "cloze", label: "Cloze Texts I–III", note: "Dil bilgisi ve kelimeyi bağlam içinde ölçen beşer soru" },
  { kind: "restatement", label: "Restatement", note: "Cümlenin anlamını en doğru biçimde yeniden ifade eden seçeneği bul" },
];

export default function UseOfEnglishPage() {
  return (
    <div className="space-y-10">
      <header className="space-y-3"><p className="eyebrow">1. oturum · 20 puan</p><h1 className="font-serif text-4xl text-[var(--navy)]">Dil kullanımı</h1><p className="prose-quiet max-w-2xl">Üç cloze metni ve beş restatement sorusuyla dil bilgisi, kelime ve anlam ilişkisini çalış.</p></header>
      <SectionCatalog groups={groups} inline />
    </div>
  );
}
