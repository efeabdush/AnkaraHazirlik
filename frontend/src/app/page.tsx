import Link from "next/link";

const sessions = [
  {
    label: "1. Oturum",
    total: 60,
    duration: "120 dakika",
    tone: "badge-navy",
    parts: [
      { name: "Dinleme", points: 20, note: "Üç kısa diyalog ve not alarak dinlenen bir ders", detail: "Diyalog soruları kayıt çalarken görünür. Son derste önce yalnızca not alırsın; sorular dinleme bittikten sonra açılır.", href: "/listening" },
      { name: "Okuma", points: 20, note: "İki okuma metni ve bir cümle yerleştirme çalışması", detail: "Okuma metinlerinde ana fikir, ayrıntı ve çıkarım soruları; cümle yerleştirmede ise paragraflar arasındaki anlam akışı ölçülür.", href: "/reading" },
      { name: "Dil kullanımı", points: 20, note: "Cloze ve aynı anlamı veren cümleyi bulma", detail: "Cloze soruları boşluğu bağlama uygun dil bilgisi veya kelimeyle tamamlatır. Restatement soruları aynı düşünceyi koruyan seçeneği buldurur.", href: "/use-of-english" },
    ],
  },
  {
    label: "2. Oturum",
    total: 20,
    duration: "60 dakika",
    tone: "badge-gold",
    parts: [{ name: "Yazma", points: 20, note: "60 dakikada en az 250 kelimelik görüş kompozisyonu", detail: "Bir görüşü açıkça savunur, neden ve örneklerle geliştirirsin. Metin görev, dil bilgisi, kelime ve tutarlılık başlıklarında incelenir.", href: "/writing" }],
  },
  {
    label: "3. Oturum",
    total: 20,
    duration: "~10 dakika",
    tone: "badge",
    parts: [{ name: "Konuşma", points: 20, note: "Konu kartı, bir dakika hazırlık ve takip soruları", detail: "Karttaki ana soruyu geliştirir, verilen maddelere değinir ve takip sorularını yanıtlarsın. Kayıt sonrasında akıcılık ve dil kullanımı geri bildirimi alırsın.", href: "/speaking" }],
  },
];

