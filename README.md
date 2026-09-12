# Ankara Hazırlık

[![CI](https://github.com/efeabdush/AnkaraHazirlik/actions/workflows/ci.yml/badge.svg)](https://github.com/efeabdush/AnkaraHazirlik/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-1c3d5a.svg)](LICENSE)

Ankara Üniversitesi İngilizce hazırlık yeterlik / muafiyet sınavının B1+ yapısını temel alan, ücretsiz ve açık kaynak bir pratik platformu.

Proje ilk olarak kendi sınav hazırlığım için başladı. Sonra aynı süreçten geçen başka öğrencilerin de kullanabileceği; sadece soru göstermek yerine yanlışı açıklayan, yazıyı ve konuşmayı inceleyen bir çalışma ortamına dönüştü.

> Bu proje Ankara Üniversitesi, YABDİL veya başka bir kurum tarafından hazırlanmış ya da onaylanmış değildir. Resmî sınav materyallerini kopyalamaz; yayımlanan sınav yapısı ve değerlendirme başlıkları referans alınarak hazırlanmış özgün pratik içerikleri kullanır. AI puanları çalışma amaçlı tahmindir, resmî sonuç değildir.

## Neyi farklı yapıyor?

### Sınavı tek bir uzun teste sıkıştırmıyor

Kullanıcı ister bir bölümü ayrı ayrı çalışır, ister Sınav Merkezi'nden üç oturumluk 100 puanlık yapıyı takip eder:

| Oturum | Bölümler | Süre | Puan |
| --- | --- | ---: | ---: |
| 1 | Dinleme, okuma, dil kullanımı | 120 dk | 60 |
| 2 | Opinion essay | 60 dk | 20 |
| 3 | Konuşma | yaklaşık 10 dk | 20 |

Bitirilen dinleme, okuma ve dil kullanımı çalışmaları tarayıcıda işaretlenir. Böylece geniş havuzda hangi paketin daha önce çözüldüğü kaybolmaz.

### Hazır içerik havuzu gerçekten hazır gelir

AI anahtarı olmadan da temel sınav pratiği yapılabilir. Repo şunları içerir:

| Alan | Hazır içerik |
| --- | ---: |
| Kısa diyalog | 25 paket |
| Not alınabilen akademik dinleme | 25 paket |
| Standart okuma pasajı | 25 paket |
| Cümle yerleştirme | 25 paket |
| Cloze text | 25 paket |
| Restatement | 25 paket |
| Writing konu çekilişi | 50 konu |
| Speaking konu kartı | 100 kart |
| A1–B1+ Akış | 280 kısa kart |

Dinleme kayıtları önceden üretilmiş olarak repoya dahildir; kullanıcı ilk kez açtığı bir kayıt için yapay zekâ veya ses üretimi beklemez. İçerik testleri paket sayısını, soru yapısını, puan toplamını, ses-metni eşleşmesini ve alıştırmalar arasındaki aşırı benzerliği otomatik olarak kontrol eder.

### AI, sorunun bağlamını biliyor

Sonuç ekranındaki sohbet yalnızca genel bir chatbot değildir. Hangi metnin veya kaydın çözüldüğünü, soruyu, seçenekleri, verilen cevabı ve doğru cevabı bilir. Kullanıcı “Bu neden yanlış?” dedikten sonra aynı soru hakkında takip soruları sorabilir; sohbet o sayfadan ayrılana kadar bağlamını korur.

AI özellikleri kendi sağlayıcı anahtarınla açılır. OpenRouter, OpenCode Go / Zen ve Google Gemini desteklenir; aktif sağlayıcı ve model yönetim panelinden seçilebilir.

### Writing sadece kelime saymıyor

- 50 konu arasından rastgele tema ve soru seçimi
- Yazmaya başlayınca otomatik çalışan 60 dakikalık sayaç
- Kâğıda yazmak isteyenler için elle başlatma seçeneği
- Süre sonunda sakin bir sesli uyarı
- 250 kelime eşiği ve görev tamamlama, dil bilgisi, kelime, bağdaşıklık / tutarlılık başlıklarında geri bildirim
- Genel yorum yerine cümle düzeltmeleri ve bir sonraki deneme için uygulanabilir hedefler

### Speaking, mikrofondan geri bildirime kadar tek akış

Konu seçiminde 100 kartlık havuz bitmeden aynı kart yeniden gelmez. Hazırlık süresinden sonra mikrofon seviyesi gösterilir, konuşma kaydedilir ve `faster-whisper` ile sunucuda yerel olarak yazıya çevrilir.

Sistem yalnızca transkripti okumaz; yaklaşık konuşma hızını, dolgu seslerini (`um`, `uh`, `erm`, `hmm`), kısa tereddütleri, uzun duraklamaları, kelime tekrarlarını, uzatmaları ve düşük güvenli kelimeleri de geri bildirime katar. Değerlendirici, “C onsist ent is the K” gibi belirgin ses-yazı dönüşümü hatalarını öğrencinin dil hatası saymamaya çalışır.

Değerlendirmeden sonra kullanıcı:

- dört başlıkta 20 puanlık çalışma sonucunu,
- puan kaybettiren somut noktaları,
- daha doğal ifade alternatiflerini,
- bir sonraki antrenman için kısa egzersizleri,
- aynı oturumun bağlamını bilen AI koçunu

görür. Geçici ses dosyası transkripsiyon başarılı olsa da olmasa da işlem sonunda silinir.

### Akış: uzun test açmadan kısa pratik

Akış bölümü A1, A2, B1 ve B1+ seviyelerinde üç farklı format sunar:

- **Soru akışı:** 20–30 saniyelik kaydı dinle, tek soruyu cevapla.
- **Kelime akışı:** kısa metindeki yanlış yazılan kelimeyi bul.
- **Boşluk doldurma:** cümledeki eksik kelimeyi dört seçenekten tamamla.

Kart cevaplandıktan sonra açıklama görünür; soru formatında takılan yer aynı kartı bilen AI'a sorulabilir. Kaydırma davranışı bir sonraki karta kontrollü geçecek ve mobilde açılan geri bildirim alanını normal biçimde kaydıracak şekilde tasarlanmıştır.

### İçerik üretim paneli

`/admin` paneli yeni diyalog, akademik dinleme, okuma, dil kullanımı, writing konusu ve speaking kartı üretebilir. Üretilen paket doğrudan yayınlanmadan önce türe özel şema ve sınav sınırlarından geçer; dinleme paketlerinde metin, kelime yardımı ve ses dosyası aynı iş akışında hazırlanır.

Yerel kurulumda panel kullanıma açıktır. Production ortamında parolasız erişim ve panelden API anahtarı değiştirme otomatik olarak kapanır.

## Gizlilik ve anahtarlar

- Hesap veya kullanıcı profili yoktur.
- Çözülen alıştırma işaretleri kullanıcının kendi tarayıcısında tutulur.
- Konuşma sesi geçici olarak işlenir ve transkripsiyondan sonra silinir.
- AI özellikleri kullanıldığında ilgili soru, yazı veya transkript kurulum sahibinin seçtiği AI sağlayıcısına gönderilir.
- API anahtarları frontend'e verilmez. `.env` veya yerel, Git tarafından yok sayılan SQLite veritabanında tutulur.
- Yerel veritabanındaki panel anahtarları şifrelenmez; `backend/storage/` klasörü başkasıyla paylaşılmamalıdır.
- CI, takip edilen dosyalarda bilinen anahtar biçimlerini otomatik olarak tarar.

Ayrıntılar ve production kontrol listesi için [SECURITY.md](SECURITY.md) dosyasına bak.

## Yerelde çalıştırma

Canlı demo sunucu maliyeti nedeniyle sürekli açık tutulmuyor. Proje Windows, macOS, Linux veya Docker ile yerelde çalıştırılabilir.

### Gerekenler

- [Python 3.13](https://www.python.org/downloads/)
- [Node.js 22](https://nodejs.org/)
- Git

### Windows

```powershell
git clone https://github.com/efeabdush/AnkaraHazirlik.git
Set-Location AnkaraHazirlik
Copy-Item .env.example .env

python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt

Set-Location frontend
npm ci
Set-Location ..
```

İlk kurulumdan sonra `baslat.bat` dosyasına çift tıklamak yeterlidir.

### macOS / Linux

```bash
git clone https://github.com/efeabdush/AnkaraHazirlik.git
cd AnkaraHazirlik
cp .env.example .env

python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

İkinci terminalde:

```bash
cd AnkaraHazirlik/frontend
npm ci
npm run dev
```

### Docker

```bash
git clone https://github.com/efeabdush/AnkaraHazirlik.git
cd AnkaraHazirlik
cp .env.example .env
docker compose up --build
```

Docker portları yalnızca `127.0.0.1` adresine bağlar. Container ağında yönetim panelini kullanmak için `.env` içindeki `ADMIN_SECRET` değerine uzun bir yerel parola yazıp panelde aynı değeri kullan.

## İlk kullanım

1. Windows'ta `baslat.bat` dosyasını aç. macOS / Linux'ta yukarıdaki backend ve frontend komutlarını iki ayrı terminalde çalışır durumda bırak.
2. Tarayıcıdan [http://localhost:3000](http://localhost:3000) adresine git.
3. AI anahtarı eklemeden hazır testleri, dinleme kayıtlarını, Akış'ı, sayaçları ve çözülme işaretlerini kullanabilirsin.
4. AI sohbeti, içerik üretimi veya writing / speaking değerlendirmesi için [http://localhost:3000/admin](http://localhost:3000/admin) adresini açıp kendi sağlayıcı anahtarını **Test et ve kaydet** alanına gir, ardından modelini seç.
5. Yönetim panelinde üretilen içerik ve panel ayarları `backend/storage/hazirlik.db` dosyasında yerel olarak saklanır. Bu klasör Git'e eklenmez; kurulumunu taşımak istiyorsan ayrıca yedekle.
6. Windows'ta durdurmak için başlangıç penceresinde `Ctrl+C` tuşlarına bas. macOS / Linux'ta iki terminali de aynı şekilde durdur. Sonraki açılışta yerel veritabanın korunur.

Site veya API açılmazsa önce 3000 ve 8000 portlarını başka bir programın kullanmadığını kontrol et. Windows başlatıcısının ayrıntılı çıktıları `.runlogs/` klasöründedir.

## Kendi AI sağlayıcını bağlama

Yerelde `/admin` sayfasını aç, sahip olduğun sağlayıcı anahtarını **Test et ve kaydet** alanına gir, ardından modelini seç.

| Sağlayıcı | Backend ortam değişkeni |
| --- | --- |
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenCode Go / Zen | `OPENCODE_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |

Anahtar olmadan hazır testler, sesler, sayaçlar, Akış ve ilerleme işaretleri çalışır. Soru sohbeti, içerik üretimi, writing / speaking değerlendirmesi ve AI koçu için bir sağlayıcı gerekir.

## Teknik yapı

```text
frontend/          Next.js 16, React 19, TypeScript, Tailwind CSS
backend/           FastAPI, SQLAlchemy, SQLite, faster-whisper
content/seeds/     sınav pratiği başlangıç paketleri
content/listening/ hazır dinleme sesleri ve manifest
content/akis/      A1–B1+ kısa Akış kartları ve sesleri
content/prompts/   AI üretim ve açıklama talimatları
```

AI katmanı sağlayıcıdan bağımsız tutulur. Backend; model seçimi, JSON doğrulama, kullanım limitleri, eşzamanlı istek sınırı ve isteğe bağlı Cloudflare Turnstile korumasını yönetir. Frontend telefon, tablet ve masaüstünde aynı akışları kullanır.

## Kontroller

```bash
python scripts/check_secrets.py

cd backend
python -m pytest -q

cd ../frontend
npm run lint
npm run typecheck
npm run check:glossary
npm run build
```

GitHub Actions aynı kontrolleri her push ve pull request'te çalıştırır.

## Production'a açmadan önce

- `APP_ENV=production` ve uzun, rastgele bir `ADMIN_SECRET` ayarla.
- AI anahtarlarını yalnızca backend değişkenlerinde tut.
- `CORS_ORIGINS` değerini gerçek frontend alan adlarıyla sınırla.
- Kullanım / harcama limitlerini ve gerekirse Cloudflare Turnstile'ı etkinleştir.
- SQLite veritabanını kalıcı volume'a bağla veya yönetilen bir veritabanı kullan.

## Katkı ve lisans

Hata düzeltmeleri, kullanıcı deneyimi iyileştirmeleri ve telifsiz, özgün B1+ pratik içerikleri için katkılara açıktır. Resmî sınav PDF'lerini, cevap anahtarlarını veya başka kaynaklardan kopyalanmış materyalleri eklemeyin; ayrıntılar [CONTRIBUTING.md](CONTRIBUTING.md) dosyasında.

Proje [MIT lisansı](LICENSE) ile sunulur.
