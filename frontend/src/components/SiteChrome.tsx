"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BrandMark } from "@/components/BrandMark";

const links = [
  { href: "/exam", label: "Sınav merkezi" },
  { href: "/akis", label: "⚡ Akış", featured: true },
  { href: "/resources", label: "Kaynaklar" },
  { href: "/about", label: "Hakkında" },
  { href: "/admin", label: "Yönetim" },
];

export function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-30 border-b border-[var(--line)] bg-[rgba(253,251,247,0.85)] backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-3 px-4 py-3 sm:px-5">
        <Link href="/" className="group flex items-center gap-2.5">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-[var(--navy)] text-[#dcc79a] shadow-sm transition-transform group-hover:scale-105">
            <BrandMark className="h-7 w-7" />
          </span>
          <span className="flex flex-col leading-none">
            <span className="font-serif text-lg tracking-tight text-[var(--navy)]">Ankara Hazırlık</span>
            <span className="mt-0.5 text-[0.66rem] uppercase tracking-[0.14em] text-[var(--ink-3)]">
              Yeterlik sınavı çalışması
            </span>
          </span>
        </Link>

        <nav aria-label="Ana menü" className="nav-scroll order-3 flex w-full items-center gap-1 overflow-x-auto pb-1 text-sm sm:order-none sm:w-auto sm:pb-0">
          {links.map((l) => {
            const active = pathname === l.href || pathname.startsWith(`${l.href}/`);
            return (
              <Link
                key={l.href}
                href={l.href}
                className={`flex-none rounded-lg px-3 py-1.5 transition-colors ${
                  l.featured
                    ? active
                      ? "bg-[var(--navy-deep)] font-semibold text-white shadow-sm"
                      : "bg-[var(--navy)] font-semibold text-white shadow-sm hover:bg-[var(--navy-deep)]"
                    : active
                    ? "bg-[rgba(28,61,90,0.09)] font-medium text-[var(--navy)]"
                    : "text-[var(--ink-2)] hover:bg-[rgba(28,61,90,0.05)] hover:text-[var(--navy)]"
                }`}
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="mt-16 border-t border-[var(--line)] bg-[rgba(253,251,247,0.6)]">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-5 py-8 text-xs text-[var(--ink-2)] sm:flex-row sm:items-center sm:justify-between">
        <p className="max-w-md leading-relaxed">
          <span className="font-medium text-[var(--navy)]">Ankara Hazırlık</span> — bağımsız bir çalışma platformudur;
          Ankara Üniversitesi ile resmi bir bağı yoktur. Tüm içerik özgündür.
        </p>
        <div className="flex flex-wrap items-center gap-4">
          <a
            className="underline decoration-[var(--line)] underline-offset-4 hover:text-[var(--navy)]"
            href="https://yabdil.ankara.edu.tr/ingilizce-hazirlik-ornek-yeterlik-muafiyet-sinavlari/"
          >
            Resmi örnek sınavlar
          </a>
          <Link className="underline decoration-[var(--line)] underline-offset-4 hover:text-[var(--navy)]" href="/resources">
            Kaynaklar
          </Link>
          <Link className="underline decoration-[var(--line)] underline-offset-4 hover:text-[var(--navy)]" href="/about">
            Hakkında ve iletişim
          </Link>
        </div>
      </div>
    </footer>
  );
}
