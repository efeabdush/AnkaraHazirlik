import type { Metadata } from "next";
import { createPageMetadata } from "@/lib/seo";

export const metadata: Metadata = createPageMetadata(
  "Ankara Üniversitesi Muafiyet Sınavı Kaynakları",
  "Ankara Üniversitesi İngilizce hazırlık yeterlik ve muafiyet sınavının resmî örnekleri ile ücretsiz B1+ dinleme, okuma ve dil çalışma kaynakları.",
  "/resources",
);

const groups = [
  {
    title: "Resmi kaynaklar",
    desc: "Sınavın gerçek formatı ve örnek kitapçıklar.",
    tone: "badge-navy",
    items: [
      {
        name: "Örnek yeterlik / muafiyet sınavları",
        href: "https://yabdil.ankara.edu.tr/ingilizce-hazirlik-ornek-yeterlik-muafiyet-sinavlari/",
        note: "Üç oturumun tamamı, PDF",
      },
      {
        name: "Öğrenciler için yararlı siteler",
        href: "https://yabdil.ankara.edu.tr/ogrenciler-icin/",
        note: "Okulun önerdiği liste",
      },
      {
        name: "Konuşma sınavı örneği",
        href: "https://yabdil.ankara.edu.tr/wp-content/uploads/sites/297/2026/07/Sample-Proficiency-Exam-Session-3-Speaking-Exam.pdf",
        note: "3. oturum, konu kartı",
      },
    ],
  },
  {
    title: "Dinleme pratiği",
    desc: "Sınav formatına en yakın ücretsiz siteler.",
    tone: "badge-gold",
    items: [
      { name: "Randall’s ESL Cyber Listening Lab", href: "https://www.esl-lab.com/", note: "Diyalog + çoktan seçmeli" },
      { name: "News in Levels", href: "https://www.newsinlevels.com/", note: "B1 uzunluk ve sözcük" },
      { name: "British Council LearnEnglish", href: "https://learnenglish.britishcouncil.org/", note: "Podcast ve alıştırma" },
      { name: "BBC Learning English", href: "https://www.bbc.co.uk/learningenglish", note: "Kısa haber ve deyim" },
    ],
  },
  {
    title: "Sözcük ve dil bilgisi",
    desc: "Dil kullanımı bölümü için.",
    tone: "badge",
    items: [
      { name: "Oxford Learner’s Dictionaries", href: "https://www.oxfordlearnersdictionaries.com/", note: "A2–B2 tanımlar" },
      { name: "Vocabulary.com", href: "https://www.vocabulary.com/", note: "Akademik sözcük" },
    ],
  },
];

export default function ResourcesPage() {
  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <p className="eyebrow">Bağlantılar</p>
        <h1 className="font-serif text-4xl tracking-tight text-[var(--navy)]">Kaynaklar</h1>
        <p className="prose-quiet max-w-2xl">
          Bu siteler okulun kendi öneri listesinde yer alıyor. İçerikleri buraya kopyalanmaz; yeni sekmede açılır.
        </p>
      </header>

      {groups.map((g) => (
        <section key={g.title} className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <span className={g.tone}>{g.title}</span>
            <p className="text-sm text-[var(--ink-2)]">{g.desc}</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {g.items.map((item) => (
              <a
                key={item.href}
                href={item.href}
                target="_blank"
                rel="noreferrer"
                className="card card-lift group flex items-center justify-between gap-4 p-5"
              >
                <span>
                  <span className="block font-medium text-[var(--navy)]">{item.name}</span>
                  <span className="mt-0.5 block text-xs text-[var(--ink-2)]">{item.note}</span>
                </span>
                <span className="text-[var(--ink-3)] transition-transform group-hover:translate-x-0.5 group-hover:text-[var(--navy)]">
                  ↗
                </span>
              </a>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
