# v2.3 / v2.4'teki yenilikler

Bu kılavuz, HotelRestaurantMini-MartManagement'in **stable v2.3** ve **stable v2.4** sürümlerinde eklenen önemli özellikleri özetlemektedir.

**Canlı kararlı siteler:**

| Sürüm | URL'si |
|-----------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Geliştirme** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## 21 dilde tam arayüz

Web uygulaması kullanıcı arayüzü **21 yerel ayarda** mevcuttur: İngilizce, İspanyolca, Fransızca, Almanca, Japonca, Korece, Arapça, Hintçe, Tayca, Vietnamca, Endonezyaca, Türkçe, Rusça, İtalyanca, Felemenkçe, Lehçe, İbranice, Laoca, Portekizce (Brezilya), Çince (Basitleştirilmiş) ve Çince (Geleneksel).

### Dil nerede değiştirilir?

| Ekran | Nasıl |
|----------|-----|
| **Giriş / kurulum** | Başlıktaki dil açılır menüsü (oturum açmadan önce) |
| **Giriş yaptıktan sonra** | Üst çubuktaki yerel ayar seçici veya menüdeki **Yerelleştirme** |
| **Ayarlar** | Uygulama dili bölümü |

Tercih tarayıcı depolama alanına kaydedilir (`hotel_mgr_uiLocale`).

### RTL (sağdan sola)

**Arapça** ve **İbranice** tüm uygulama için RTL düzenini etkinleştirir. Modal formlar, etiketlerin ve girişlerin hem LTR hem de RTL dillerinde doğru şekilde okunması için gelişmiş hizalama kullanır.

---

## İlk kurulum (çevrilmiş)

Kurulum sihirbazı tamamen yerelleştirilmiştir:

- İşletme / otel adı
- Sistem başlığı metni
- Yönetici kullanıcı adı, e-posta ve şifre alanları
- Tüm düğmeler ve doğrulama mesajları

Kurulumdan sonra otel adı, yapılandırılan uygulama başlığında saklanır ve gösterilir.

---

## Kontrol paneli hızlı eylemleri (PMS kılavuzu)

**Kontrol Paneli**, ortak görevler için mavi **+** düğmelerden oluşan bir tablo gösterir:

| Düğme | Açılıyor |
|----------|-----------|
| Oda Ekle | Yeni oda formu |
| Rezervasyon Ekle | Yeni rezervasyon formu |
| Misafir Ekle | Yeni misafir formu |
| Görev Ekle | Yeni bakım bileti |
| Hizmet Ekle | Yeni hizmet talebi |
| Fatura Ekle | Yeni fatura formu |
| Stok Ekle | Yeni envanter öğesi |
| Menü Ekle | Yeni menü öğesi |
| Mağaza Öğesi Ekle | Yeni mağaza / mini market ürünü |
| Kullanıcı Ekle | Yeni personel hesabı |

**Not:** *Temizlik Ekle* ve *İşlem Ekle* bu kılavuzdan kaldırıldı (v2.4). Gerektiğinde **Temizlik** ve **İşlemler** için kenar çubuğunu kullanın.

---

## Çevrilmiş kalıcı formlar

Ekleme ve düzenleme iletişim kutuları, aşağıdakiler dahil olmak üzere 21 dilin tamamında yerelleştirilmiştir:

- **Bakım** — yeni bilet (oda, öncelik, düzenleme, notlar)
- **Fatura** — ekle / düzenle (misafir, oda, tarihler, tutarlar, ödeme durumu)
- **Envanter** — öğe ekle / düzenle (ad, barkod, kategori, miktar, POS kullanılabilirliği)
- **Menü öğesi** — ekle / düzenle (isim, simge, fiyat, kategori, resim, hisse senedi bağlantısı)
- **Mağaza öğesi** — ekle / düzenle (isim, fiyat, kategori, raf simgesi, barkod, stok)- **Kullanıcı hesabı** — ekle / düzenle (ad, e-posta, şifre, rol)

Resim yükleme etiketleri (“cihazdan”, “veya resim URL'si”) etkin dili takip eder.

---

## Rezervasyon → Yeni misafir

**Rezervasyon** oluştururken misafir henüz dizinde değilse:

1. Rezervasyon formunda **+ Yeni misafir** (veya eşdeğeri) seçeneğine dokunun.
2. **Yeni Misafir** formunu doldurun (isim, pasaport, uyruk, doğum tarihi, ödeme yöntemi, iletişim bilgileri, notlar).
3. **Misafir ekle ve geri dön** seçeneğine dokunun; yeni misafir seçili olarak rezervasyona geri dönersiniz.

Uyruk seçici (arama listesi) de tercüme edilir.

---

## Belgeler

- Bu **Yenilikler** kılavuzu 21 belge dilinin tamamında mevcuttur.
- Dokümanları uygulamadan açın: **üst çubuk → Dokümantasyon**, **☰ Yardım → Dokümantasyon** veya **alt gezinme → Dokümanlar**.
- Bağımsız URL: `/doc/?lang={code}#/whats-new-v2`

---

## Yöneticiler için

| Görev | Nerede |
|------|--------|
| Personeli dil değişimi konusunda eğitin | [Localization](localization.md) |
| Yükseltme sonrasında mülkü yapılandırın | [Settings & configuration](settings-and-configuration.md) |
| Güncellemeleri dağıtın | [Deployment](deployment.md) — `npm run deploy:stable` v2.3 ve v2.4'te yayınlanıyor |

---

## İlgili kılavuzlar

- [Localization](localization.md) — diller, RTL, yerel ayar dosyaları
- [First-time setup](first-time-setup.md) — ilk yapılandırma
- [Navigation & UI](navigation-and-ui.md) — gösterge paneli, kenar çubuğu, mobil gezinme
- [Hotel operations](hotel-operations.md) — rezervasyonlar ve misafirler
- [Deployment](deployment.md) — geliştirme ve kararlı v2.3 / v2.4 karşılaştırması