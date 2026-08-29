"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api, type TestDetail, type TestSummary } from "@/lib/api";
import { saveExamProgress } from "@/lib/examProgress";
import { MarkdownText } from "@/components/MarkdownText";

type SpeechResultLike = { resultIndex: number; results: ArrayLike<{ isFinal: boolean; 0: { transcript: string } }> };
type RecognitionLike = {
  continuous: boolean; interimResults: boolean; lang: string;
  onstart: (() => void) | null; onend: (() => void) | null;
  onresult: ((event: SpeechResultLike) => void) | null;
  onerror: ((event: { error?: string }) => void) | null;
  start: () => void; stop: () => void;
};
type RecognitionCtor = new () => RecognitionLike;
type Phase = "pick" | "prep" | "speak" | "processing" | "review";
type RecognitionState = "waiting" | "live" | "fallback";
type SpeakingContent = { prompt?: string; bullets?: string[]; followups?: string[] };
type TranscriptionResult = {
  text: string; language: string; duration_sec: number; speech_duration_sec: number; long_pause_count: number; audio_deleted: boolean;
  filler_count: number; filler_words: Record<string, number>; hesitation_pause_count: number; word_repetition_count: number; elongation_count: number; unclear_word_count: number;
};
type SpeakingResult = { scores: Record<string, number>; session_score_20: number; level_summary_tr: string; priorities_tr: string[]; filler_feedback_tr: string; better_phrases: { instead_of: string; try: string; why_tr: string }[]; next_drill_tr: string[]; disclaimer_tr: string };
type ChatMessage = { role: "user" | "assistant"; content: string };

const scoreLabels: Record<string, string> = { task_completion: "Görevi tamamlama", grammar: "Dil bilgisi", vocabulary: "Kelime", fluency_pronunciation: "Akıcılık ve telaffuz" };
const fmt = (sec: number) => `${Math.floor(Math.max(0, sec) / 60).toString().padStart(2, "0")}:${(Math.max(0, sec) % 60).toString().padStart(2, "0")}`;

