import type { Metadata } from "next";
import { ModeHub } from "@/components/ModeHub";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "Akış: kısa İngilizce pratikleri",
  "Dinleme, yanlış yazılan kelimeyi bulma ve boşluk doldurma kartlarıyla A1'den B1+ seviyesine kısa İngilizce pratiği yap.",
  "/akis",
);

export default function AkisPage() {
  return <ModeHub />;
}
