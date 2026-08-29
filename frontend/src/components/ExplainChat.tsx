"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { MarkdownText } from "@/components/MarkdownText";

type Props = {
  attemptId: string;
  questionId: string;
};

const presets = ["Bu neden yanlış?", "Doğru cevabı açıkla", "Şıkları karşılaştır"];

export function ExplainChat({ attemptId, questionId }: Props) {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("Bu neden yanlış?");
  const [reply, setReply] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function send(text = message) {
    setBusy(true);
    setError("");
    setReply("");
    try {
      const data = await api<{ reply: string }>("/api/explain", {
        method: "POST",
        body: JSON.stringify({
          attempt_id: attemptId,
          question_id: questionId,
          message: text,
        }),
      });
      setReply(data.reply);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Sohbet açılamadı");
    } finally {
      setBusy(false);
    }
  }

  if (!open) {
    return (
      <button type="button" className="btn btn-quiet mt-3 text-sm" onClick={() => setOpen(true)}>
        Anlamadım, sor
      </button>
    );
  }

  return (
    <div className="mt-4 rounded-xl border border-[var(--line)] bg-[rgba(176,139,63,0.06)] p-4">
      <div className="flex items-center justify-between gap-3">
        <p className="eyebrow">Soru sor</p>
        <button type="button" className="btn btn-quiet text-xs" onClick={() => setOpen(false)}>
          Kapat
        </button>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {presets.map((p) => (
          <button
            key={p}
            type="button"
            className="badge hover:border-[var(--navy)] hover:text-[var(--navy)]"
            onClick={() => {
              setMessage(p);
              void send(p);
            }}
          >
            {p}
          </button>
        ))}
      </div>

      <textarea
        className="input mt-3"
        rows={2}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Kendi sorunu yaz…"
      />

      <div className="mt-2 flex items-center gap-3">
        <button type="button" disabled={busy} onClick={() => send()} className="btn btn-primary text-sm">
          {busy ? "Yanıtlanıyor…" : "Gönder"}
        </button>
        <span className="text-xs text-[var(--ink-3)]">Yalnızca bu soru hakkında</span>
      </div>

      {error ? <p className="mt-3 text-sm text-[var(--terracotta)]">{error}</p> : null}
      {reply ? (
        <div className="mt-3 rounded-lg bg-[var(--paper)] p-4">
          <MarkdownText className="text-sm leading-7" >{reply}</MarkdownText>
        </div>
      ) : null}
    </div>
  );
}
