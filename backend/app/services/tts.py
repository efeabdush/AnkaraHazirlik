from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import edge_tts


VOICES = {
    "student": "en-US-JennyNeural",
    "staff": "en-US-GuyNeural",
    "lecturer": "en-GB-SoniaNeural",
}


async def _save(text: str, voice: str, dest: Path) -> None:
    communicate = edge_tts.Communicate(text, voice=voice, rate="-5%")
    await communicate.save(str(dest))


async def _render(script: list[dict], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = dest.parent / f"{dest.stem}_parts"
    tmp_dir.mkdir(exist_ok=True)
    parts: list[Path] = []
    for i, line in enumerate(script):
        speaker = line.get("speaker", "lecturer")
        voice = VOICES.get(speaker, VOICES["lecturer"])
        path = tmp_dir / f"{i:03d}.mp3"
        await _save(line["text"], voice, path)
        parts.append(path)
    with dest.open("wb") as out:
        for part in parts:
            out.write(part.read_bytes())
    for f in tmp_dir.iterdir():
        f.unlink()
    tmp_dir.rmdir()


def synthesize_script(script: list[dict], dest: Path) -> int:
    """Write concatenated mp3. Returns approximate duration seconds."""

    def runner() -> None:
        asyncio.run(_render(script, dest))

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        runner()
    else:
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(runner).result()

    words = sum(len(line["text"].split()) for line in script)
    return max(30, int(words / 2.3))
