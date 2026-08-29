"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/exam", label: "Sınav merkezi" },
  { href: "/listening", label: "Dinleme" },
  { href: "/reading", label: "Okuma" },
  { href: "/use-of-english", label: "Dil" },
  { href: "/writing", label: "Yazma" },
  { href: "/speaking", label: "Konuşma" },
  { href: "/resources", label: "Kaynaklar" },
];

/** Özgün güneş kursu motifi — Ankara'yı çağrıştırır, birebir kopya değildir. */
const RAY_LINES: [number, number, number, number][] = [
  [31.5, 20, 35.5, 20],
  [29.96, 25.75, 33.42, 27.75],
  [25.75, 29.96, 27.75, 33.42],
  [20, 31.5, 20, 35.5],
  [14.25, 29.96, 12.25, 33.42],
  [10.04, 25.75, 6.58, 27.75],
  [8.5, 20, 4.5, 20],
  [10.04, 14.25, 6.58, 12.25],
  [14.25, 10.04, 12.25, 6.58],
  [20, 8.5, 20, 4.5],
  [25.75, 10.04, 27.75, 6.58],
  [29.96, 14.25, 33.42, 12.25],
];

function SunMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 40 40" className={className} aria-hidden="true">
      <g stroke="currentColor" fill="none" strokeWidth="2.1" strokeLinecap="round">
        <circle cx="20" cy="20" r="8.5" />
        {RAY_LINES.map(([x1, y1, x2, y2], i) => (
          <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} />
        ))}
      </g>
      <circle cx="20" cy="20" r="3" fill="currentColor" />
    </svg>
  );
}

export function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-30 border-b border-[var(--line)] bg-[rgba(253,251,247,0.85)] backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-3 px-4 py-3 sm:px-5">
        <Link href="/" className="group flex items-center gap-2.5">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-[var(--navy)] text-[#dcc79a] shadow-sm transition-transform group-hover:scale-105">
            <SunMark className="h-6 w-6" />
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
                  active
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
        </div>
      </div>
    </footer>
  );
}
