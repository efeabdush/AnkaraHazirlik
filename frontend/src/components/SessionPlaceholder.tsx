import Link from "next/link";

type Props = {
  eyebrow: string;
  title: string;
  intro: string;
  items: [string, string][];
};

export function SessionPlaceholder({ eyebrow, title, intro, items }: Props) {
  return (
    <div className="space-y-8">
      <header className="space-y-3">
        <p className="eyebrow">{eyebrow}</p>
        <h1 className="font-serif text-4xl tracking-tight text-[var(--navy)]">{title}</h1>
        <p className="prose-quiet max-w-2xl">{intro}</p>
      </header>

      <div className="card divide-y divide-[var(--line-soft)]">
        {items.map(([k, v]) => (
          <div key={k} className="flex flex-col gap-1 p-5 sm:flex-row sm:items-center sm:gap-6">
            <span className="w-32 flex-none font-medium text-[var(--navy)]">{k}</span>
            <span className="prose-quiet text-sm">{v}</span>
          </div>
        ))}
      </div>

      <div className="card border-dashed p-6">
        <p className="font-serif text-xl text-[var(--navy)]">Bu bölüm henüz açık değil</p>
        <p className="prose-quiet mt-2 max-w-xl text-sm">
          Şu an dinleme bölümü tam çalışıyor. Bu bölüm aynı üretim akışıyla eklenecek.
        </p>
        <Link href="/listening" className="btn btn-primary mt-4">
          Dinlemeye dön
        </Link>
      </div>
    </div>
  );
}
