"use client";

import { useState, type FormEvent } from "react";
import { api } from "@/lib/api";
import { MarkdownText } from "@/components/MarkdownText";

type Props = {
  attemptId: string;
  questionId: string;
};

const presets = ["Bu neden yanlış?", "Doğru cevabı açıkla", "Şıkları karşılaştır"];

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export function ExplainChat({ attemptId, questionId }: Props) {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("Bu neden yanlış?");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function send(text = message) {
    const clean = text.trim();
    if (!clean || busy) return;
    const userMessage: ChatMessage = { role: "user", content: clean };
    // Ekranda tüm konuşmayı göster; modele yalnızca son turları göndererek isteği küçük tut.
    const requestMessages: ChatMessage[] = [...messages.slice(-10), userMessage];
    setMessages((current) => [...current, userMessage]);
    setMessage("");
    setBusy(true);
    setError("");
    try {
      const data = await api<{ reply: string }>("/api/explain", {
        method: "POST",
        body: JSON.stringify({
          attempt_id: attemptId,
          question_id: questionId,
          message: clean,
          messages: requestMessages,
        }),
      });
      setMessages((current) => [...current, { role: "assistant", content: data.reply }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Sohbet açılamadı");
    } finally {
      setBusy(false);
    }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void send();
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
              void send(p);
            }}
          >
            {p}
          </button>
        ))}
      </div>

      {messages.length ? (
        <div className="mt-3 max-h-80 space-y-3 overflow-y-auto rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3" aria-live="polite">
          {messages.map((item, index) => (
            <div
              key={`${item.role}-${index}`}
              className={`max-w-[92%] rounded-xl px-3.5 py-2.5 text-sm leading-6 ${
                item.role === "user"
                  ? "ml-auto bg-[var(--navy)] text-white"
                  : "mr-auto border border-[var(--line-soft)] bg-white text-[var(--ink)]"
              }`}
            >
              {item.role === "assistant" ? <MarkdownText>{item.content}</MarkdownText> : item.content}
            </div>
          ))}
          {busy ? <p className="text-xs text-[var(--ink-3)]">Yanıt hazırlanıyor…</p> : null}
        </div>
      ) : (
        <p className="mt-3 text-sm leading-6 text-[var(--ink-2)]">
          İlk sorunu seç veya kendin yaz. Bu konuşma yalnızca bu soru ve bu sayfa açıkken sürer.
        </p>
      )}

      <form className="mt-3" onSubmit={submit}>
        <textarea
          className="input"
          rows={2}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Bu soruyla ilgili devamını sor…"
        />

        <div className="mt-2 flex flex-wrap items-center gap-3">
          <button type="submit" disabled={busy || !message.trim()} className="btn btn-primary text-sm">
            {busy ? "Yanıtlanıyor…" : "Gönder"}
          </button>
          <span className="text-xs text-[var(--ink-3)]">Yalnızca bu soru hakkında · sayfadan çıkınca silinir</span>
        </div>
      </form>

      {error ? <p className="mt-3 text-sm text-[var(--terracotta)]">{error}</p> : null}
    </div>
  );
}
