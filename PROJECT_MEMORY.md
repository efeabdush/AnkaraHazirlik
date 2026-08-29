# Proje hafıza notu

## Yayın hedefi

- Ankara Hazırlık MVP'sini güvenli biçimde internete aç.
- Önerilen yapı: özel GitHub deposu -> Railway üzerinde frontend + backend -> Cloudflare üzerinde domain/DNS, HTTPS ve kötüye kullanım koruması.

## Yayından önce siteyi temize çekme

- Ankara Üniversitesi/YABDİL gerçek sınav bölüm, süre, soru sayısı ve değerlendirme ölçütlerini son kez doğrula.
- Sınav Merkezi akışını, bölüm açıklamalarını ve tam denemeye geçişi anlaşılır hâle getir.
- Mikrofon/konuşma algılama ve dolgu sesi geri bildirimini doğrula.
- Yazma konu seçimini, dil bölümü performansını ve tüm AI cevaplarında Markdown görünümünü kontrol et.
- Telefon, tablet ve bilgisayarda bütün ana akışları uçtan uca test et.
- Admin rotalarını kapat; API anahtarları, CORS, kalıcı disk, istek sınırı, Turnstile, harcama limiti ve gizlilik metnini production için ayarla.

Kullanıcı "bir şey unuttuk mu?" diye sorduğunda bu listeyi kontrol et.