function analyseSpeech(text: string, duration: number, transcription: TranscriptionResult | null) {
  const words = text.toLowerCase().match(/[a-z]+(?:['’-][a-z]+)?/g) ?? [];
  const fillers = text.toLowerCase().match(/\b(?:um+|uh+|erm+|hmm+|you know|i mean)\b/g) ?? [];
  const counts = new Map<string, number>();
  for (let i = 0; i < words.length - 1; i += 1) { const phrase = `${words[i]} ${words[i + 1]}`; counts.set(phrase, (counts.get(phrase) ?? 0) + 1); }
  const repeated = [...counts.entries()].filter(([, count]) => count >= 3).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([phrase, count]) => `${phrase} (${count}×)`);
  const measuredDuration = transcription?.duration_sec || duration;
  const speakingMinutes = Math.max(1, transcription?.speech_duration_sec || measuredDuration) / 60;
  return {
    duration_sec: measuredDuration,
    word_count: words.length,
    filler_count: Math.max(fillers.length, transcription?.filler_count ?? 0),
    filler_words: transcription?.filler_words ?? {},
    repeated_phrases: repeated,
    long_pause_count: transcription?.long_pause_count ?? 0,
    hesitation_pause_count: transcription?.hesitation_pause_count ?? 0,
    word_repetition_count: transcription?.word_repetition_count ?? 0,
    elongation_count: transcription?.elongation_count ?? 0,
    unclear_word_count: transcription?.unclear_word_count ?? 0,
    speech_rate_wpm: Math.round(words.length / speakingMinutes),
  };
}

function Coach({ context }: { context: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([{ role: "assistant", content: "Değerlendirmeyi birlikte parçalayabiliriz. En çok zorlandığın noktayı söyle; sana ölçülebilir bir sonraki adım vereceğim." }]);
  const [input, setInput] = useState(""); const [busy, setBusy] = useState(false); const [error, setError] = useState("");
  async function send(preset?: string) {
    const content = (preset ?? input).trim(); if (!content || busy) return;
    const next = [...messages, { role: "user" as const, content }]; setMessages(next); setInput(""); setBusy(true); setError("");
    try { const data = await api<{ reply: string }>("/api/evaluate/coach", { method: "POST", body: JSON.stringify({ context, messages: next }) }); setMessages((old) => [...old, { role: "assistant", content: data.reply }]); }
    catch (caught) { setError(caught instanceof Error ? caught.message : "Koç yanıt veremedi"); } finally { setBusy(false); }
  }
  return <section className="card overflow-hidden">
    <div className="border-b border-[var(--line)] bg-[rgba(28,61,90,0.04)] p-5"><p className="eyebrow">Oturum içi AI koçu</p><h2 className="mt-1 font-serif text-2xl text-[var(--navy)]">Sakin, net, uygulanabilir</h2><p className="prose-quiet mt-1 text-sm">Bu sohbet sayfadan ayrılana kadar önceki mesajları hatırlar.</p></div>
    <div className="max-h-[28rem] space-y-3 overflow-y-auto p-5">{messages.map((message, index) => <div key={index} className={`max-w-[88%] rounded-xl px-4 py-3 text-sm leading-6 ${message.role === "user" ? "ml-auto whitespace-pre-wrap bg-[var(--navy)] text-white" : "border border-[var(--line)] bg-white"}`}>{message.role === "assistant" ? <MarkdownText>{message.content}</MarkdownText> : message.content}</div>)}{busy ? <span className="badge pulse-soft">düşünüyor…</span> : null}</div>
    <div className="flex flex-wrap gap-2 px-5 pb-3">{["En kritik eksiğim ne?", "Bana 7 günlük çalışma ver", "Bunu nasıl daha akıcı söylerdim?"].map((item) => <button key={item} type="button" className="badge hover:border-[var(--navy)]" onClick={() => void send(item)}>{item}</button>)}</div>
    <form className="flex gap-2 border-t border-[var(--line)] p-4" onSubmit={(event) => { event.preventDefault(); void send(); }}><input className="input" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Değerlendirme hakkında sor…" /><button className="btn btn-primary" disabled={busy || !input.trim()}>Gönder</button></form>
    {error ? <p className="px-5 pb-4 text-sm text-[var(--terracotta)]">{error}</p> : null}
  </section>;
}

function preferredRecordingType() {
  if (typeof MediaRecorder === "undefined") return "";
  return ["audio/webm;codecs=opus", "audio/ogg;codecs=opus", "audio/mp4", "audio/webm"].find((type) => MediaRecorder.isTypeSupported(type)) ?? "";
}

function extensionForMime(type: string) {
  if (type.includes("ogg")) return "ogg";
  if (type.includes("mp4")) return "m4a";
  return "webm";
}

export function SpeakingPractice() {
  const [cards, setCards] = useState<TestSummary[]>([]); const [card, setCard] = useState<TestDetail | null>(null); const [rollingTitle, setRollingTitle] = useState("Konu havuzu hazırlanıyor…"); const [rolling, setRolling] = useState(false);
  const [phase, setPhase] = useState<Phase>("pick"); const [prepLeft, setPrepLeft] = useState(60); const [elapsed, setElapsed] = useState(0); const [showTimer, setShowTimer] = useState(false);
  const [transcript, setTranscript] = useState(""); const [interim, setInterim] = useState(""); const [recognitionState, setRecognitionState] = useState<RecognitionState>("waiting"); const [recordingReady, setRecordingReady] = useState(false); const [transcription, setTranscription] = useState<TranscriptionResult | null>(null);
  const [inputLevel, setInputLevel] = useState(0); const [heardAudio, setHeardAudio] = useState(false);
  const [result, setResult] = useState<SpeakingResult | null>(null); const [busy, setBusy] = useState(false); const [error, setError] = useState("");
  const recognitionRef = useRef<RecognitionLike | null>(null); const recorderRef = useRef<MediaRecorder | null>(null); const streamRef = useRef<MediaStream | null>(null); const chunksRef = useRef<BlobPart[]>([]); const speakingActiveRef = useRef(false); const startedAtRef = useRef(0);
  const audioContextRef = useRef<AudioContext | null>(null); const meterFrameRef = useRef<number | null>(null); const meterUpdatedAtRef = useRef(0);
  const content = card?.content as SpeakingContent | undefined;
  const topicHint = `${content?.prompt ?? ""}\n${content?.bullets?.join("\n") ?? ""}`.trim();

  const stopMeter = useCallback(() => {
    if (meterFrameRef.current !== null) cancelAnimationFrame(meterFrameRef.current);
    meterFrameRef.current = null;
    const context = audioContextRef.current; audioContextRef.current = null;
    if (context && context.state !== "closed") void context.close();
    setInputLevel(0);
  }, []);

  const startRecording = useCallback(async () => {
    setError(""); setElapsed(0); setInterim(""); setTranscription(null); setRecognitionState("waiting"); setHeardAudio(false); setInputLevel(0); chunksRef.current = []; speakingActiveRef.current = true; startedAtRef.current = Date.now();
    try {
      if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") throw new Error("Bu tarayıcı ses kaydını desteklemiyor.");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
      streamRef.current = stream;
      const mimeType = preferredRecordingType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType, audioBitsPerSecond: 64000 } : undefined);
      recorderRef.current = recorder;
      recorder.ondataavailable = (event) => { if (event.data.size) chunksRef.current.push(event.data); };
      recorder.onerror = () => setError("Ses kaydı sırasında tarayıcı hatası oluştu. Konuşmayı bitirip tekrar dene.");
      recorder.start(1000); setRecordingReady(true);

      const AudioContextCtor = window.AudioContext ?? (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (AudioContextCtor) {
        const context = new AudioContextCtor(); const analyser = context.createAnalyser(); analyser.fftSize = 256; const source = context.createMediaStreamSource(stream); const samples = new Uint8Array(analyser.fftSize);
        source.connect(analyser); audioContextRef.current = context;
        const updateMeter = (now: number) => {
          analyser.getByteTimeDomainData(samples); let sum = 0;
          for (const sample of samples) { const normalized = (sample - 128) / 128; sum += normalized * normalized; }
          const level = Math.min(1, Math.sqrt(sum / samples.length) * 5);
          if (level > 0.035) setHeardAudio(true);
          if (now - meterUpdatedAtRef.current > 90) { setInputLevel(level); meterUpdatedAtRef.current = now; }
          if (speakingActiveRef.current) meterFrameRef.current = requestAnimationFrame(updateMeter);
        };
        meterFrameRef.current = requestAnimationFrame(updateMeter);
      }
    } catch (caught) {
      speakingActiveRef.current = false; setRecordingReady(false); setRecognitionState("fallback"); setError(caught instanceof Error ? `Mikrofon açılamadı: ${caught.message}` : "Mikrofon açılamadı."); return;
    }
    const scope = window as typeof window & { SpeechRecognition?: RecognitionCtor; webkitSpeechRecognition?: RecognitionCtor };
    const Recognition = scope.SpeechRecognition ?? scope.webkitSpeechRecognition;
    if (!Recognition) { setRecognitionState("fallback"); return; }
    const recognition = new Recognition(); recognition.continuous = true; recognition.interimResults = true; recognition.lang = "en-US";
    recognition.onstart = () => setRecognitionState("live");
    recognition.onresult = (event) => { let finalText = ""; let liveText = ""; for (let index = event.resultIndex; index < event.results.length; index += 1) { const item = event.results[index]; if (item.isFinal) finalText += `${item[0].transcript} `; else liveText += item[0].transcript; } if (finalText) setTranscript((old) => `${old} ${finalText}`.trim()); setInterim(liveText); };
    recognition.onerror = () => setRecognitionState("fallback"); recognition.onend = () => { if (speakingActiveRef.current) setRecognitionState("fallback"); }; recognitionRef.current = recognition;
    try { recognition.start(); } catch { setRecognitionState("fallback"); }
  }, []);

  const stopRecorder = useCallback(async () => {
    const recorder = recorderRef.current; recorderRef.current = null; if (!recorder) return null;
    const buildBlob = () => new Blob(chunksRef.current, { type: recorder.mimeType || "audio/webm" });
    if (recorder.state === "inactive") return buildBlob();
    return new Promise<Blob>((resolve) => { recorder.addEventListener("stop", () => resolve(buildBlob()), { once: true }); try { recorder.stop(); } catch { resolve(buildBlob()); } });
  }, []);

  const beginSpeaking = useCallback(() => { setPrepLeft(0); setPhase("speak"); void startRecording(); }, [startRecording]);

  useEffect(() => { api<TestSummary[]>("/api/tests?kind=speaking_card").then((items) => { setCards(items); setRollingTitle(items[0]?.title ?? "Konu bulunamadı"); }).catch((caught) => setError(caught instanceof Error ? caught.message : "Konu kartları yüklenemedi")); }, []);
  useEffect(() => { if (phase !== "prep") return; const timer = window.setInterval(() => setPrepLeft((value) => { if (value <= 1) { window.clearInterval(timer); beginSpeaking(); return 0; } return value - 1; }), 1000); return () => window.clearInterval(timer); }, [phase, beginSpeaking]);
  useEffect(() => { if (phase !== "speak") return; const timer = window.setInterval(() => setElapsed(Math.floor((Date.now() - startedAtRef.current) / 1000)), 1000); return () => window.clearInterval(timer); }, [phase]);
  useEffect(() => () => { speakingActiveRef.current = false; recognitionRef.current?.stop(); if (recorderRef.current?.state !== "inactive") recorderRef.current?.stop(); streamRef.current?.getTracks().forEach((track) => track.stop()); chunksRef.current = []; if (meterFrameRef.current !== null) cancelAnimationFrame(meterFrameRef.current); void audioContextRef.current?.close(); }, []);

  async function pickCard() {
    if (!cards.length || rolling) return; setRolling(true); setResult(null); setTranscript(""); setTranscription(null); setError(""); let tick = 0;
    const interval = window.setInterval(() => { setRollingTitle(cards[tick % cards.length].title); tick += 1; }, 90);
    window.setTimeout(async () => { window.clearInterval(interval); try { const chosen = cards[Math.floor(Math.random() * cards.length)]; setRollingTitle(chosen.title); setCard(await api<TestDetail>(`/api/tests/${chosen.id}`)); } catch (caught) { setError(caught instanceof Error ? caught.message : "Konu kartı açılamadı"); } finally { setRolling(false); } }, 1500);
  }

  async function finish() {
    speakingActiveRef.current = false; recognitionRef.current?.stop(); recognitionRef.current = null; setInterim(""); setError(""); setPhase("processing");
    const finalElapsed = Math.max(elapsed, Math.floor((Date.now() - startedAtRef.current) / 1000)); setElapsed(finalElapsed);
    const blob = await stopRecorder(); streamRef.current?.getTracks().forEach((track) => track.stop()); streamRef.current = null; stopMeter(); setRecordingReady(false);
    if (blob && blob.size >= 256) {
      const form = new FormData(); form.append("audio", blob, `speaking.${extensionForMime(blob.type)}`); form.append("topic_hint", topicHint);
      try { const localResult = await api<TranscriptionResult>("/api/transcribe", { method: "POST", body: form }); setTranscript(localResult.text); setTranscription(localResult); }
      catch (caught) { const message = caught instanceof Error ? caught.message : "Yerel konuşma algılama tamamlanamadı."; setError(transcript.trim() ? `${message} Tarayıcının çıkardığı metni düzenleyerek devam edebilirsin.` : message); }
    } else if (!transcript.trim()) setError("Ses kaydı oluşmadı. Windows giriş aygıtını ve tarayıcının mikrofon seçimini kontrol edip tekrar dene.");
    chunksRef.current = []; setPhase("review");
  }

  const metrics = useMemo(() => analyseSpeech(transcript, elapsed, transcription), [transcript, elapsed, transcription]);
  const context = result && card ? JSON.stringify({ card: content, transcript, metrics, assessment: result }) : "";
  async function evaluate() {
    if (!card || transcript.trim().length < 5) return; setBusy(true); setError("");
    try { const evaluation = await api<SpeakingResult>("/api/evaluate/speaking", { method: "POST", body: JSON.stringify({ topic: topicHint, transcript, metrics }) }); setResult(evaluation); saveExamProgress({ speaking: { score: evaluation.session_score_20, completedAt: new Date().toISOString() } }); }
    catch (caught) { setError(caught instanceof Error ? caught.message : "Değerlendirilemedi"); } finally { setBusy(false); }
  }
  function restart() {
    speakingActiveRef.current = false; recognitionRef.current?.stop(); recognitionRef.current = null; if (recorderRef.current?.state !== "inactive") recorderRef.current?.stop(); recorderRef.current = null; streamRef.current?.getTracks().forEach((track) => track.stop()); streamRef.current = null; chunksRef.current = []; stopMeter();
    setPhase("pick"); setCard(null); setResult(null); setTranscript(""); setInterim(""); setTranscription(null); setElapsed(0); setPrepLeft(60); setRecordingReady(false); setRecognitionState("waiting"); setHeardAudio(false); setError("");
  }
  const phaseLabel = phase === "prep" ? "Hazırlık" : phase === "speak" ? "Konuşma" : phase === "processing" ? "Yazıya çevriliyor" : "Tamamlandı";

  return <div className="space-y-8">
    <header className="space-y-3"><div className="flex flex-wrap gap-2"><span className="badge badge-navy">3. oturum · 20 puan</span><span className="badge">yaklaşık 10 dakika</span></div><h1 className="font-serif text-4xl text-[var(--navy)]">Konuşma</h1><p className="prose-quiet max-w-3xl">Konu kartını seç, bir dakika hazırlan, ana maddeleri ve takip sorularını konuş. Ses yalnızca yazıya çevrilmek için geçici olarak yerel API’ye gönderilir; işlem tamamlanınca ses dosyası silinir.</p></header>

    {phase === "pick" ? <section className="card overflow-hidden"><div className="relative grid min-h-72 place-items-center overflow-hidden bg-[linear-gradient(160deg,rgba(28,61,90,.08),rgba(176,139,63,.12))] p-6 text-center"><div className="pointer-events-none absolute inset-x-0 top-1/2 h-px bg-[var(--gold)] opacity-50" /><div className={`relative w-full max-w-xl rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-8 shadow-lg ${rolling ? "pulse-soft" : ""}`}><p className="eyebrow">Konu seçimi</p><p className="mt-3 font-serif text-3xl leading-tight text-[var(--navy)]">{rollingTitle}</p><button type="button" className="btn btn-primary mt-6" onClick={() => void pickCard()} disabled={rolling || !cards.length}>{rolling ? "Konular akıyor…" : card ? "Başka konu seç" : "Konu kartını çek"}</button>{card && !rolling ? <button type="button" className="btn btn-outline ml-2 mt-6" onClick={() => { setPrepLeft(60); setPhase("prep"); }}>Bu konuyla başla</button> : null}</div></div></section> : null}

    {card && phase !== "pick" ? <section className="grid gap-4 lg:grid-cols-[0.7fr_0.3fr]"><div className="card p-6 sm:p-8"><p className="eyebrow">Konu kartı</p><h2 className="mt-3 font-serif text-3xl leading-tight text-[var(--navy)]">{content?.prompt}</h2><ul className="prose-quiet mt-5 space-y-2">{content?.bullets?.map((item, index) => <li key={index}>— {item}</li>)}</ul><div className="mt-6 border-t border-[var(--line)] pt-5"><p className="eyebrow">Takip soruları</p><ul className="mt-3 space-y-2 text-sm leading-6">{content?.followups?.map((item, index) => <li key={index}>{index + 1}. {item}</li>)}</ul></div></div><aside className="card flex flex-col items-center justify-center p-6 text-center"><p className="eyebrow">{phaseLabel}</p><p className="mt-2 font-serif text-5xl text-[var(--navy)]">{phase === "prep" ? fmt(prepLeft) : showTimer ? fmt(elapsed) : "••:••"}</p>{phase !== "prep" ? <button type="button" className="btn btn-quiet mt-2 text-xs" onClick={() => setShowTimer((value) => !value)}>{showTimer ? "Süreyi gizle" : "Süreyi göster"}</button> : null}{phase === "prep" ? <button type="button" className="btn btn-outline mt-5" onClick={beginSpeaking}>Hazırım, konuşmayı başlat</button> : null}{phase === "speak" ? <><span className={`mt-4 inline-flex items-center gap-2 text-sm ${recordingReady ? "text-[var(--terracotta)]" : "text-[var(--ink-2)]"}`}><i className={`h-2.5 w-2.5 rounded-full ${recordingReady ? "bg-[var(--terracotta)] pulse-soft" : "bg-[var(--ink-3)]"}`} />{recordingReady ? "kayıt sürüyor" : "mikrofon bekleniyor"}</span><button type="button" className="btn btn-primary mt-5" onClick={() => void finish()}>Konuşmayı bitir</button></> : null}{phase === "processing" ? <span className="badge badge-gold mt-5 pulse-soft">yerel model çalışıyor…</span> : null}</aside></section> : null}

    {phase === "speak" ? <section className="card p-5"><div className="flex flex-wrap items-center justify-between gap-2"><p className="eyebrow">Canlı metin</p><span className={recognitionState === "live" ? "badge badge-green" : "badge badge-gold"}>{recognitionState === "live" ? "canlı algılama açık" : recognitionState === "fallback" ? "final yerel algılama hazır" : "algılama başlatılıyor"}</span></div><div className="mt-4"><div className="flex items-center justify-between text-xs"><span className="text-[var(--ink-2)]">Mikrofon sinyali</span><span className={heardAudio ? "text-[var(--green)]" : "text-[var(--terracotta)]"}>{heardAudio ? "ses geliyor" : elapsed > 4 ? "ses algılanmıyor" : "dinleniyor…"}</span></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-[var(--line)]"><div className="h-full rounded-full bg-[var(--green)] transition-[width] duration-100" style={{ width: `${Math.max(2, Math.round(inputLevel * 100))}%` }} /></div>{elapsed > 4 && !heardAudio ? <p className="mt-2 text-xs text-[var(--terracotta)]">Windows’ta doğru giriş aygıtının seçili ve mikrofonun sessizde olmadığını kontrol et.</p> : null}</div><p className="mt-3 min-h-20 text-sm leading-7 text-[var(--ink-2)]">{transcript} <span className="opacity-50">{interim}</span></p>{recognitionState === "fallback" ? <p className="mt-2 text-xs text-[var(--ink-3)]">Canlı metin görünmeyebilir; ses kaydı konuşmayı bitirdiğinde yerel modelle yazıya çevrilecek.</p> : null}</section> : null}
    {phase === "processing" ? <section className="card p-6 text-center"><p className="font-serif text-2xl text-[var(--navy)]">Konuşman yazıya çevriliyor</p><p className="prose-quiet mt-2 text-sm">İlk kullanımda model hazırlanırken biraz uzun sürebilir. Bu sayfayı kapatma.</p></section> : null}

    {phase === "review" ? <section className="card p-6"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="eyebrow">Algılanan konuşma</p><p className="mt-1 text-xs text-[var(--ink-2)]">{metrics.word_count} kelime · {fmt(metrics.duration_sec)} · yaklaşık {metrics.speech_rate_wpm} kelime/dk</p></div><button type="button" className="btn btn-outline" onClick={restart}>Yeni kart</button></div>{transcription?.audio_deleted ? <p className="mt-4 rounded-xl border border-[rgba(47,107,81,.25)] bg-[rgba(47,107,81,.07)] p-3 text-xs text-[var(--green)]">Yerel transkripsiyon tamamlandı; geçici ses dosyası silindi.</p> : null}{transcription ? <div className="mt-4 grid gap-2 rounded-xl border border-[var(--line)] bg-[rgba(176,139,63,.07)] p-4 sm:grid-cols-2 lg:grid-cols-4"><div><p className="eyebrow">Dolgu sesi</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{metrics.filler_count}</p><p className="text-xs text-[var(--ink-2)]">{Object.entries(metrics.filler_words).map(([word, count]) => `${word} ×${count}`).join(", ") || "um/uh/hmm yok"}</p></div><div><p className="eyebrow">Tereddüt</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{metrics.hesitation_pause_count}</p><p className="text-xs text-[var(--ink-2)]">0,45–1,2 sn kısa duraklama</p></div><div><p className="eyebrow">Tekrar / uzatma</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{metrics.word_repetition_count} / {metrics.elongation_count}</p><p className="text-xs text-[var(--ink-2)]">kelime tekrarı / uzun dolgu</p></div><div><p className="eyebrow">Belirsiz söyleyiş</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{metrics.unclear_word_count}</p><p className="text-xs text-[var(--ink-2)]">düşük güvenli kelime</p></div></div> : null}<textarea className="input mt-4 min-h-44 leading-7" value={transcript} onChange={(event) => setTranscript(event.target.value)} placeholder="Algılanan metin burada görünür. Gerekirse değerlendirmeden önce düzeltebilirsin." /><p className="mt-2 text-xs text-[var(--ink-3)]">Dolgu ve geveleme verileri kelime zamanları ile model güveninden yaklaşık hesaplanır; geri bildirimde eğilim olarak kullanılır, kesin telaffuz ölçümü değildir.</p><button type="button" className="btn btn-primary mt-4" disabled={busy || transcript.trim().length < 5} onClick={() => void evaluate()}>{busy ? "Konuşma inceleniyor…" : "Konuşmamı değerlendir"}</button></section> : null}
    {error ? <p className="rounded-xl border border-[var(--terracotta)] p-4 text-sm text-[var(--terracotta)]">{error}</p> : null}

    {result ? <section className="space-y-5"><div className="card grid gap-5 p-6 md:grid-cols-[0.35fr_0.65fr]"><div><p className="eyebrow">Çalışma puanı</p><p className="mt-2 font-serif text-5xl text-[var(--navy)]">{result.session_score_20}<span className="text-xl text-[var(--ink-3)]">/20</span></p><MarkdownText className="prose-quiet mt-3 text-sm">{result.level_summary_tr}</MarkdownText></div><div className="grid gap-3 sm:grid-cols-2">{Object.entries(result.scores).map(([key, value]) => <div key={key} className="rounded-xl border border-[var(--line)] p-4"><p className="text-xs text-[var(--ink-2)]">{scoreLabels[key] ?? key}</p><p className="mt-1 font-serif text-2xl text-[var(--navy)]">{value}<span className="text-sm text-[var(--ink-3)]">/2.5</span></p></div>)}</div></div><div className="grid gap-4 md:grid-cols-2"><div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Puan kaybettiren noktalar</h2><ol className="mt-3 space-y-2 text-sm leading-6">{result.priorities_tr.map((item, index) => <li key={index} className="flex gap-2"><span>{index + 1}.</span><MarkdownText>{item}</MarkdownText></li>)}</ol><MarkdownText className="mt-4 rounded-xl bg-[rgba(176,139,63,.1)] p-3 text-sm">{result.filler_feedback_tr}</MarkdownText></div><div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Bir sonraki antrenman</h2><ul className="mt-3 space-y-2 text-sm leading-6">{result.next_drill_tr.map((item, index) => <li key={index} className="flex gap-2"><span>—</span><MarkdownText>{item}</MarkdownText></li>)}</ul></div></div>{result.better_phrases.length ? <div className="card p-6"><h2 className="font-serif text-xl text-[var(--navy)]">Daha iyi ifade et</h2><div className="mt-4 grid gap-3 md:grid-cols-2">{result.better_phrases.map((item, index) => <div key={index} className="rounded-xl border border-[var(--line)] p-4 text-sm"><MarkdownText className="text-[var(--terracotta)]">{item.instead_of}</MarkdownText><MarkdownText className="mt-1 font-medium text-[var(--green)]">{`→ ${item.try}`}</MarkdownText><MarkdownText className="prose-quiet mt-2 text-xs">{item.why_tr}</MarkdownText></div>)}</div></div> : null}<MarkdownText className="text-xs text-[var(--ink-3)]">{result.disclaimer_tr}</MarkdownText><div className="flex flex-wrap gap-3"><Link href="/exam" className="btn btn-primary">Sınav merkezi puanlarını gör</Link><button type="button" className="btn btn-outline" onClick={restart}>Yeni speaking oturumu</button></div><Coach context={context} /></section> : null}
  </div>;
}
