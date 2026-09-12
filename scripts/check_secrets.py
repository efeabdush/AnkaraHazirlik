"""Fail when Git-tracked files contain likely credentials or private files."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SELF = "scripts/check_secrets.py"

# Keep the token prefixes split so this scanner does not flag its own source.
PATTERNS = {
    "OpenRouter token": re.compile(rb"sk" + rb"-or-v1-[A-Za-z0-9_-]{20,}"),
    "provider token": re.compile(rb"(?<![A-Za-z0-9])sk" + rb"-(?!or-v1-)[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(rb"gh" + rb"[pousr]_[A-Za-z0-9_]{20,}"),
    "Resend token": re.compile(rb"re" + rb"_[A-Za-z0-9_]{20,}"),
    "AWS access key": re.compile(rb"AK" + rb"IA[0-9A-Z]{16}"),
    "Google API key": re.compile(rb"AI" + rb"za[0-9A-Za-z_-]{30,}"),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "literal credential assignment": re.compile(
        rb"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"']"
        rb"[A-Za-z0-9_./+=-]{24,}[\"']"
    ),
}

SAFE_ENV_FILES = {".env.example", ".env.sample"}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".db", ".sqlite", ".sqlite3"}


def tracked_files() -> list[str]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [item.decode("utf-8") for item in output.split(b"\0") if item]


def private_filename(path: str) -> bool:
    posix = PurePosixPath(path)
    name = posix.name.lower()
    if name == ".env" or (name.startswith(".env.") and name not in SAFE_ENV_FILES):
        return True
    if posix.suffix.lower() in PRIVATE_SUFFIXES:
        return True
    return name.startswith("credentials") and name.endswith(".json")


def main() -> int:
    findings: list[str] = []
    for relative in tracked_files():
        source = ROOT / relative
        # A locally deleted tracked file is not part of the next commit.
        if not source.is_file():
            continue
        if private_filename(relative):
            findings.append(f"{relative}: private filename")

        if relative == SELF:
            continue
        data = source.read_bytes()
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                line = data.count(b"\n", 0, match.start()) + 1
                findings.append(f"{relative}:{line}: {label}")

    if findings:
        print("Potential secrets found (values intentionally hidden):")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Secret scan passed: no likely credentials in tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
