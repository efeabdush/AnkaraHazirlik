import type { Metadata } from "next";
import { AboutContact } from "@/components/AboutContact";

export const metadata: Metadata = {
  title: "Hakkında ve iletişim · Ankara Hazırlık",
  description: "Ankara Hazırlık projesinin hikâyesi, bağımsızlık açıklaması ve iletişim formu.",
};

export default function AboutPage() {
  return (
    <div className="space-y-6 sm:space-y-8">
      <section className="grid gap-5 md:grid-cols-2">
        <article className="card p-6 sm:p-8">
          <p className="eyebrow">Ne için?</p>
          <p className="prose-quiet mt-4 text-[0.96rem]">
            Ai ile yeni yeni oynamaya başladığım için ihtiyaçlarıma göre bir proje geliştirmek de istedim, bu siteyi normalde
            bireysel kullanım için tasarlamıştım ama insanlara bedava böyle bir hizmet verebileceğimi farkettim, mantıklı da
            geldi. Hazırlık muafiyetine girecek insanların çalışabilmeleri için özelleştirilmiş bir site diyebilirim. Bu siteden
            hiçbir veri toplamıyorum, hiçbir gelir elde etmiyorum, bana herhangi bir getirisi olmuyor. Sadece paylaşmak
            istediğim bir proje olduğu için paylaşıyorum, umarım işinize yaramıştır. &lt;3
          </p>
        </article>

        <article className="card border-l-4 border-l-[var(--gold)] p-6 sm:p-8">
          <p className="eyebrow">Önemli ve net</p>
          <h2 className="mt-3 font-serif text-3xl text-[var(--navy)]">Resmî site değil.</h2>
          <div className="prose-quiet mt-4 space-y-4 text-[0.96rem]">
            <p>
              Bu site <strong className="text-[var(--ink)]">Ankara Üniversitesi, Yabancı Diller Yüksekokulu veya başka herhangi bir kurum tarafından hazırlanmış, desteklenmiş ya da onaylanmış değildir.</strong>
            </p>
            <p>
              İçerikler resmî olarak yayımlanan sınav yapısı ve ölçütler referans alınarak pratik amacıyla özgün biçimde
              hazırlanır. Buradaki AI değerlendirmeleri çalışma geri bildirimidir; resmî puan veya başarı garantisi değildir.
            </p>
          </div>
        </article>
      </section>

      <section className="card p-6 sm:p-8">
        <div>
          <p className="eyebrow">Yapan kişi</p>
          <h2 className="mt-3 font-serif text-3xl text-[var(--navy)]">Efe</h2>
          <p className="prose-quiet mt-3 text-[0.96rem]">İşine yaradıysa tanışabiliriz, yaramadıysa da tanışabiliriz :P</p>
          <div className="mt-5 flex flex-wrap gap-3">
            <a
              className="flex items-center gap-3 rounded-xl border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--ink)] transition-colors hover:border-[var(--navy)]"
              href="https://www.instagram.com/efe.abdush/"
              target="_blank"
              rel="noreferrer"
            >
              <svg className="h-5 w-5 text-[var(--navy)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <rect x="3" y="3" width="18" height="18" rx="5" />
                <circle cx="12" cy="12" r="4" />
                <circle cx="17.4" cy="6.7" r="1" fill="currentColor" stroke="none" />
              </svg>
              <span><span className="block text-xs text-[var(--ink-3)]">Instagram</span>efe.abdush</span>
            </a>
            <a
              className="flex items-center gap-3 rounded-xl border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--ink)] transition-colors hover:border-[var(--navy)]"
              href="https://www.linkedin.com/in/efeabdullahduman/"
              target="_blank"
              rel="noreferrer"
            >
              <svg className="h-5 w-5 text-[var(--navy)]" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <rect x="3" y="9" width="4" height="12" rx="0.8" />
                <circle cx="5" cy="5" r="2" />
                <path d="M10 9h3.8v1.7c1-1.3 2.4-2.1 4.2-2.1 3 0 4.7 1.9 4.7 5.7V21h-4v-6.1c0-1.9-.7-2.9-2.2-2.9-1.7 0-2.5 1.1-2.5 3.3V21h-4V9Z" />
              </svg>
              <span><span className="block text-xs text-[var(--ink-3)]">LinkedIn</span>Efe A. Duman</span>
            </a>
          </div>
        </div>
      </section>

      <AboutContact />
    </div>
  );
}
