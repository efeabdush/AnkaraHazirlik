# Hazırlık Prep

Unofficial B1+ practice tool for the [Ankara University](https://yabdil.ankara.edu.tr/ingilizce-hazirlik-ornek-yeterlik-muafiyet-sinavlari/) English proficiency / exemption exam.

**Not affiliated with Ankara University School of Foreign Languages.**

Visitors can practise every session separately or complete a three-session mock exam. Only the site owner generates new tests (hidden admin panel). Nobody pastes an API key in the browser.

## Exam shape

| Session | Skills | Points |
| --- | --- | --- |
| 1 | Listening, Reading, Use of English | 60 |
| 2 | Writing | 20 |
| 3 | Speaking | 20 |

The current MVP includes the complete 100-point structure: Listening, Reading, Use of English, a 250+ word Writing task, and topic-card Speaking practice. The browser keeps the three session scores together on the exam hub. Writing and speaking feedback is an AI estimate, not an official score.

Speaking audio is held in browser memory while the activity is running, then sent to the local backend only for transcription. The backend deletes the temporary audio file immediately after transcription (including failed attempts); only the resulting transcript and speaking metrics are sent for AI feedback. Microphone tracks are stopped when the activity finishes or the page closes.

## Quick start

Windows: proje klasöründe `baslat.bat` dosyasına çift tıkla. **Tek** siyah pencere açılır; API ve site arka planda çalışır, tarayıcı ana sayfayı açar. Durdurmak için o pencerede `Ctrl+C` bas — hepsi kapanır. Günde bir kez açman yeter. Kod değişse bile API kendini yeniler. Admin’den yeni test üretince yeniden başlatmana gerek yok.

```bash
# elle baslatmak istersen:
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# other terminal
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Admin: [http://localhost:3000/admin](http://localhost:3000/admin).

İlk kurulum (bir kez):

```bash
cp .env.example .env
# set ADMIN_SECRET, then paste ONE provider key (see "AI providers" below)

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cd ../frontend
npm install
```

Or: `docker compose up`.

## AI providers

The site owner pays for the model; visitors never enter a key. Fill one variable in `.env`, then pick the model from a dropdown in `/admin`. The choice is stored in the database and survives restarts.

| Provider | Env var | Notes |
| --- | --- | --- |
| OpenCode Go | `OPENCODE_API_KEY` | Subscription. Open-weight models (Grok, GLM, Kimi, DeepSeek). |
| OpenCode Zen | `OPENCODE_API_KEY` | Pay-per-use. Full catalog including GPT and Claude. |
| OpenRouter | `OPENROUTER_API_KEY` | Uses your credit. 400+ models. |
| Google Gemini | `GEMINI_API_KEY` | Optional fallback. |

Model lists are fetched live from each provider, so new models appear without a code change.

## Turkish help on the results page

After a student submits answers, every English string on the results page is selectable. Clicking one word gives that word alone; dragging over a phrase gives the phrase; selecting a full line gives one natural Turkish sentence. Nothing calls a model at selection time.

Three precomputed layers back it, checked in order:

1. phrase and sentence entries stored per test (`tests.glossary_json`)
2. a word bank the generator produced for words the shared dictionary was missing
3. `content/dictionary/en_tr_core.json`, the shared word list

Word lookups fall back through plural and tense forms (`machines` → `machine`, `relinked` → `relink`), and a single word never resolves to the sentence containing it. Unknown word groups are read word by word instead of returning nothing.

For an older test with no pack, press **Türkçe paket** in `/admin`. `python -m pytest -q` in `backend` and `npm run check:glossary` in `frontend` assert that both engines resolve every word, option, rationale, and transcript line in the seed tests.

## Stack

- Frontend: Next.js, TypeScript, Tailwind
- Backend: FastAPI, SQLite, edge-tts

## License

MIT. Do not open PRs that dump official exam PDFs or answer keys.
