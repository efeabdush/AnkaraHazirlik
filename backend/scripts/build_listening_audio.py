"""Pre-render every bundled listening track used by the public practice catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_DIR / "backend"))

from app.services.practice_catalog import build_practice_catalog  # noqa: E402
from app.services.tts import synthesize_script  # noqa: E402


def script_digest(script: list[dict]) -> str:
    payload = json.dumps(script, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def listening_packs() -> list[dict]:
    packs: list[dict] = []
    for path in sorted((REPO_DIR / "content" / "seeds").glob("*.json")):
        if path.name.endswith(".glossary.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("kind") in {"conversation", "lecture"}:
            packs.append(data)
    packs.extend(
        data
        for data in build_practice_catalog()
        if data.get("kind") in {"conversation", "lecture"}
    )
    return packs


def render(pack: dict, output_dir: Path, force: bool, previous_manifest: dict[str, str]) -> tuple[str, str]:
    destination = output_dir / f"{pack['id']}.mp3"
    if destination.exists() and not force and previous_manifest.get(pack["id"]) == script_digest(pack["script"]):
        return pack["id"], "kept"
    synthesize_script(pack["script"], destination)
    return pack["id"], "rendered"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    packs = listening_packs()
    output_dir = REPO_DIR / "content" / "listening" / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    try:
        previous_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        previous_manifest = {}

    # Existing seed tracks are already approved and can be reused without a network call.
    storage_dir = REPO_DIR / "backend" / "storage" / "audio"
    for pack in packs:
        source = storage_dir / f"{pack['id']}.mp3"
        destination = output_dir / source.name
        if source.exists() and not destination.exists() and not args.force:
            shutil.copyfile(source, destination)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [
            pool.submit(render, pack, output_dir, args.force, previous_manifest)
            for pack in packs
        ]
        for completed, future in enumerate(as_completed(futures), start=1):
            track_id, status = future.result()
            print(f"[{completed:02d}/{len(packs):02d}] {status}: {track_id}", flush=True)

    manifest = {pack["id"]: script_digest(pack.get("script") or []) for pack in packs}
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
