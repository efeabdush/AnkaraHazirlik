import { lookup } from "../src/lib/glossary.ts";
import fs from "node:fs";
import path from "node:path";

const seeds = path.join(process.cwd(), "..", "content", "seeds");
const core = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), "..", "content", "dictionary", "en_tr_core.json"), "utf8"),
);

let failures = 0;
function check(name: string, ok: boolean, extra = "") {
  if (!ok) {
    failures += 1;
    console.error(`FAIL ${name} ${extra}`);
  }
}

for (const name of ["conversation_laundry", "lecture_sleep"]) {
  const pack = JSON.parse(fs.readFileSync(path.join(seeds, `${name}.json`), "utf8"));
  const rawGloss = JSON.parse(fs.readFileSync(path.join(seeds, `${name}.glossary.json`), "utf8"));
  const entries = Array.isArray(rawGloss) ? rawGloss : rawGloss.entries;
  const packWords: Record<string, string> = Array.isArray(rawGloss) ? {} : rawGloss.words ?? {};
  const words = { ...core, ...packWords };

  const texts: string[] = [pack.title];
  for (const line of pack.script) texts.push(line.text);
  for (const q of pack.questions) {
    texts.push(q.stem, q.rationale ?? "", ...Object.values(q.options as Record<string, string>));
  }

  const unique = new Set<string>();
  for (const t of texts) for (const w of t.match(/[A-Za-z][A-Za-z'’\-]*/g) ?? []) unique.add(w.toLowerCase());
  for (const w of unique) {
    const hit = lookup(entries, w, words);
    check(`${name}:word:${w}`, !!hit && (hit.kind === "word" || hit.kind === "phrase"), JSON.stringify(hit));
  }
  for (const t of texts) {
    check(`${name}:sentence`, !!lookup(entries, t, words), t.slice(0, 50));
  }
}

const pack = JSON.parse(fs.readFileSync(path.join(seeds, "lecture_sleep.json"), "utf8"));
void pack;
const lectureGloss = JSON.parse(fs.readFileSync(path.join(seeds, "lecture_sleep.glossary.json"), "utf8"));
const lectureEntries = Array.isArray(lectureGloss) ? lectureGloss : lectureGloss.entries;
check("phrase:REM sleep", lookup(lectureEntries, "REM sleep", core)?.tr === "REM uykusu");
check("phrase:more important", lookup(lectureEntries, "more important", core)?.tr === "daha önemli");
const wordByWord = lookup(lectureEntries, "students sleep badly", core);
check("wordByWord", wordByWord?.kind === "words" && wordByWord.parts?.length === 3, JSON.stringify(wordByWord));
check("trailingPunct", lookup([], "lecture.", core)?.tr === "ders / konferans");

console.log(failures ? `${failures} failing checks` : "frontend glossary checks passed");
process.exit(failures ? 1 : 0);
