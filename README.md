# Ankara Hazırlık

Ankara Üniversitesi İngilizce hazırlık yeterlik / muafiyet sınavının B1+ yapısına göre hazırlanmış, bağımsız ve açık kaynak bir çalışma platformu.

> Bu proje Ankara Üniversitesi veya YABDİL ile bağlantılı değildir. Resmî sınav belgelerini kopyalamaz; yayımlanan sınav yapısını referans alan özgün pratik içerikleri kullanır.

## Neler var?

- Dinleme: kısa diyaloglar ve not almalı akademik dersler
- Okuma: standart pasajlar ve cümle yerleştirme
- Dil kullanımı: cloze text ve restatement
- Yazma: 250+ kelimelik opinion essay ve AI geri bildirimi
- Konuşma: konu kartları, yerel ses-yazı dönüşümü ve AI koçu
- Akış: A1–B1+ seviyelerinde kısa, kaydırmalı çalışmalar
- Üretim paneli: kendi AI anahtarınla yeni özgün içerik üretme ve yayımlama

Hazır soru ve ses havuzu repoya dahildir. AI anahtarı olmadan test çözme bölümleri çalışır; açıklama, üretim, yazma ve konuşma değerlendirmesi gibi AI özellikleri için kendi sağlayıcı anahtarın gerekir.

## En kolay kurulum — Windows

Gerekenler:

- [Python 3.13](https://www.python.org/downloads/)
- [Node.js 22 LTS](https://nodejs.org/)
- Git

İlk kurulumda PowerShell açıp proje klasöründe şunları çalıştır:

```powershell
Copy-Item .env.example .env

python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt

Set-Location frontend
npm install
Set-Location ..
```

Sonraki açılışlarda yalnızca `baslat.bat` dosyasına çift tıkla. Site otomatik olarak [http://localhost:3000](http://localhost:3000) adresinde açılır.

Üst menüde **Yönetim** bağlantısı görünür. Yerel kurulumda `/admin` şifre istemeden açılır. Bu kolaylık yalnızca aynı bilgisayardan gelen localhost isteklerinde geçerlidir; production ortamında panel `ADMIN_SECRET` ister.

## macOS / Linux

```bash
cp .env.example .env

python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt

cd frontend
npm install
npm run dev
```

İkinci terminalde:

```bash
cd backend
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Docker ile çalıştırma

```bash
cp .env.example .env
docker compose up --build
```

Portlar yalnızca `127.0.0.1` adresine bağlanır. Docker içindeki ağ yönlendirmesine göre yönetim paneli `ADMIN_SECRET` isteyebilir; böyle bir durumda `.env` dosyasına uzun bir değer yazıp panelde aynı değeri kullan.

## Kendi AI anahtarını bağlama

Yerelde [http://localhost:3000/admin](http://localhost:3000/admin) adresini aç. Desteklenen sağlayıcılardan birinin anahtarını yapıştır, **Test et ve kaydet** de, ardından listeden modeli seç.

| Sağlayıcı | Ortam değişkeni |
| --- | --- |
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenCode Go / Zen | `OPENCODE_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |

Anahtarlar tarayıcıdaki öğrenci arayüzüne gönderilmez. Yerel panelden kaydedilen anahtar SQLite veritabanında tutulur; bu dosya Git tarafından izlenmez. İstersen anahtarı doğrudan `.env` içine de ekleyebilirsin.

## Projeyi değiştirmek

```text
frontend/src/app/         sayfalar ve rotalar
frontend/src/components/  arayüz bileşenleri
backend/app/routers/      API uçları
backend/app/services/     üretim, doğrulama, TTS ve AI işlemleri
content/seeds/            başlangıç testleri
content/akis/             kısa Akış içerikleri ve sesleri
content/prompts/          içerik üretim talimatları
```

Yeni bir yön vermek için repoyu forkla, `.env.example` dosyasını `.env` olarak kopyala ve kendi içeriklerini / promptlarını düzenle. Resmî sınav PDF’lerini, cevap anahtarlarını veya başkasına ait materyalleri repoya ekleme.

## Teknik yapı

- Next.js 16, React 19, TypeScript, Tailwind CSS
- FastAPI, SQLAlchemy, SQLite
- faster-whisper ile yerel speech-to-text
- edge-tts ile ses üretimi
- OpenRouter, OpenCode ve Gemini sağlayıcı desteği
- Pytest, ESLint, TypeScript ve GitHub Actions CI

Sınav oturumları 100 puanlık yapıyı izler: ilk oturum dinleme + okuma + dil kullanımı (60), ikinci oturum yazma (20), üçüncü oturum konuşma (20). AI puanları çalışma amaçlı tahmindir; resmî sonuç değildir.

## Testler

```bash
cd backend
python -m pytest -q

cd ../frontend
npm run lint
npx tsc --noEmit
npm run check:glossary
npm run build
```

## Production güvenliği

İnternete açmadan önce en az şunları yap:

- `APP_ENV=production` ve uzun, rastgele bir `ADMIN_SECRET` ayarla.
- AI anahtarlarını yalnızca backend değişkenlerinde tut; hiçbirini `NEXT_PUBLIC_*` yapma.
- `CORS_ORIGINS` değerini gerçek frontend alan adlarıyla sınırla.
- Kullanım limitlerini ve mümkünse Cloudflare Turnstile’ı etkinleştir.
- SQLite veritabanını kalıcı bir volume üzerinde tut veya yönetilen bir veritabanına geç.

Ayrıntılar için [SECURITY.md](SECURITY.md) dosyasına bak.

## Katkı ve lisans

Katkılar kabul edilir; önce [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını oku. Proje [MIT](LICENSE) lisansıyla yayımlanır.
