import Link from "next/link";
import { ExamProgressSummary } from "@/components/ExamProgressSummary";

const practiceSections = [
  { number: "01", title: "Dinleme", session: "1. oturum", score: "20 puan", href: "/listening", description: "Üç kısa kampüs diyaloğunu sorular açıkken, bir dersi ise önce not alarak çalış." },
  { number: "02", title: "Okuma", session: "1. oturum", score: "20 puan", href: "/reading", description: "Uzun metinlerde ana fikir ve ayrıntıyı; cümle yerleştirmede metin akışını çalış." },
  { number: "03", title: "Dil", session: "1. oturum", score: "20 puan", href: "/use-of-english", description: "Cloze ile bağlam içinde dil bilgisi ve kelimeyi, restatement ile anlam eşdeğerliğini çalış." },
  { number: "04", title: "Yazma", session: "2. oturum", score: "20 puan", href: "/writing", description: "Tema kartını çek, 60 dakikada en az 250 kelimelik opinion essay yaz ve geri bildirim al." },
  { number: "05", title: "Konuşma", session: "3. oturum", score: "20 puan", href: "/speaking", description: "Konu kartını çek, hazırlan, konuş; akıcılık, dolgu sesleri ve anlatım için geri bildirim al." },
];

export default function ExamHubPage() {
  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <span className="badge badge-navy">B1+ · çalışma alanı</span>
        <h1 className="font-serif text-4xl tracking-tight text-[var(--navy)] md:text-5xl">Sınav merkezi</h1>
        <p className="prose-quiet max-w-3xl">Önce tek bir bölümü tanı ve pratik yap. Hazır olduğunda sağdaki tam denemeyle 1. oturumun 120 dakikalık akışını başlat.</p>
      </header>

      <section className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_1px_17.5rem] xl:gap-8">
        <div>
          <div className="mb-4 flex flex-wrap items-end justify-between gap-2">
            <div><p className="eyebrow">Bölüm pratiği</p><h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">Önce neyle karşılaşacağını gör</h2></div>
            <span className="text-xs text-[var(--ink-3)]">İstediğin bölümden başla</span>
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {practiceSections.map((section) => (
              <Link key={section.href} href={section.href} className="card card-lift flex min-h-64 flex-col p-5">
                <div className="flex items-center justify-between gap-2"><span className="font-serif text-2xl text-[var(--gold)]">{section.number}</span><span className="badge">{section.score}</span></div>
                <p className="mt-5 text-[0.68rem] uppercase tracking-[0.14em] text-[var(--ink-3)]">{section.session}</p>
                <h3 className="mt-1 font-serif text-2xl text-[var(--navy)]">{section.title}</h3>
                <p className="prose-quiet mt-3 flex-1 text-sm">{section.description}</p>
                <span className="mt-5 border-t border-[var(--line)] pt-3 text-sm font-medium text-[var(--navy)]">Pratiğe gir →</span>
              </Link>
            ))}
          </div>
        </div>

        <div className="h-px bg-[var(--line)] xl:h-auto xl:w-px" aria-hidden="true" />

        <aside className="space-y-4">
          <div className="panel flex min-h-80 flex-col p-6">
            <span className="w-fit rounded-full border border-[rgba(244,239,228,.25)] px-2.5 py-1 text-[0.7rem] uppercase tracking-[.14em] text-[#dcc79a]">Hazır olduğunda</span>
            <h2 className="mt-5 font-serif text-3xl">Tam deneme</h2>
            <p className="mt-3 text-sm leading-6 text-[rgba(244,239,228,.75)]">Dinleme, okuma ve dil kullanımı kesintisiz biçimde açılır. Sayaç 120 dakikadan başlar; bu alan hızlı pratik için değildir.</p>
            <div className="mt-5 grid grid-cols-3 gap-2 text-center text-xs"><span className="rounded-lg bg-[rgba(255,255,255,.08)] p-2">3 bölüm</span><span className="rounded-lg bg-[rgba(255,255,255,.08)] p-2">60 puan</span><span className="rounded-lg bg-[rgba(255,255,255,.08)] p-2">120 dk</span></div>
            <Link href="/exam/session-1" className="btn mt-auto border border-[#dcc79a] bg-[#dcc79a] text-[var(--navy-deep)] hover:bg-[#ead8ae]">Tam denemeyi incele →</Link>
          </div>
          <div className="rounded-2xl border border-[var(--gold)] bg-[rgba(176,139,63,.08)] p-4 text-xs leading-6 text-[var(--ink-2)]"><b className="text-[var(--navy)]">Gerçek sınav uyarısı:</b> 1. oturumda 29,5/60 altı, sonraki oturumlara geçmek için yetersizdir. Platform seni kilitlemez; eksiğini gösterip pratiğe dönmene izin verir.</div>
        </aside>
      </section>

      <ExamProgressSummary />
    </div>
  );
}
