"use client";

import { useEffect, useRef, useState } from "react";
import { api, getHumanToken, setHumanToken } from "@/lib/api";

type SecurityConfig = {
  turnstile_enabled: boolean;
  turnstile_site_key: string;
  session_minutes: number;
};

type TurnstileApi = {
  render: (
    target: HTMLElement,
    options: {
      sitekey: string;
      action: string;
      theme: "auto";
      callback: (token: string) => void;
      "error-callback": () => void;
      "expired-callback": () => void;
    },
  ) => string;
  remove: (widgetId: string) => void;
  reset: (widgetId: string) => void;
};

declare global {
  interface Window {
    turnstile?: TurnstileApi;
  }
}

let scriptPromise: Promise<void> | null = null;

function loadTurnstile() {
  if (window.turnstile) return Promise.resolve();
  if (scriptPromise) return scriptPromise;
  scriptPromise = new Promise((resolve, reject) => {
    const existing = document.getElementById("cloudflare-turnstile-script") as HTMLScriptElement | null;
    if (existing) {
      existing.addEventListener("load", () => resolve(), { once: true });
      existing.addEventListener("error", () => reject(new Error("Doğrulama bileşeni yüklenemedi.")), { once: true });
      return;
    }
    const script = document.createElement("script");
    script.id = "cloudflare-turnstile-script";
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Doğrulama bileşeni yüklenemedi."));
    document.head.appendChild(script);
  });
  return scriptPromise;
}

export function HumanVerification() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [config, setConfig] = useState<SecurityConfig | null>(null);
  const [verified, setVerified] = useState(() => Boolean(getHumanToken()));
  const [message, setMessage] = useState("Güvenli bağlantı hazırlanıyor…");

  useEffect(() => {
    api<SecurityConfig>("/api/security/config")
      .then(setConfig)
      .catch(() => setConfig({ turnstile_enabled: false, turnstile_site_key: "", session_minutes: 0 }));
    const requireVerification = () => {
      setVerified(false);
      setMessage("Devam etmek için kısa güvenlik kontrolünü tamamla.");
    };
    window.addEventListener("human-verification-required", requireVerification);
    return () => window.removeEventListener("human-verification-required", requireVerification);
  }, []);

  useEffect(() => {
    if (!config?.turnstile_enabled || verified || !containerRef.current) return;
    let widgetId = "";
    let cancelled = false;
    loadTurnstile()
      .then(() => {
        if (cancelled || !containerRef.current || !window.turnstile) return;
        setMessage("Bu kontrol otomatik olabilir; gerekirse kutuyu işaretle.");
        widgetId = window.turnstile.render(containerRef.current, {
          sitekey: config.turnstile_site_key,
          action: "practice",
          theme: "auto",
          callback: async (token) => {
            try {
              const result = await api<{ human_token: string; expires_at: number }>("/api/security/verify", {
                method: "POST",
                body: JSON.stringify({ token }),
              });
              setHumanToken(result.human_token, result.expires_at);
              setVerified(true);
            } catch (caught) {
              setMessage(caught instanceof Error ? caught.message : "Doğrulama başarısız oldu; tekrar dene.");
              if (widgetId && window.turnstile) window.turnstile.reset(widgetId);
            }
          },
          "error-callback": () => setMessage("Doğrulama yüklenemedi. Bağlantını kontrol edip sayfayı yenile."),
          "expired-callback": () => {
            setMessage("Kontrolün süresi doldu; kutuyu yeniden tamamla.");
            if (widgetId && window.turnstile) window.turnstile.reset(widgetId);
          },
        });
      })
      .catch((caught) => setMessage(caught instanceof Error ? caught.message : "Doğrulama bileşeni yüklenemedi."));
    return () => {
      cancelled = true;
      if (widgetId && window.turnstile) window.turnstile.remove(widgetId);
    };
  }, [config, verified]);

  if (!config?.turnstile_enabled || verified) return null;
  return (
    <aside className="fixed inset-x-3 bottom-3 z-50 mx-auto max-w-sm rounded-2xl border border-[#d7c8b3] bg-[#fffdf8] p-4 shadow-2xl" aria-live="polite">
      <p className="font-serif text-xl text-[#0d3a5a]">Kısa güvenlik kontrolü</p>
      <p className="mt-1 text-sm text-[#625a52]">{message}</p>
      <div ref={containerRef} className="mt-3 min-h-[65px]" />
    </aside>
  );
}
