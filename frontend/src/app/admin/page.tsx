"use client";

import { useEffect, useState } from "react";
import { ModelPicker, type ActiveSummary } from "@/components/ModelPicker";
import { API_URL, adminHeaders, api } from "@/lib/api";

type AdminTest = {
  id: string;
  kind: string;
  title: string;
  topic: string;
  published: boolean;
  source: string;
  duration_sec: number;
  glossary_n: number;
  glossary_entries: number;
  glossary_words: number;
};

const KEY = "hazirlik-admin-secret";

const topicIdeas = [
  "lost library card",
  "changing a course section",
  "lab safety induction",
  "sleep and study habits",
  "family life in cities",
  "public transport in Ankara",
];

const generationKinds = [
  ["conversation", "Diyalog · Tracks I–III"],
  ["lecture", "Not almalı ders · Track IV"],
  ["reading_standard", "Okuma · Passage I–II"],
  ["reading_insertion", "Okuma · Cümle yerleştirme"],
  ["cloze", "Dil kullanımı · Cloze"],
  ["restatement", "Dil kullanımı · Restatement"],
  ["writing_prompt", "Yazma · Opinion essay konusu"],
  ["speaking_card", "Konuşma · Konu kartı"],
] as const;

const kindLabels: Record<string, string> = Object.fromEntries(generationKinds);

const statusLabels: Record<string, string> = {
  queued: "Sıraya alındı",
  script: "Metin yazılıyor",
  glossary: "Türkçe seçim paketi",
  audio: "Ses üretiliyor",
  ready: "Hazır",
  failed: "Başarısız",
};

