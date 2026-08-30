import type { Metadata } from "next";
import type { ReactNode } from "react";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "Ankara Üniversitesi Hazırlık Dinleme Pratiği",
  "Ankara Üniversitesi hazırlık muafiyet sınavı için B1+ kampüs diyalogları ve not almalı akademik ders kayıtlarıyla dinleme pratiği yap.",
  "/listening",
);

export default function ListeningLayout({ children }: { children: ReactNode }) {
  return children;
}
