import type { Metadata } from "next";
import { WritingPractice } from "@/components/WritingPractice";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "İngilizce Hazırlık Writing Pratiği",
  "Ankara Üniversitesi hazırlık yeterlik sınavı için 60 dakikalık B1+ opinion essay yazma pratiği yap ve ölçütlere göre geri bildirim al.",
  "/writing",
);

export default function WritingPage() {
  return <WritingPractice />;
}
