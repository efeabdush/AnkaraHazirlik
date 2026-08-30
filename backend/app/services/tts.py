from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import edge_tts


VOICES = {
    "student": "en-US-JennyNeural",
    "staff": "en-US-GuyNeural",
    "friend": "en-US-AriaNeural",
    "teacher": "en-GB-RyanNeural",
    "lecturer": "en-GB-SoniaNeural",
    "announcer": "en-US-EricNeural",
}

RATE_BY_LEVEL = {"A1": "-18%", "A2": "-12%", "B1": "-6%", "B1+": "-2%"}


async def _save(text: str, voice: str, dest: Path, rate: str = "-5%") -> None:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(str(dest))


async def _render(script: list[dict], dest: Path, rate: str = "-5%") -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = dest.parent / f"{dest.stem}_parts"
    tmp_dir.mkdir(exist_ok=True)
    parts: list[Path] = []
    for i, line in enumerate(script):
        speaker = line.get("speaker", "lecturer")
        voice = VOICES.get(speaker, VOICES["lecturer"])
        path = tmp_dir / f"{i:03d}.mp3"
        await _save(line["text"], voice, path, rate)
        parts.append(path)
    with dest.open("wb") as out:
        for part in parts:
            out.write(part.read_bytes())
    for f in tmp_dir.iterdir():
        f.unlink()
    tmp_dir.rmdir()


def estimate_seconds(script: list[dict], level: str | None = None) -> int:
    words = sum(len(str(line.get("text") or "").split()) for line in script)
    if level:
        per_second = {"A1": 1.9, "A2": 2.1, "B1": 2.3, "B1+": 2.5}.get(level, 2.2)
        return max(6, round(words / per_second))
    return max(30, int(words / 2.3))


def synthesize_script(script: list[dict], dest: Path, level: str | None = None) -> int:
    """Write concatenated mp3. Returns approximate duration seconds."""

    def runner() -> None:
        asyncio.run(_render(script, dest, RATE_BY_LEVEL.get(level, "-5%")))

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        runner()
    else:
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(runner).result()

    return estimate_seconds(script, level)
