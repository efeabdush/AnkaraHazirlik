from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache

from .llm import complete, parse_json_object

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
EDGE_PUNCT = " \t\n\"'“”‘’()[]{}.,;:!?…-–—"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def clean_selection(text: str) -> str:
    return normalize(text).strip(EDGE_PUNCT)


def _word_forms(word: str) -> list[str]:
    """Candidate dictionary keys for one selected word, most specific first."""
    w = word.strip(EDGE_PUNCT)
    forms = [w]
    if w.endswith("'s"):
        forms.append(w[:-2])
    if w.endswith("s'"):
        forms.append(w[:-2])
    if len(w) > 3 and w.endswith("ies"):
        forms.append(w[:-3] + "y")
    if len(w) > 3 and w.endswith("es"):
        forms.append(w[:-2])
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        forms.append(w[:-1])
    if len(w) > 4 and w.endswith("ing"):
        forms.append(w[:-3])
        forms.append(w[:-3] + "e")
    if len(w) > 3 and w.endswith("ed"):
        forms.append(w[:-2])
        forms.append(w[:-1])
        forms.append(w[:-2] + "e")
    if len(w) > 4 and w.endswith("ly"):
        forms.append(w[:-2])
    # stopped -> stop, planning -> plan
    for f in list(forms):
        if len(f) > 2 and f[-1] == f[-2] and f[-1].isalpha():
            forms.append(f[:-1])
    out: list[str] = []
    for f in forms:
        if f and f not in out:
            out.append(f)
    return out


@lru_cache(maxsize=1)
def core_dictionary() -> dict[str, str]:
    from ..config import settings

    path = settings.content_dir / "dictionary" / "en_tr_core.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {normalize(k): str(v) for k, v in data.items() if str(v).strip()}


def word_gloss(word: str, extra: dict[str, str] | None = None) -> str | None:
    key = normalize(word)
    banks = [extra or {}, core_dictionary()]
    for form in _word_forms(key):
        for bank in banks:
            hit = bank.get(form)
            if hit:
                return hit
    return None


def lookup(
    entries: list[dict],
    selected: str,
    words: dict[str, str] | None = None,
) -> dict | None:
    """Resolve a mouse selection with precomputed data only.

    A single word never resolves to the sentence that contains it; it resolves
    through the word bank. A multi-word selection prefers an exact phrase or
    sentence entry, then falls back to a word-by-word reading.
    """
    needle = clean_selection(selected)
    if not needle:
        return None

    bank = {normalize(k): v for k, v in (words or {}).items() if str(v).strip()}
    cleaned = [e for e in (_clean_entry(x) for x in entries) if e]
    by_key: dict[str, str] = {}
    for e in cleaned:
        by_key.setdefault(clean_selection(e["en"]), e["tr"])

    tokens = WORD_RE.findall(needle)

    exact = by_key.get(needle)
    if exact:
        return {"en": selected.strip(), "tr": exact, "kind": "phrase" if len(tokens) > 1 else "word"}

    if len(tokens) <= 1:
        gloss = word_gloss(needle, bank)
        if gloss:
            return {"en": selected.strip(), "tr": gloss, "kind": "word"}
        short = [
            e
            for e in cleaned
            if len(WORD_RE.findall(clean_selection(e["en"]))) <= 3 and needle in clean_selection(e["en"])
        ]
        if short:
            short.sort(key=lambda e: len(clean_selection(e["en"])))
            return {"en": short[0]["en"], "tr": short[0]["tr"], "kind": "phrase"}
        return None

    covering = sorted(
        (e for e in cleaned if needle in clean_selection(e["en"])),
        key=lambda e: len(clean_selection(e["en"])),
    )
    for e in covering:
        hay = clean_selection(e["en"])
        if len(needle) / len(hay) >= 0.8:
            return {"en": e["en"], "tr": e["tr"], "kind": "sentence"}

    parts: list[dict] = []
    for token in tokens:
        gloss = word_gloss(token, bank)
        parts.append({"en": token, "tr": gloss or "?"})
    known = [p for p in parts if p["tr"] != "?"]
    if not known:
        return None
    return {
        "en": selected.strip(),
        "tr": " · ".join(p["tr"] for p in known),
        "kind": "words",
        "parts": parts,
    }


def _clean_entry(raw: dict) -> dict | None:
    en = str(raw.get("en") or "").strip()
    tr = str(raw.get("tr") or "").strip()
    if len(en) < 2 or not tr:
        return None
    return {"en": en, "tr": tr}