export default function AdminPage() {
  const [secret, setSecret] = useState("");
  const [authed, setAuthed] = useState(false);
  const [active, setActive] = useState<ActiveSummary | null>(null);
  const [error, setError] = useState("");
  const [tests, setTests] = useState<AdminTest[]>([]);
  const [kind, setKind] = useState<(typeof generationKinds)[number][0]>("conversation");
  const [topic, setTopic] = useState("lost library card");
  const [jobId, setJobId] = useState("");
  const [jobStatus, setJobStatus] = useState("");
  const [jobError, setJobError] = useState("");
  const [glossaryBusy, setGlossaryBusy] = useState("");
  const [glossaryJobId, setGlossaryJobId] = useState("");
  const [glossaryNote, setGlossaryNote] = useState("");

  useEffect(() => {
    const stored = sessionStorage.getItem(KEY);
    // Local clones can open the panel directly. A protected deployment falls
    // back to the secret form after this harmless empty-secret probe.
    void login(stored ?? "", false);
    // mount-only restore
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!jobId || !secret) return;
    const t = setInterval(() => {
      fetch(`${API_URL}/api/admin/jobs/${jobId}`, { headers: adminHeaders(secret) })
        .then((r) => r.json())
        .then((j) => {
          setJobStatus(j.status);
          setJobError(j.error ?? "");
          if (j.status === "ready" || j.status === "failed") {
            clearInterval(t);
            void loadTests(secret);
          }
        })
        .catch(() => clearInterval(t));
    }, 2000);
    return () => clearInterval(t);
  }, [jobId, secret]);

  useEffect(() => {
    if (!glossaryJobId || !secret) return;
    const t = setInterval(() => {
      fetch(`${API_URL}/api/admin/jobs/${glossaryJobId}`, { headers: adminHeaders(secret) })
        .then((r) => r.json())
        .then((j) => {
          if (j.status === "glossary" || j.status === "queued") {
            setGlossaryNote("Cümle çevirisi üretiliyor…");
          }
          if (j.status === "ready" || j.status === "failed") {
            clearInterval(t);
            setGlossaryBusy("");
            setGlossaryJobId("");
            setGlossaryNote(j.error ? `Cümle çevirisi alınamadı: ${j.error}` : "Türkçe paket hazır.");
            void loadTests(secret);
          }
        })
        .catch(() => clearInterval(t));
    }, 2000);
    return () => clearInterval(t);
  }, [glossaryJobId, secret]);

  async function login(value = secret, showError = true) {
    setError("");
    try {
      const data = await api<{ ok: boolean; llm: boolean; active: ActiveSummary }>("/api/admin/status", {
        headers: adminHeaders(value),
      });
      sessionStorage.setItem(KEY, value);
      setSecret(value);
      setAuthed(true);
      setActive(data.active);
      await loadTests(value);
    } catch (e) {
      setAuthed(false);
      if (showError) setError(e instanceof Error ? e.message : "Giriş yapılamadı");
    }
  }

  async function loadTests(value: string) {
    const list = await api<AdminTest[]>("/api/admin/tests", { headers: adminHeaders(value) });
    setTests(list);
  }

  async function generate() {
    setError("");
    setJobError("");
    try {
      const data = await api<{ job_id: string }>("/api/admin/generate", {
        method: "POST",
        headers: adminHeaders(secret),
        body: JSON.stringify({ kind, topic, publish: true }),
      });
      setJobId(data.job_id);
      setJobStatus("queued");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Üretilemedi");
    }
  }

  async function toggle(id: string, published: boolean) {
    await api(`/api/admin/tests/${id}/publish`, {
      method: "POST",
      headers: adminHeaders(secret),
      body: JSON.stringify({ published: !published }),
    });
    await loadTests(secret);
  }

  async function rebuildGlossary(id: string) {
    setGlossaryBusy(id);
    setError("");
    setGlossaryNote("");
    try {
      const data = await api<{
        job_id: string | null;
        note?: string;
        glossary_words?: number;
      }>(`/api/admin/tests/${id}/glossary`, {
        method: "POST",
        headers: adminHeaders(secret),
      });
      setGlossaryNote(data.note ?? (data.glossary_words ? `${data.glossary_words} kelime kaydedildi.` : "Türkçe paket işlendi."));
      await loadTests(secret);
      if (data.job_id) {
        setGlossaryJobId(data.job_id);
      } else {
        setGlossaryBusy("");
      }
    } catch (e) {
      setGlossaryBusy("");
      setError(e instanceof Error ? e.message : "Türkçe paket üretilemedi");
    }
  }

  if (!authed) {
    return (
      <div className="mx-auto max-w-md">
        <form
          className="card rise space-y-4 p-7"
          onSubmit={(e) => {
            e.preventDefault();
            void login(secret);
          }}
        >
          <span className="badge badge-navy">Yönetim</span>
          <h1 className="font-serif text-3xl text-[var(--navy)]">Üretim paneli</h1>
          <p className="prose-quiet text-sm">
            Yerel kurulumda şifre gerekmez. İnternete açılan kurulumlarda ADMIN_SECRET zorunludur.
          </p>
          <input
            type="password"
            className="input"
            placeholder="ADMIN_SECRET"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
          />
          <button type="submit" className="btn btn-primary w-full">
            Giriş
          </button>
          {error ? <p className="text-sm text-[var(--terracotta)]">{error}</p> : null}
        </form>
      </div>
    );
  }

  const busy = jobStatus === "queued" || jobStatus === "script" || jobStatus === "glossary" || jobStatus === "audio";

  return (
    <div className="space-y-8">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <span className="badge badge-navy">Yerel yönetim</span>
          <h1 className="font-serif text-4xl tracking-tight text-[var(--navy)]">Üretim paneli</h1>
        </div>
        <span className={active?.ready ? "badge badge-green" : "badge badge-warn"}>
          {active?.ready ? `${active.provider_label} · ${active.model}` : "model seçilmedi"}
        </span>
      </header>

      {error ? <p className="text-sm text-[var(--terracotta)]">{error}</p> : null}
      {glossaryNote ? <p className="text-sm text-[var(--ink-2)]">{glossaryNote}</p> : null}

      <ModelPicker secret={secret} active={active} onSaved={setActive} />

      <section className="card p-7">
        <h2 className="font-serif text-2xl text-[var(--navy)]">Yeni test üret</h2>
        <p className="prose-quiet mt-1 text-sm">
          Seçtiğin bölümün resmî soru sayısına ve B1+ sınırlarına uygun özgün bir paket üretilir. Dinleme türlerinde ses ve Türkçe seçim paketi de hazırlanır.
        </p>

        <div className="mt-6 space-y-5">
          <div>
            <p className="eyebrow">Tür</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {generationKinds.map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setKind(value)}
                  className={`rounded-xl border px-4 py-2.5 text-sm transition ${
                    kind === value
                      ? "border-[var(--navy)] bg-[rgba(28,61,90,0.07)] font-medium text-[var(--navy)]"
                      : "border-[var(--line)] text-[var(--ink-2)] hover:border-[var(--navy)]"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="eyebrow">Konu</p>
            <input
              className="input mt-2"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Örnek: a student asks about a lab access card"
            />
            <div className="mt-2 flex flex-wrap gap-2">
              {topicIdeas.map((t) => (
                <button
                  key={t}
                  type="button"
                  className="badge hover:border-[var(--navy)] hover:text-[var(--navy)]"
                  onClick={() => setTopic(t)}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <button
              type="button"
              className="btn btn-primary"
              onClick={generate}
              disabled={!active?.ready || busy}
            >
              {busy ? "Üretiliyor…" : "Üret ve yayınla"}
            </button>
            {jobStatus ? (
              <span className={busy ? "badge badge-navy pulse-soft" : jobStatus === "ready" ? "badge badge-green" : "badge badge-warn"}>
                {statusLabels[jobStatus] ?? jobStatus}
              </span>
            ) : null}
          </div>

          {busy ? (
            <div className="flex items-center gap-2 text-xs text-[var(--ink-2)]">
              {["script", "glossary", "audio", "ready"].map((step) => (
                <span
                  key={step}
                  className={`h-1.5 flex-1 rounded-full ${
                    jobStatus === step || (step === "script" && jobStatus === "queued")
                      ? "bg-[var(--navy)]"
                      : "bg-[var(--line-soft)]"
                  }`}
                />
              ))}
            </div>
          ) : null}

          {jobError ? <p className="text-sm text-[var(--terracotta)]">{jobError}</p> : null}
        </div>
      </section>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="font-serif text-2xl text-[var(--navy)]">Testler</h2>
          <span className="text-xs text-[var(--ink-2)]">{tests.length} kayıt</span>
        </div>
        <div className="card divide-y divide-[var(--line-soft)]">
          {tests.map((t) => (
            <div key={t.id} className="flex flex-wrap items-center justify-between gap-3 p-5">
              <div className="min-w-0">
                <p className="font-medium text-[var(--navy)]">{t.title}</p>
                <p className="mt-0.5 flex flex-wrap items-center gap-2 text-xs text-[var(--ink-2)]">
                  <span>{kindLabels[t.kind] ?? t.kind}</span>
                  <span className="text-[var(--line)]">·</span>
                  <span>{t.source === "ai" ? "yapay zeka" : "hazır"}</span>
                  <span className="text-[var(--line)]">·</span>
                  {t.duration_sec ? <><span>~{Math.max(1, Math.round(t.duration_sec / 60))} dk</span><span className="text-[var(--line)]">·</span></> : null}
                  <span>
                    {t.glossary_entries
                      ? `${t.glossary_entries} cümle · ${t.glossary_words} kelime`
                      : t.glossary_words
                        ? `${t.glossary_words} kelime · cümle paketi yok`
                        : "Türkçe paket yok"}
                  </span>
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className={t.published ? "badge badge-green" : "badge"}>
                  {t.published ? "yayında" : "gizli"}
                </span>
                {(t.kind === "conversation" || t.kind === "lecture") && !t.glossary_entries ? (
                  <button
                    type="button"
                    className="btn btn-outline text-sm"
                    disabled={glossaryBusy === t.id}
                    onClick={() => void rebuildGlossary(t.id)}
                  >
                    {glossaryBusy === t.id ? "Türkçe…" : t.glossary_words ? "Cümle paketi" : "Türkçe paket"}
                  </button>
                ) : null}
                <button type="button" className="btn btn-outline text-sm" onClick={() => toggle(t.id, t.published)}>
                  {t.published ? "Gizle" : "Yayınla"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
