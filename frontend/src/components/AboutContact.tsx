"use client";

import { useEffect, useState, type FormEvent } from "react";
import { api } from "@/lib/api";

type Props = {
  linkedinUrl?: string;
  instagramUrl?: string;
};

type FormState = {
  name: string;
  email: string;
  category: "bug" | "content" | "general";
  message: string;
  website: string;
};

const emptyForm: FormState = {
  name: "",
  email: "",
  category: "bug",
  message: "",
  website: "",
};

function safeSocialUrl(value?: string) {
  if (!value) return "";
  try {
    const url = new URL(value);
    return url.protocol === "https:" ? url.toString() : "";
  } catch {
    return "";
  }
}

export function AboutContact({ linkedinUrl, instagramUrl }: Props) {
  const linkedin = safeSocialUrl(linkedinUrl);
  const instagram = safeSocialUrl(instagramUrl);
  const [enabled, setEnabled] = useState<boolean | null>(null);
  const [form, setForm] = useState<FormState>(emptyForm);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<"idle" | "sent" | "error">("idle");
  const [message, setMessage] = useState("");

  useEffect(() => {
    api<{ enabled: boolean }>("/api/contact/config")
      .then((result) => setEnabled(result.enabled))
      .catch(() => setEnabled(false));
  }, []);

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((current) => ({ ...current, [key]: value }));
    setStatus("idle");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!enabled || busy) return;
    setBusy(true);
    setStatus("idle");
    setMessage("");
    try {
      await api<{ ok: boolean }>("/api/contact", {
        method: "POST",
        body: JSON.stringify(form),
      });
      setForm(emptyForm);
      setStatus("sent");
      setMessage("Mesaj ulaştı. Yamuk bir şey varsa artık kaçamaz.");
    } catch (caught) {
      setStatus("error");
      setMessage(caught instanceof Error ? caught.message : "Mesaj gönderilemedi.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section id="iletisim" className="card grid overflow-hidden lg:grid-cols-[0.38fr_0.62fr]">
      <div className="panel rounded-none p-6 sm:p-8">
        <p className="eyebrow !text-[#dcc79a]">İletişim</p>
        <h2 className="mt-3 font-serif text-3xl leading-tight text-white">Bir şey yamuk mu?</h2>
        <p className="mt-4 max-w-sm text-sm leading-7 text-[#ece3d2]">
          Bozuk bir yer, kafa karıştıran bir soru ya da “şurası şöyle olsa daha tatlı olur” dediğin bir şey varsa yaz.
          Gerçek kullanıcı geri bildirimi bu projenin yakıtı.
        </p>

        {linkedin || instagram ? (
          <div className="mt-7 flex flex-wrap gap-2">
            {linkedin ? (
              <a className="btn border border-white/25 bg-white/10 text-sm text-white hover:bg-white/15" href={linkedin} target="_blank" rel="noreferrer">
                LinkedIn ↗
              </a>
            ) : null}
            {instagram ? (
              <a className="btn border border-white/25 bg-white/10 text-sm text-white hover:bg-white/15" href={instagram} target="_blank" rel="noreferrer">
                Instagram ↗
              </a>
            ) : null}
          </div>
        ) : (
          <p className="mt-7 text-xs leading-6 text-[#cfc5b2]">Sosyal bağlantılar kısa süre içinde burada olacak.</p>
        )}
      </div>

      <form className="space-y-4 p-6 sm:p-8" onSubmit={submit}>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block text-sm font-medium text-[var(--navy)]">
            Adın
            <input
              className="input mt-1.5"
              value={form.name}
              onChange={(event) => update("name", event.target.value)}
              minLength={2}
              maxLength={80}
              autoComplete="name"
              required
            />
          </label>
          <label className="block text-sm font-medium text-[var(--navy)]">
            E-posta
            <input
              className="input mt-1.5"
              type="email"
              value={form.email}
              onChange={(event) => update("email", event.target.value)}
              maxLength={160}
              autoComplete="email"
              required
            />
          </label>
        </div>

        <label className="block text-sm font-medium text-[var(--navy)]">
          Konu
          <select
            className="input mt-1.5"
            value={form.category}
            onChange={(event) => update("category", event.target.value as FormState["category"])}
          >
            <option value="bug">Bir şey bozuk</option>
            <option value="content">İçerik önerim var</option>
            <option value="general">Genel mesaj</option>
          </select>
        </label>

        <label className="block text-sm font-medium text-[var(--navy)]">
          Mesajın
          <textarea
            className="input mt-1.5 min-h-36 resize-y"
            value={form.message}
            onChange={(event) => update("message", event.target.value)}
            minLength={10}
            maxLength={4000}
            placeholder="Nerede ne oldu? Mümkünse hangi sayfada olduğunu da yaz."
            required
          />
        </label>

        <label className="absolute left-[-10000px] h-px w-px overflow-hidden" aria-hidden="true">
          Website
          <input tabIndex={-1} autoComplete="off" value={form.website} onChange={(event) => update("website", event.target.value)} />
        </label>

        {enabled === false ? (
          <p className="rounded-xl border border-[rgba(176,81,44,.25)] bg-[rgba(176,81,44,.06)] p-3 text-sm text-[var(--terracotta)]">
            Mesaj kutusu şu an hazırlanıyor. Sosyal bağlantılardan ulaşabilirsin.
          </p>
        ) : null}
        {status !== "idle" ? (
          <p className={`rounded-xl p-3 text-sm ${status === "sent" ? "bg-[rgba(47,107,81,.08)] text-[var(--green)]" : "bg-[rgba(176,81,44,.06)] text-[var(--terracotta)]"}`} aria-live="polite">
            {message}
          </p>
        ) : null}

        <div className="flex flex-wrap items-center gap-3">
          <button className="btn btn-primary" type="submit" disabled={busy || enabled !== true}>
            {busy ? "Gönderiliyor…" : enabled === null ? "Bağlantı kontrol ediliyor…" : "Mesajı gönder"}
          </button>
          <span className="text-xs text-[var(--ink-3)]">Mesajın sitede saklanmaz; doğrudan e-posta olarak iletilir.</span>
        </div>
      </form>
    </section>
  );
}
