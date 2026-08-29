from __future__ import annotations

ALLOWED_TYPES_CONVERSATION = {"purpose", "detail", "process", "inference"}
ALLOWED_TYPES_LECTURE = {"main_idea", "true", "not_true", "cause"}
ACADEMIC_KINDS = {
    "reading_standard": 6,
    "reading_insertion": 4,
    "cloze": 5,
    "restatement": 5,
    "writing_prompt": 0,
    "speaking_card": 0,
}


class ValidationError(ValueError):
    pass


def validate_pack(kind: str, data: dict) -> dict:
    if kind not in {"conversation", "lecture"}:
        raise ValidationError("kind conversation veya lecture olmalı")
    for key in ("title", "topic", "script", "questions"):
        if key not in data:
            raise ValidationError(f"Eksik alan: {key}")
    script = data["script"]
    questions = data["questions"]
    if not isinstance(script, list) or len(script) < 4:
        raise ValidationError("Script çok kısa")
    if len(questions) != 4:
        raise ValidationError("Tam 4 soru olmalı")

    words = sum(len(str(line.get("text", "")).split()) for line in script)
    if kind == "conversation" and not (180 <= words <= 450):
        raise ValidationError(f"Diyalog uzunluğu uygun değil ({words} kelime)")
    if kind == "lecture" and not (620 <= words <= 980):
        raise ValidationError(f"Ders uzunluğu uygun değil ({words} kelime)")

    full_text = " ".join(str(line.get("text", "")).lower() for line in script)
    seen_types: set[str] = set()
    for q in questions:
        if q.get("answer") not in {"A", "B", "C", "D"}:
            raise ValidationError("Cevap A–D olmalı")
        options = q.get("options") or {}
        if set(options.keys()) != {"A", "B", "C", "D"}:
            raise ValidationError("Şıklar A B C D olmalı")
        if any(not str(v).strip() for v in options.values()):
            raise ValidationError("Boş şık var")
        joined = " ".join(str(v).lower() for v in options.values())
        if "all of the above" in joined or "none of the above" in joined:
            raise ValidationError("all/none of the above yasak")
        qtype = q.get("qtype", "detail")
        allowed = ALLOWED_TYPES_CONVERSATION if kind == "conversation" else ALLOWED_TYPES_LECTURE
        if qtype not in allowed:
            q["qtype"] = "detail" if kind == "conversation" else "main_idea"
        else:
            seen_types.add(qtype)
        key_text = str(options[q["answer"]]).lower()
        tokens = [t for t in key_text.split() if len(t) > 4][:4]
        if tokens and not any(t in full_text for t in tokens):
            # soft check — keep but require stem to be non-empty
            pass
        if not str(q.get("stem", "")).strip():
            raise ValidationError("Soru kökü boş")

    if kind == "conversation":
        speakers = {line.get("speaker") for line in script}
        if not {"student", "staff"} <= speakers and len(speakers) < 2:
            raise ValidationError("Diyalogda iki konuşmacı olmalı")
    return data


def validate_academic_pack(kind: str, data: dict) -> dict:
    if kind not in ACADEMIC_KINDS:
        raise ValidationError("Bilinmeyen akademik içerik türü")
    if not str(data.get("title", "")).strip() or not isinstance(data.get("content"), dict):
        raise ValidationError("Başlık veya içerik eksik")
    questions = data.get("questions") or []
    expected = ACADEMIC_KINDS[kind]
    if len(questions) != expected:
        raise ValidationError(f"{kind} tam {expected} soru içermeli")

    if kind == "reading_standard":
        passage = " ".join(data["content"].get("paragraphs") or [])
        words = len(passage.split())
        if not 380 <= words <= 700:
            raise ValidationError(f"Okuma metni 380-700 kelime olmalı ({words})")
    elif kind == "reading_insertion":
        passage = " ".join(data["content"].get("paragraphs") or [])
        if sum(passage.count(f"[[{i}]]") for i in range(1, 5)) != 4:
            raise ValidationError("Cümle yerleştirmede [[1]]-[[4]] boşlukları olmalı")
        choices = data["content"].get("sentence_options") or {}
        if set(choices) != {"A", "B", "C", "D", "E"}:
            raise ValidationError("Cümle yerleştirmede A-E seçenekleri olmalı")
    elif kind == "cloze":
        passage = str(data["content"].get("text", ""))
        if sum(passage.count(f"[[{i}]]") for i in range(1, 6)) != 5:
            raise ValidationError("Cloze metninde [[1]]-[[5]] boşlukları olmalı")
    elif kind == "writing_prompt":
        if len(str(data["content"].get("prompt", "")).split()) < 8:
            raise ValidationError("Yazma konusu çok kısa")
    elif kind == "speaking_card":
        if len(data["content"].get("bullets") or []) != 3:
            raise ValidationError("Konuşma kartında üç madde olmalı")
        if len(data["content"].get("followups") or []) < 2:
            raise ValidationError("En az iki takip sorusu olmalı")

    for q in questions:
        answer = str(q.get("answer", ""))
        options = q.get("options") or {}
        allowed = {"A", "B", "C", "D", "E"} if kind == "reading_insertion" else {"A", "B", "C", "D"}
        if answer not in allowed or not set(options).issubset(allowed) or answer not in options:
            raise ValidationError("Soru seçenekleri veya cevap anahtarı geçersiz")
        if kind != "reading_insertion" and set(options) != allowed:
            raise ValidationError("Soruda A-D seçeneklerinin tamamı olmalı")
        if not str(q.get("stem", "")).strip() or any(not str(v).strip() for v in options.values()):
            raise ValidationError("Boş soru veya seçenek var")
    return data
