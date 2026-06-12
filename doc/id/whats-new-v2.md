# Apa yang baru di v2.3/v2.4

Panduan ini merangkum fitur-fitur utama yang ditambahkan di **stable v2.3** dan **stable v2.4** dari HotelRestaurantMini-MartManagement.

**Situs stabil langsung:**

| Versi | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Pengembangan** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Antarmuka lengkap dalam 21 bahasa

UI aplikasi web tersedia dalam **21 lokal**: Inggris, Spanyol, Prancis, Jerman, Jepang, Korea, Arab, Hindi, Thailand, Vietnam, Indonesia, Turki, Rusia, Italia, Belanda, Polandia, Ibrani, Laos, Portugis (Brasil), China (Sederhana), dan China (Tradisional).

### Tempat mengubah bahasa

| Layar | Bagaimana |
|--------|-----|
| **Masuk / pengaturan** | Dropdown bahasa di header (sebelum masuk) |
| **Setelah masuk** | Pemilih lokal bilah atas atau **Lokalisasi** di menu |
| **Pengaturan** | Bagian bahasa aplikasi |

Preferensi disimpan di penyimpanan browser (`hotel_mgr_uiLocale`).

### RTL (kanan ke kiri)

**Arab** dan **Ibrani** mengaktifkan tata letak RTL untuk seluruh aplikasi. Bentuk modal menggunakan penyelarasan yang ditingkatkan sehingga label dan masukan terbaca dengan benar dalam bahasa LTR dan RTL.

---

## Penyiapan pertama kali (diterjemahkan)

Wizard pengaturan sepenuhnya dilokalkan:

- Nama bisnis / hotel
- Teks header sistem
- Bidang nama pengguna admin, email, dan kata sandi
- Semua tombol dan pesan validasi

Setelah pengaturan, nama hotel disimpan dan ditampilkan di header aplikasi tempat dikonfigurasi.

---

## Tindakan cepat dasbor (kisi PMS)

**Dasbor** menampilkan kotak tombol **+** biru untuk tugas umum:

| Tombol | Buka |
|--------|--------|
| Tambahkan Ruangan | Bentuk ruangan baru |
| Tambahkan Pemesanan | Formulir pemesanan baru |
| Tambahkan Tamu | Formulir tamu baru |
| Tambahkan Tugas | Tiket pemeliharaan baru |
| Tambahkan Layanan | Permintaan layanan baru |
| Tambahkan Faktur | Formulir faktur baru |
| Tambah Stok | Barang inventaris baru |
| Tambahkan Menu | Item menu baru |
| Tambahkan Item Toko | Barang baru toko/minimarket |
| Tambahkan Pengguna | Akun staf baru |

**Catatan:** *Tambahkan Pembersihan* dan *Tambahkan Transaksi* telah dihapus dari grid ini (v2.4). Gunakan sidebar untuk **Pembenahan Kamar** dan **Transaksi** bila diperlukan.

---

## Bentuk modal yang diterjemahkan

Dialog tambah dan edit dilokalkan dalam 21 bahasa, termasuk:

- **Pemeliharaan** — tiket baru (ruangan, prioritas, penerbitan, catatan)
- **Faktur** — tambahkan / edit (tamu, kamar, tanggal, jumlah, status pembayaran)
- **Inventaris** — menambah / mengedit item (nama, kode batang, kategori, jumlah, ketersediaan POS)
- **Item menu** — tambahkan / edit (nama, ikon, harga, kategori, gambar, tautan stok)
- **Simpan item** — tambahkan / edit (nama, harga, kategori, ikon rak, kode batang, stok)- **Akun pengguna** — tambahkan / edit (nama, email, kata sandi, peran)

Label unggahan gambar (“dari perangkat”, “atau URL gambar”) mengikuti bahasa aktif.

---

## Pemesanan → Tamu baru

Saat membuat **pemesanan**, jika tamu belum ada di direktori:

1. Ketuk **+ Tamu baru** (atau setara) pada formulir pemesanan.
2. Isi modal **Tamu Baru** (nama, paspor, kewarganegaraan, tanggal lahir, metode pembayaran, kontak, catatan).
3. Ketuk **Tambahkan tamu & kembali** — Anda kembali ke pemesanan dengan tamu baru yang dipilih.

Pemilih kewarganegaraan (daftar pencarian) juga diterjemahkan.

---

## Dokumentasi

- Panduan **Apa yang baru** ini tersedia dalam 21 bahasa dokumentasi.
- Buka dokumen dari aplikasi: **bilah atas → Dokumentasi**, **☰ Bantuan → Dokumentasi**, atau **nav bawah → Dokumen**.
- URL mandiri: `/doc/?lang={code}#/whats-new-v2`

---

## Untuk administrator

| Tugas | Dimana |
|------|--------|
| Latih staf tentang peralihan bahasa | [Localization](localization.md) |
| Konfigurasikan properti setelah peningkatan | [Settings & configuration](settings-and-configuration.md) |
| Menyebarkan pembaruan | [Deployment](deployment.md) — `npm run deploy:stable` diterbitkan ke v2.3 dan v2.4 |

---

## Panduan terkait

- [Localization](localization.md) — bahasa, RTL, file lokal
- [First-time setup](first-time-setup.md) — konfigurasi awal
- [Navigation & UI](navigation-and-ui.md) — dasbor, bilah sisi, navigasi seluler
- [Hotel operations](hotel-operations.md) — pemesanan dan tamu
- [Deployment](deployment.md) — pengembangan vs stabil v2.3 / v2.4