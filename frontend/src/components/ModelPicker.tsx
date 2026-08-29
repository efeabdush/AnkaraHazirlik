"use client";

import { useEffect, useMemo, useState } from "react";
import { API_URL, adminHeaders, api } from "@/lib/api";

export type ActiveSummary = {
  provider: string | null;
  provider_label: string | null;
  model: string | null;
  ready: boolean;
};

type ProviderInfo = {
  id: string;
  label: string;
  note: string;
  key_env: string;
  configured: boolean;
  key_source: "panel" | "env" | "none";
  key_masked: string;
};

type Props = {
  secret: string;
  active: ActiveSummary | null;
  onSaved: (a: ActiveSummary) => void;
};

const keyHelp: Record<string, { label: string; url: string }> = {
  OPENCODE_API_KEY: { label: "opencode.ai/auth", url: "https://opencode.ai/auth" },
  OPENROUTER_API_KEY: { label: "openrouter.ai/keys", url: "https://openrouter.ai/keys" },
  GEMINI_API_KEY: { label: "aistudio.google.com/apikey", url: "https://aistudio.google.com/apikey" },
};

export function ModelPicker({ secret, active, onSaved }: Props) {
  const [providers, setProviders] = useState<ProviderInfo[]>([]);
  const [provider, setProvider] = useState("");
  const [models, setModels] = useState<string[]>([]);
  const [model, setModel] = useState("");
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  const [keyDrafts, setKeyDrafts] = useState<Record<string, string>>({});
  const [keyBusy, setKeyBusy] = useState("");
  const [keyMsg, setKeyMsg] = useState<Record<string, string>>({});
  const [keyErr, setKeyErr] = useState<Record<string, string>>({});

  async function refreshProviders(pick?: string) {
    const d = await api<{ providers: ProviderInfo[]; active: ActiveSummary }>("/api/admin/providers", {
      headers: adminHeaders(secret),
    });
    setProviders(d.providers);
    const next = pick ?? d.active.provider ?? d.providers.find((p) => p.configured)?.id ?? "";
    setProvider(next);
    if (d.active.model) setModel(d.active.model);
    return d;
  }

  useEffect(() => {
    refreshProviders().catch((e) => setError(e.message));
    // initial load only
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [secret]);

  useEffect(() => {
    const info = providers.find((p) => p.id === provider);
    if (!provider || !info?.configured) return;

    let cancelled = false;

    async function loadModels() {
      setLoading(true);
      setError("");
      try {
        const data = await api<{ models: string[] }>(
          `/api/admin/models?provider=${encodeURIComponent(provider)}`,
          { headers: adminHeaders(secret) },
        );
        if (!cancelled) setModels(data.models);
      } catch (e) {
        if (!cancelled) {
          setModels([]);
          setError(e instanceof Error ? e.message : "Model listesi alınamadı");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void loadModels();
    return () => {
      cancelled = true;
    };
  }, [provider, providers, secret]);

  const shown = useMemo(() => {
    const q = filter.trim().toLowerCase();
    const list = q ? models.filter((m) => m.toLowerCase().includes(q)) : models;
    return list.slice(0, 300);
  }, [models, filter]);

  async function testKey(info: ProviderInfo) {
    const draft = (keyDrafts[info.key_env] ?? "").trim();
    if (!draft) return;
    setKeyBusy(info.key_env);
    setKeyErr((p) => ({ ...p, [info.key_env]: "" }));
    setKeyMsg((p) => ({ ...p, [info.key_env]: "" }));
    try {
      const res = await api<{ model_count: number; tested_with: string }>("/api/admin/keys", {
        method: "POST",
        headers: adminHeaders(secret),
        body: JSON.stringify({ key_env: info.key_env, api_key: draft }),
      });
      setKeyMsg((p) => ({
        ...p,
        [info.key_env]: `Çalışıyor · ${res.model_count} model (${res.tested_with})`,
      }));
      setKeyDrafts((p) => ({ ...p, [info.key_env]: "" }));
      await refreshProviders(info.id);
    } catch (e) {
      setKeyErr((p) => ({ ...p, [info.key_env]: e instanceof Error ? e.message : "Test başarısız" }));
    } finally {
      setKeyBusy("");
    }
  }

  async function removeKey(info: ProviderInfo) {
    setKeyBusy(info.key_env);
    try {
      await fetch(`${API_URL}/api/admin/keys/${info.key_env}`, {
        method: "DELETE",
        headers: adminHeaders(secret),
      });
      setKeyMsg((p) => ({ ...p, [info.key_env]: "" }));
      setModels([]);
      await refreshProviders();
    } finally {
      setKeyBusy("");
    }
  }

  async function saveModel() {
    setError("");
    setSaved(false);
    try {
      const result = await api<ActiveSummary>("/api/admin/model", {
        method: "POST",
        headers: adminHeaders(secret),
        body: JSON.stringify({ provider, model }),
      });
      onSaved(result);
      setSaved(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Kaydedilemedi");
    }
  }

  const current = providers.find((p) => p.id === provider);

  return (
    <section className="card p-7">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-serif text-2xl text-[var(--navy)]">Sağlayıcı ve model</h2>
          <p className="prose-quiet mt-1 text-sm">
            Anahtarı buraya yapıştır, test edilsin. Çalışırsa kaydedilir ve model listesi açılır.
          </p>
        </div>
        {active?.ready ? (
          <span className="badge badge-green">
            {active.provider_label} · {active.model}
          </span>
        ) : (
          <span className="badge badge-warn">model seçilmedi</span>
        )}
      </div>

      <div className="mt-6 space-y-3">
        {providers.map((p) => {
          const on = provider === p.id;
          const help = keyHelp[p.key_env];
          const busy = keyBusy === p.key_env;
          return (
            <div
              key={p.id}
              className={`rounded-xl border p-4 transition ${
                on ? "border-[var(--navy)] bg-[rgba(28,61,90,0.05)]" : "border-[var(--line)]"
              }`}
            >
              <div className="flex flex-wrap items-start justify-between gap-3">
                <button
                  type="button"
                  onClick={() => {
                    if (!p.configured) return;
                    setProvider(p.id);
                    setModel("");
                    setSaved(false);
                  }}
                  className="text-left"
                >
                  <span className="flex items-center gap-2">
                    <span className="font-medium text-[var(--navy)]">{p.label}</span>
                    {on ? <span className="badge badge-navy">seçili</span> : null}
                  </span>
                  <span className="mt-1 block text-xs leading-relaxed text-[var(--ink-2)]">{p.note}</span>
                </button>
                <span className={p.configured ? "badge badge-green" : "badge"}>
                  {p.configured ? `anahtar: ${p.key_masked}` : "anahtar yok"}
                </span>
              </div>

              <div className="mt-3 flex flex-wrap items-center gap-2">
                <input
                  type="password"
                  className="input flex-1 min-w-[220px]"
                  placeholder={p.configured ? "Yeni anahtarla değiştir" : "API anahtarını yapıştır"}
                  value={keyDrafts[p.key_env] ?? ""}
                  onChange={(e) => setKeyDrafts((prev) => ({ ...prev, [p.key_env]: e.target.value }))}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") void testKey(p);
                  }}
                />
                <button
                  type="button"
                  className="btn btn-primary text-sm"
                  disabled={busy || !(keyDrafts[p.key_env] ?? "").trim()}
                  onClick={() => testKey(p)}
                >
                  {busy ? "Test ediliyor…" : "Test et ve kaydet"}
                </button>
                {p.key_source === "panel" ? (
                  <button type="button" className="btn btn-quiet text-sm" disabled={busy} onClick={() => removeKey(p)}>
                    Sil
                  </button>
                ) : null}
              </div>

              <div className="mt-2 flex flex-wrap items-center gap-3 text-xs">
                {help ? (
                  <a className="text-[var(--ink-2)] underline" href={help.url} target="_blank" rel="noreferrer">
                    Anahtar al: {help.label}
                  </a>
                ) : null}
                {p.key_source === "env" ? <span className="text-[var(--ink-3)]">.env üzerinden geliyor</span> : null}
                {p.key_env === "OPENCODE_API_KEY" ? (
                  <span className="text-[var(--ink-3)]">Go ve Zen aynı anahtarı paylaşır</span>
                ) : null}
                {keyMsg[p.key_env] ? <span className="text-[var(--green)]">{keyMsg[p.key_env]}</span> : null}
                {keyErr[p.key_env] ? <span className="text-[var(--terracotta)]">{keyErr[p.key_env]}</span> : null}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-7 space-y-3">
        <div className="flex items-end justify-between gap-3">
          <p className="eyebrow">Model</p>
          {models.length ? <span className="text-xs text-[var(--ink-3)]">{models.length} model</span> : null}
        </div>

        {!current?.configured ? (
          <p className="prose-quiet text-sm">Önce yukarıdan bir sağlayıcının anahtarını kaydet.</p>
        ) : (
          <>
            <input
              className="input"
              placeholder="Listede ara: claude, gpt, glm, kimi…"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
            <select
              className="input"
              value={model}
              onChange={(e) => {
                setModel(e.target.value);
                setSaved(false);
              }}
              disabled={loading || !shown.length}
              size={Math.min(8, Math.max(3, shown.length))}
            >
              {shown.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            {loading ? <p className="text-xs text-[var(--ink-2)]">Model listesi alınıyor…</p> : null}
          </>
        )}

        <div className="flex flex-wrap items-center gap-3">
          <button type="button" className="btn btn-primary" onClick={saveModel} disabled={!provider || !model}>
            Modeli kaydet
          </button>
          {saved ? <span className="badge badge-green">kaydedildi</span> : null}
          {error ? <span className="text-sm text-[var(--terracotta)]">{error}</span> : null}
        </div>
      </div>
    </section>
  );
}