def merge_entries(*groups: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for group in groups:
        for raw in group:
            item = _clean_entry(raw)
            if not item:
                continue
            key = normalize(item["en"])
            if key in seen:
                continue
            seen.add(key)
            out.append(item)
    out.sort(key=lambda e: len(normalize(e["en"])), reverse=True)
    return out


def pack_texts(pack: dict) -> list[str]:
    out: list[str] = [str(pack.get("title") or "")]
    for line in pack.get("script") or []:
        out.append(str(line.get("text") or ""))
    for q in pack.get("questions") or []:
        out.append(str(q.get("stem") or ""))
        out.append(str(q.get("rationale") or ""))
        options = q.get("options") or {}
        if isinstance(options, dict):
            out.extend(str(v) for v in options.values())
    scaffold = pack.get("note_scaffold")
    if isinstance(scaffold, list):
        out.extend(str(s) for s in scaffold)
    return [t for t in out if t.strip()]


def pack_words(pack: dict) -> list[str]:
    seen: list[str] = []
    known: set[str] = set()
    for text in pack_texts(pack):
        for word in WORD_RE.findall(normalize(text)):
            if word not in known:
                known.add(word)
                seen.append(word)
    return seen


def word_bank_for(pack: dict, extra: dict[str, str] | None = None) -> dict[str, str]:
    """Only the words this pack actually uses, so the client payload stays small."""
    bank: dict[str, str] = {}
    for word in pack_words(pack):
        gloss = word_gloss(word, extra)
        if gloss:
            bank[word] = gloss
    return bank


def missing_words(pack: dict, extra: dict[str, str] | None = None) -> list[str]:
    return [w for w in pack_words(pack) if not word_gloss(w, extra)]


def pack_from_test(test) -> dict:
    import json as _json

    return {
        "title": test.title,
        "script": _json.loads(test.transcript_json or "[]"),
        "questions": [
            {
                "stem": q.stem,
                "options": _json.loads(q.options_json),
                "rationale": q.rationale,
            }
            for q in test.questions
        ],
    }


def local_glossary(pack: dict) -> dict:
    """Word pack that does not call a model. Sentence entries stay empty."""
    return {"entries": [], "words": word_bank_for(pack)}


def merge_glossary(*packs: dict) -> dict:
    entries: list[dict] = []
    words: dict[str, str] = {}
    for pack in packs:
        entries.extend(pack.get("entries") or [])
        for k, v in (pack.get("words") or {}).items():
            key = normalize(str(k))
            if key and str(v).strip():
                words.setdefault(key, str(v).strip())
    return {"entries": merge_entries(entries), "words": words}


def _ingest_words(raw: dict, dest: dict[str, str]) -> None:
    for k, v in (raw or {}).items():
        key = normalize(str(k))
        if key and str(v).strip() and WORD_RE.fullmatch(key):
            dest.setdefault(key, str(v).strip())


def _prompt(name: str) -> str:
    from ..config import settings

    return (settings.content_dir / "prompts" / name).read_text(encoding="utf-8")


def _llm_entries_for(texts: list[str]) -> list[dict]:
    texts = [t for t in texts if str(t).strip()]
    if not texts:
        return []
    raw = complete(
        _prompt("glossary_batch.txt"),
        json.dumps({"translate_exactly": texts}, ensure_ascii=False),
        json_mode=True,
    )
    data = parse_json_object(raw)
    blob = normalize(" \n ".join(texts))
    return [e for e in (data.get("entries") or []) if normalize(str(e.get("en") or "")) in blob]


def _llm_words_for(words: list[str]) -> dict[str, str]:
    if not words:
        return {}
    raw = complete(
        _prompt("glossary_words.txt"),
        json.dumps({"words_needing_turkish": words}, ensure_ascii=False),
        json_mode=True,
    )
    data = parse_json_object(raw)
    out: dict[str, str] = {}
    _ingest_words(data.get("words") or {}, out)
    return out


def generate_glossary(pack: dict) -> dict:
    """Build a Turkish pack. Always includes the local word bank; LLM adds sentences."""
    built = local_glossary(pack)
    entries: list[dict] = list(built["entries"])
    words: dict[str, str] = dict(built["words"])
    errors: list[str] = []

    script_texts = [str(line.get("text") or "") for line in pack.get("script") or []]
    question_texts: list[str] = []
    if pack.get("title"):
        question_texts.append(str(pack["title"]))
    for q in pack.get("questions") or []:
        question_texts.append(str(q.get("stem") or ""))
        question_texts.append(str(q.get("rationale") or ""))
        options = q.get("options") or {}
        if isinstance(options, dict):
            question_texts.extend(str(v) for v in options.values())

    for batch in _chunks(script_texts + question_texts, 6):
        try:
            entries.extend(_llm_entries_for(batch))
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc)[:240])
            print(f"Glossary sentence batch skipped: {exc}")

    for batch in _chunks(missing_words(pack, words), 40):
        try:
            _ingest_words(_llm_words_for(batch), words)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc)[:240])
            print(f"Glossary word batch skipped: {exc}")

    result = {"entries": merge_entries(entries), "words": words}
    if errors and not result["entries"]:
        result["warning"] = errors[0]
    return result


def _chunks(items: list, size: int) -> list[list]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def run_glossary_job(db, job_id: str) -> None:
    from ..models import GenerationJob, Test

    job = db.get(GenerationJob, job_id)
    if not job:
        return
    test = db.get(Test, job.test_id)
    if not test:
        job.status = "failed"
        job.error = "Test yok"
        db.commit()
        return
    try:
        job.status = "glossary"
        db.commit()
        pack = pack_from_test(test)
        built = generate_glossary(pack)
        existing_entries, existing_words = [], {}
        try:
            raw = json.loads(test.glossary_json or "[]")
            if isinstance(raw, dict):
                existing_entries = raw.get("entries") or []
                existing_words = raw.get("words") or {}
            elif isinstance(raw, list):
                existing_entries = raw
        except json.JSONDecodeError:
            pass
        merged = merge_glossary(
            {"entries": existing_entries, "words": existing_words},
            built,
        )
        test.glossary_json = json.dumps(
            {"entries": merged["entries"], "words": merged["words"]},
            ensure_ascii=False,
        )
        job.status = "ready"
        if built.get("warning") and not merged["entries"]:
            job.error = str(built["warning"])[:2000]
        db.commit()
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        job = db.get(GenerationJob, job_id)
        if job:
            job.status = "failed"
            job.error = str(exc)[:2000]
            db.commit()
