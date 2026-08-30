import type { Metadata } from "next";
import { AboutContact } from "@/components/AboutContact";
import { BrandMark } from "@/components/BrandMark";

export const metadata: Metadata = {
  title: "Hakkında ve iletişim · Ankara Hazırlık",
  description: "Ankara Hazırlık projesinin hikâyesi, bağımsızlık açıklaması ve iletişim formu.",
};

export default function AboutPage() {
  return (
    <div className="space-y-6 sm:space-y-8">
      <section className="panel relative overflow-hidden p-7 sm:p-10">
        <BrandMark className="pointer-events-none absolute -right-10 -top-12 h-64 w-64 text-[#dcc79a] opacity-[0.08]" />
        <div className="relative max-w-3xl">
          <p className="eyebrow !text-[#dcc79a]">Hakkında</p>
          <h1 className="mt-3 font-serif text-4xl leading-tight text-white sm:text-5xl">
            Önce kendim için yaptım. Sonra tek başıma kullanmak biraz ayıp geldi.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-8 text-[#ece3d2]">
            Ben Efe. Bir şeyi en iyi, onu gerçekten yapmaya çalışırken öğreniyorum. Bu site de aynı hikâyeden çıktı:
            ihtiyacım olan aracı bulamayınca, gerekeni öğrenip kendim yapmaya başladım.
          </p>
        </div>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <article className="card p-6 sm:p-8">
          <p className="eyebrow">Bu proje neden var?</p>
          <h2 className="mt-3 font-serif text-3xl text-[var(--navy)]">Dağınık hazırlığı tek yerde toplamak için.</h2>
          <div className="prose-quiet mt-4 space-y-4 text-[0.96rem]">
            <p>
              Hazırlık ve muafiyet sınavına çalışırken yalnızca soru çözmek değil; dinlemek, yazmak, konuşmak ve nerede
              takıldığını somut biçimde görmek gerekiyor. Ben de kendi pratiğim için bunları tek bir yerde toplamaya başladım.
            </p>
            <p>
              Sonra “madem çalışıyor, başkasının da işine yarasın” dedim. Ankara Hazırlık şu an gönüllü olarak geliştirdiğim,
              geri bildirim geldikçe toparlanan bağımsız bir öğrenci projesi. Kısacası: ürün canlı, geliştirici de hâlâ öğrenci. 🙂
            </p>
          </div>
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
        <div className="grid gap-6 md:grid-cols-[0.35fr_0.65fr] md:items-center">
          <div>
            <p className="eyebrow">Yapan kişi</p>
            <h2 className="mt-3 font-serif text-3xl text-[var(--navy)]">Efe Abdullah Duman</h2>
          </div>
          <p className="prose-quiet text-[0.96rem]">
            Python, Unity, elektronik, CAD ve 3B tasarım gibi birbirinden farklı araçlarla uğraşmamın ortak sebebi şu:
            kafamda bir fikir oluyor ve onu çalıştırmak için ne gerekiyorsa öğreniyorum. Şimdi Ankara Üniversitesi’nde
            Biyomedikal Mühendisliği yolculuğuna başlarken aynı merakı mühendislik, nöroteknoloji ve gerçek problemlere taşıyorum.
            Bu site de “bir şey yapmak istedim, gerektiği için öğrendim” dosyasının yaşayan üyelerinden biri.
          </p>
        </div>
      </section>

      <AboutContact
        linkedinUrl={process.env.NEXT_PUBLIC_LINKEDIN_URL}
        instagramUrl={process.env.NEXT_PUBLIC_INSTAGRAM_URL}
      />
    </div>
  );
}
