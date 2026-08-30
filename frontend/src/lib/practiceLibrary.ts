export const practiceLibrary = {
  conversation: {
    label: "Diyalog arşivi",
    eyebrow: "Dinleme · Track I–III",
    description: "Kampüs yaşamından 25 özgün diyalog. Her çalışmada dört soru bulunur ve cevaplarını kayıt sürerken işaretlersin.",
    backHref: "/listening",
    backLabel: "Dinlemeye dön",
  },
  lecture: {
    label: "Not almalı ders arşivi",
    eyebrow: "Dinleme · Track IV",
    description: "Farklı akademik konularda 25 uzun ders kaydı. Kaydı dinlerken not alır, soruları kayıt bittikten sonra çözersin.",
    backHref: "/listening",
    backLabel: "Dinlemeye dön",
  },
  reading_standard: {
    label: "Passage I–II arşivi",
    eyebrow: "Okuma · Passage I–II",
    description: "Ana fikir, ayrıntı, çıkarım ve bağlam sorularını birlikte çalıştıran 25 özgün B1+ okuma metni.",
    backHref: "/reading",
    backLabel: "Okumaya dön",
  },
  reading_insertion: {
    label: "Passage III arşivi",
    eyebrow: "Okuma · Passage III",
    description: "Metnin akışını kurmayı öğreten 25 özgün cümle yerleştirme çalışması. Her metinde bir seçenek fazladır.",
    backHref: "/reading",
    backLabel: "Okumaya dön",
  },
  cloze: {
    label: "Cloze Text arşivi",
    eyebrow: "Dil kullanımı · Cloze",
    description: "Dil bilgisi ve kelime bilgisini bağlam içinde çalıştıran 25 özgün, beş soruluk cloze metni.",
    backHref: "/use-of-english",
    backLabel: "Dil kullanımına dön",
  },
  restatement: {
    label: "Restatement arşivi",
    eyebrow: "Dil kullanımı · Restatement",
    description: "Anlamı koruyarak yeniden ifade etmeyi ölçen 25 özgün çalışma; her çalışmada beş farklı soru bulunur.",
    backHref: "/use-of-english",
    backLabel: "Dil kullanımına dön",
  },
} as const;

export type PracticeKind = keyof typeof practiceLibrary;

export function isPracticeKind(value: string): value is PracticeKind {
  return value in practiceLibrary;
}

export function practiceHref(kind: PracticeKind, id: string) {
  if (kind === "conversation") return `/listening/conversation/${id}`;
  if (kind === "lecture") return `/listening/lecture/${id}`;
  return `/practice/${id}`;
}
