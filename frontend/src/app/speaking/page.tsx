import type { Metadata } from "next";
import { SpeakingPractice } from "@/components/SpeakingPractice";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "İngilizce Hazırlık Speaking Pratiği",
  "Ankara Üniversitesi hazırlık muafiyet sınavı için B1+ konu kartlarıyla speaking pratiği yap; akıcılık, dil kullanımı ve dolgu sesleri için geri bildirim al.",
  "/speaking",
);

export default function SpeakingPage() {
  return <SpeakingPractice />;
}