export default function HomePage() {
  return (
    <div className="space-y-16">
      {/* ---------- hero ---------- */}
      <section className="rise grid gap-8 md:grid-cols-[1.1fr_0.9fr] md:items-center">
        <div className="space-y-5">
          <span className="badge badge-navy">Yeterlik sınavına hazırlık</span>
          <h1 className="font-serif text-4xl leading-[1.1] tracking-tight text-[var(--navy)] md:text-[3.35rem]">
            Sınavı, sınavdaki
            <br />
            gibi çalış.
          </h1>
          <p className="prose-quiet max-w-xl text-lg">
            Ankara Üniversitesi B1+ yeterlik yapısında üç oturumun tamamını çalış: dinleme, okuma, dil kullanımı,
            yazma ve konuşma. İçerikler özgündür; sonuçlarda neyi neden kaçırdığını somut biçimde görürsün.
          </p>
          <div className="flex flex-wrap items-center gap-3 pt-1">
            <Link href="/exam" className="btn btn-primary">
              Sınav merkezine geç
            </Link>
            <Link href="/resources" className="btn btn-outline">
              Resmi kaynaklar
            </Link>
          </div>
        </div>

        {/* exam structure — grouped by session, table-like */}
        <div className="panel p-7">
          <div className="flex items-baseline justify-between">
            <p className="text-[0.7rem] uppercase tracking-[0.16em] text-[rgba(244,239,228,0.6)]">Sınav yapısı</p>
            <p className="text-[0.7rem] text-[rgba(244,239,228,0.6)]">3 oturum</p>
          </div>
          <p className="mt-1 font-serif text-5xl">
            100 <span className="text-xl text-[rgba(244,239,228,0.7)]">puan</span>
          </p>

          <div className="mt-6 space-y-5">
            {sessions.map((s) => (
              <div key={s.label}>
                <div className="flex items-center justify-between border-b border-[rgba(244,239,228,0.18)] pb-1.5 text-xs">
                  <span className="font-semibold uppercase tracking-[0.12em] text-[#dcc79a]">{s.label}</span>
                  <span className="text-[rgba(244,239,228,0.75)]">
                    {s.duration} · <span className="font-semibold text-[#f4efe4]">{s.total} puan</span>
                  </span>
                </div>
                <div className="mt-2.5 space-y-2">
                  {s.parts.map((p) => (
                    <div key={p.name} className="flex items-center gap-3 text-xs text-[rgba(244,239,228,0.9)]">
                      <span className="w-24 flex-none">{p.name}</span>
                      <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-[rgba(244,239,228,0.14)]">
                        <span
                          className="block h-full rounded-full bg-[#dcc79a]"
                          style={{ width: `${p.points}%` }}
                        />
                      </span>
                      <span className="w-7 flex-none text-right font-semibold">{p.points}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <p className="mt-6 text-xs leading-relaxed text-[rgba(244,239,228,0.6)]">
            Çubuklar 100 puan içindeki payı gösterir. Bölüm pratiği ve tam oturum akışı ayrı ayrı kullanılabilir.
          </p>
        </div>
      </section>

      {/* ---------- how it works ---------- */}
      <section className="space-y-5">
        <div>
          <p className="eyebrow">Nasıl çalışır</p>
          <h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">Çöz, değerlendir, eksiğini çalış</h2>
        </div>
        <div className="grid items-start gap-4 md:grid-cols-3">
          <div className="card card-lift p-6">
            <div className="demo-stage">
              <div className="eq">
                <i /><i /><i /><i /><i /><i /><i />
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2.5">
              <span className="font-serif text-2xl text-[var(--gold)]">1</span>
              <h3 className="font-medium text-[var(--navy)]">Kaydı dinle</h3>
            </div>
            <p className="prose-quiet mt-2 text-sm">
              Sınav modunda kayıt gerçek sınavdaki gibi en fazla iki kez çalar. Diyalogda sorular dinlerken açıktır;
              derste önce not alırsın, sorular kayıt bitince açılır. Pratik modunda sınır yok.
            </p>
          </div>

          <div className="card card-lift p-6">
            <div className="demo-stage">
              <div className="quiz-demo">
                <div className="quiz-row"><span className="quiz-dot" /><span className="quiz-bar" /></div>
                <div className="quiz-row"><span className="quiz-dot" /><span className="quiz-bar" /></div>
                <div className="quiz-row"><span className="quiz-dot" /><span className="quiz-bar" /></div>
                <div className="quiz-row"><span className="quiz-dot" /><span className="quiz-bar" /></div>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2.5">
              <span className="font-serif text-2xl text-[var(--gold)]">2</span>
              <h3 className="font-medium text-[var(--navy)]">Sınav düzeninde cevapla</h3>
            </div>
            <p className="prose-quiet mt-2 text-sm">
              Cevap ekranı sınav kâğıdı düzenindedir: dört seçenek, tek doğru. İşaretle, gönder; puanın ve her sorunun
              doğru cevabı gerekçesiyle birlikte anında karşına gelir.
            </p>
          </div>

          <div className="card card-lift p-6">
            <div className="demo-stage">
              <div className="chat-demo">
                <span className="chat-q">Bu neden yanlış?</span>
                <span className="chat-typing"><i /><i /><i /></span>
                <span className="chat-a">Konuşmacı ders saatini değiştirdi, bu yüzden…</span>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2.5">
              <span className="font-serif text-2xl text-[var(--gold)]">3</span>
              <h3 className="font-medium text-[var(--navy)]">Takıldığını yapay zekâya sor</h3>
            </div>
            <p className="prose-quiet mt-2 text-sm">
              Sonuç ekranında her sorunun altında bir sohbet kutusu var. &ldquo;Bu neden yanlış?&rdquo; diye yaz; yapay
              zekâ kayda ve soruya bakarak Türkçe, gerekçeli bir açıklama verir.
            </p>
          </div>
        </div>
      </section>

      {/* ---------- sessions, table view ---------- */}
      <section className="space-y-5">
        <div>
          <p className="eyebrow">Sınav</p>
          <h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">Üç oturum, 100 puan</h2>
          <p className="prose-quiet mt-2 max-w-2xl text-sm">
            Yeterlik sınavı üç ayrı oturumda yapılır. Her bölüm 20 puandır; ilk oturum üç bölümü birden kapsar.
          </p>
        </div>
        <div className="grid items-start gap-4 md:grid-cols-3">
          {sessions.map((s) => (
            <details key={s.label} className="card group overflow-hidden">
              <summary className="flex cursor-pointer list-none items-center justify-between border-b border-[var(--line)] bg-[rgba(28,61,90,0.04)] px-5 py-3.5 [&::-webkit-details-marker]:hidden">
                <span className="font-serif text-lg text-[var(--navy)]">{s.label}</span>
                <span className="flex items-center gap-2"><span className={s.tone}>{s.total} puan</span><span className="text-[var(--gold)] transition-transform group-open:rotate-45">+</span></span>
              </summary>
              <div className="flex-1 divide-y divide-[var(--line-soft)] px-5">
                {s.parts.map((p) => (
                  <div key={p.name} className="py-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                      <p className="font-medium text-[var(--navy)]">{p.name}</p>
                      <p className="mt-0.5 text-xs text-[var(--ink-2)]">{p.note}</p>
                      </div>
                      <span className="flex-none pt-0.5 text-sm font-semibold text-[var(--gold)]">{p.points}</span>
                    </div>
                    <p className="prose-quiet mt-3 text-xs">{p.detail}</p>
                    <Link href={p.href} className="mt-3 inline-flex text-xs font-medium text-[var(--navy)] hover:underline">Bu bölümü çalış →</Link>
                  </div>
                ))}
              </div>
              <div className="border-t border-[var(--line-soft)] px-5 py-2.5 text-xs text-[var(--ink-3)]">Süre: {s.duration} · Ayrıntı için karta dokun</div>
            </details>
          ))}
        </div>
      </section>

      {/* ---------- listening structure explained ---------- */}
      <section className="card overflow-hidden">
        <div className="border-b border-[var(--line)] bg-[rgba(28,61,90,0.04)] px-7 py-5">
          <p className="eyebrow">Dinleme bölümü</p>
          <h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">Bir dinleme sınavı dört kayıttan oluşur</h2>
          <p className="prose-quiet mt-2 max-w-3xl text-sm">
            İlk üç kayıt (Track I–III) kısa kampüs diyaloglarıdır, sorular dinlerken önündedir. Dördüncü kayıt (Track
            IV) yaklaşık beş dakikalık bir derstir: önce not alırsın, sorular kayıt bitince açılır.
          </p>
        </div>
        <div className="grid gap-0 md:grid-cols-2">
          <div className="border-b border-[var(--line)] p-7 md:border-b-0 md:border-r">
            <div className="flex items-center gap-3">
              <span className="badge badge-navy">Track I–III</span>
              <span className="live-dot" />
            </div>
            <h3 className="mt-3 font-serif text-2xl text-[var(--navy)]">Diyalog</h3>
            <p className="prose-quiet mt-2 text-sm">
              Öğrenci ile görevli arasında kısa bir kampüs konuşması: kayıt bürosu, kütüphane, danışman görüşmesi…
              Her diyalogda dört soru vardır ve dinlerken işaretlersin.
            </p>
            <Link href="/listening" className="btn btn-outline mt-5">
              Diyaloğa geç
            </Link>
          </div>
          <div className="p-7">
            <div className="flex items-center gap-3">
              <span className="badge badge-gold">Track IV</span>
              <span className="live-dot" />
            </div>
            <h3 className="mt-3 font-serif text-2xl text-[var(--navy)]">Not almalı ders</h3>
            <p className="prose-quiet mt-2 text-sm">
              Tek konuşmacının beş dakikalık dersi. Dinlerken çizgili deftere not alırsın; notlar puanlanmaz ama
              sorular kayıt bittikten sonra geldiği için iyi not almak işini kolaylaştırır.
            </p>
            <Link href="/listening" className="btn btn-outline mt-5">
              Derse geç
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
