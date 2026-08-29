import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2] / "content" / "seeds"


def texts(pack):
    out = [pack["title"]]
    for line in pack["script"]:
        out.append(line["text"])
    for q in pack["questions"]:
        out.append(q["stem"])
        out.append(q.get("rationale", ""))
        out.extend(q["options"].values())
    for n in pack.get("note_scaffold") or []:
        out.append(n)
    return out


words = {}
for path in sorted(root.glob("*.json")):
    if path.name.endswith(".glossary.json"):
        continue
    pack = json.loads(path.read_text(encoding="utf-8"))
    for t in texts(pack):
        for w in re.findall(r"[A-Za-z][A-Za-z'’\-]*", t):
            key = w.replace("’", "'").lower()
            words[key] = words.get(key, 0) + 1

print(len(words))
print(json.dumps(sorted(words), ensure_ascii=False))
