import Link from "next/link";

export function PracticeMoreCard({ href, count, label }: { href: string; count: number; label: string }) {
  return (
    <Link
      href={href}
      className="group relative flex min-h-28 flex-col justify-between overflow-hidden rounded-2xl border border-[rgba(176,139,63,.45)] bg-[linear-gradient(145deg,rgba(176,139,63,.13),rgba(28,61,90,.08))] p-5 transition hover:-translate-y-0.5 hover:border-[var(--navy)] hover:shadow-[var(--shadow-md)]"
    >
      <span className="absolute -right-8 -top-10 font-serif text-8xl text-[rgba(28,61,90,.06)]">+</span>
      <span className="relative">
        <span className="eyebrow">Daha fazla pratik</span>
        <span className="mt-1 block font-serif text-xl text-[var(--navy)]">Tüm çalışmaları keşfet</span>
        <span className="prose-quiet mt-1 block text-xs">{label} bölümündeki {count} özgün çalışmanın tamamını gör.</span>
      </span>
      <span className="relative mt-3 text-sm font-semibold text-[var(--navy)]">Arşivi aç <span className="inline-block transition-transform group-hover:translate-x-1">→</span></span>
    </Link>
  );
}
