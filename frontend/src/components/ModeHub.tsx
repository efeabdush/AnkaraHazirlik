import Link from "next/link";
import { LEVELS, levelClass, levelNote } from "@/lib/levels";
import { MODES, type Mode } from "@/lib/modes";

export function AkisModeDemo({ kind }: { kind: Mode["demo"] }) {
  if (kind === "ask") {
    return (
      <div className="demo-ask" aria-hidden="true">
        <div className="demo-ask-wave">
          <i />
          <i />
          <i />
          <i />
          <i />
        </div>
        <div className="demo-ask-opts">
          <span className="demo-ask-opt" />
          <span className="demo-ask-opt" />
          <span className="demo-ask-opt" />
          <span className="demo-ask-opt" />
        </div>
      </div>
    );
  }
  if (kind === "spell") {
    // a line of text where one word is wrong and then gets caught
    return (
      <div className="demo-spell" aria-hidden="true">
        <span className="demo-spell-line">
          <i />
          <i />
          <b className="demo-spell-bad" />
          <i />
          <i />
        </span>
        <span className="demo-spell-line">
          <i />
          <i />
        </span>
      </div>
    );
  }
  return (
    // a sentence with a hole that the right word drops into
    <div className="demo-gap" aria-hidden="true">
      <span className="demo-gap-line">
        <i />
        <i />
        <b className="demo-gap-hole" />
        <i />
      </span>
      <span className="demo-gap-opts">
        <u />
        <u className="demo-gap-pick" />
        <u />
        <u />
      </span>
    </div>
  );
}

function BoltMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} aria-hidden="true" fill="currentColor">
      <path d="M13.2 2 4.6 13.1c-.3.4 0 .9.5.9h5.1l-1.4 8c-.1.6.6.9 1 .4l8.6-11.1c.3-.4 0-.9-.5-.9h-5.1l1.4-8c.1-.6-.6-.9-1-.4z" />
    </svg>
  );
}

export function ModeHub() {
  return (
    <div className="mx-auto w-full max-w-5xl">
      <header className="text-center">
        <h1 className="inline-flex items-center gap-2.5 font-serif text-4xl tracking-tight text-[var(--navy)] sm:text-5xl">
          Akış
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-[var(--gold)] text-[#fdfbf7] sm:h-11 sm:w-11">
            <BoltMark className="h-5 w-5 sm:h-6 sm:w-6" />
          </span>
        </h1>
        <p className="prose-quiet mx-auto mt-3 max-w-xl text-sm sm:text-base">
          Uzun teste oturacak vaktin olmadığı günler için kısa format. Bir biçim seç, kaydırarak
          çalış.
        </p>
      </header>

      <div className="mt-9 grid gap-4 md:grid-cols-3">
        {MODES.map((mode) => (
          <div key={mode.id} className="flex flex-col gap-2.5">
            {/* the card itself starts the mode without asking for a level */}
            <Link
              href={`/akis/${mode.id}`}
              aria-label={`${mode.title}: seviye seçmeden başla`}
              className="card card-lift group flex flex-1 flex-col p-4 sm:p-5"
            >
              <div className="mode-stage">
                <AkisModeDemo kind={mode.demo} />
              </div>

              <h2 className="mt-4 font-serif text-xl leading-tight text-[var(--navy)]">
                {mode.title}
              </h2>

              <p className="prose-quiet mt-1.5 flex-1 text-sm">{mode.blurb}</p>

              <div className="mt-3 flex items-center justify-between gap-2">
                <span className="text-xs text-[var(--ink-3)]">{mode.meta}</span>
                <span className="text-lg leading-none text-[var(--gold)] transition-transform group-hover:translate-x-0.5">
                  →
                </span>
              </div>
            </Link>

            <Link href={`/akis/${mode.id}/seviye`} className="btn btn-primary w-full">
              Seviyene göre ilerle
            </Link>
          </div>
        ))}
      </div>

      <section className="mt-12 border-t border-[var(--line)] pt-7">
        <p className="eyebrow">Seviyeler</p>
        <h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">
          Her biçim aynı dört seviyeyi kullanır
        </h2>
        <p className="prose-quiet mt-2 max-w-2xl text-sm">
          Renk soğuktan sıcağa gittikçe seviye yükselir. Bir biçimde seçtiğin seviye o biçimin kendi
          paketlerini açar; ilerlemen biçimler arasında karışmaz.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {LEVELS.map((level) => (
            <span key={level} className={levelClass(level)}>
              {level}
              <small>{levelNote[level]}</small>
            </span>
          ))}
        </div>
      </section>

      <footer className="mt-10 flex flex-wrap items-center justify-between gap-3 border-t border-[var(--line)] pt-6 text-xs leading-relaxed text-[var(--ink-2)]">
        <p className="max-w-lg">
          Ankara Hazırlık çalışma platformunun kısa format bölümü. Tüm kayıtlar ve sorular
          özgündür; resmî bir sınav içeriği değildir.
        </p>
        <Link href="/exam" className="tap-link underline underline-offset-4 hover:text-[var(--navy)]">Sınav merkezine dön</Link>
      </footer>
    </div>
  );
}
