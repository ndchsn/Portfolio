# Portfolio (Flask • Cloud/DevOps Vibes)

Website portfolio berbasis Flask dengan nuansa Cloud/DevOps (glassmorphism, gradient, cloud background). Memuat: Summary, Experiences, Expertise, Certifications (klik ke credential), Education, dan Contact Me (chat box).

Fitur:
- UI modern, responsive (Bootstrap + CSS kustom).
- Contact Me: kirim email via SendGrid API (disarankan di hosting gratis) dengan fallback SMTP.
- Data profil mudah diubah dari app.py.
- .env di-ignore agar rahasia aman.


## 1. Prasyarat

- Python 3.10+ (disarankan)
- Pip
- Git
- Akun GitHub (untuk deployment)
- Opsional: Akun SendGrid (Free) untuk pengiriman email via API


## 2. Clone & Instalasi

```bash
git clone https://github.com/ndchsn/Portfolio.git
cd Portfolio
python -m pip install -r requirements.txt
```

Jika pip belum terupdate:
```bash
python -m pip install --upgrade pip
```


## 3. Konfigurasi Environment (.env)

Jangan commit file .env. Di repo ini .env sudah di-ignore oleh git. Gunakan .env.example sebagai referensi.

Langkah:
1) Duplikat .env.example menjadi .env
2) Isi variabel berikut:

```
# Flask
FLASK_SECRET_KEY=ubah-ini-di-produksi
PORT=5000

# SendGrid (rekomendasi untuk hosting gratis seperti Render)
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM=you@example.com

# SMTP (opsional fallback jika SendGrid tidak tersedia)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASS=your_app_password_without_spaces

# Logging
LOG_LEVEL=INFO
```

Catatan keamanan:
- Jangan pernah commit .env ke repository publik.
- Gunakan App Password untuk Gmail (aktifkan 2FA, lalu buat App Password) jika memakai SMTP.


## 4. Menjalankan Secara Lokal

```bash
python app.py
```

Akses: http://127.0.0.1:5000

Pengujian kirim email:
- Buka bagian “Contact Me” → isi chat → Kirim.
- Jika SendGrid API Key valid, email dikirim via API.
- Jika tidak ada SendGrid, dan SMTP di .env valid, maka fallback ke SMTP.
- Log akan menampilkan:
  - [CONTACT_REQUEST] … saat request masuk
  - [CONTACT_SENT] method=sendgrid|smtp … saat sukses
  - Peringatan/error jika gagal


## 5. Mengubah Konten

- app.py:
  - PROFILE (nama, role, summary, avatar, location, links)
  - EXPERIENCES (company, role, period, highlights, stack)
  - EXPERTISE
  - CERTIFICATIONS (name, issuer, year, url → untuk tautan credential)
  - EDUCATION
- templates/base.html: layout dasar
- templates/index.html: struktur halaman utama
- static/css/style.css: tema, warna, efek
- static/js/animations.js: animasi ringan


## 6. Kirim Email via SendGrid (Direkomendasikan)

Mengapa SendGrid?
- Banyak hosting gratis (mis. Render) membatasi SMTP outbound. SendGrid API via HTTPS lebih andal.

Langkah membuat SendGrid:
1) Daftar akun SendGrid (Free): https://sendgrid.com → Sign Up.
2) Verifikasi pengirim:
   - Paling cepat: Single Sender Verification
     - Settings → Sender Authentication → Single Sender → Create New
     - Gunakan email Anda sendiri (yang bisa diverifikasi).
     - Klik link verifikasi yang dikirim SendGrid.
   - Alternatif: Domain Authentication (via DNS) untuk deliverability lebih baik.
3) Buat API Key:
   - Settings → API Keys → Create API Key (beri izin Mail Send).
4) Isi .env:
   - SENDGRID_API_KEY=… 
   - SENDGRID_FROM=alamat_pengirim_terverifikasi
5) Jalankan aplikasi / deploy, lalu uji kirim dari “Contact Me”.


## 7. Alternatif: Kirim Email via SMTP

Jika ingin SMTP (mis. Gmail):
- Gunakan App Password (bukan password akun biasa)
  - Aktifkan 2FA, lalu buat App Password (16 karakter)
- .env:
  ```
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=you@gmail.com
  SMTP_PASS=APP_PASSWORD_TANPA_SPASI
  ```
- Catatan: Di beberapa hosting gratis, SMTP outbound bisa diblokir.


## 8. Deploy Gratis ke Render (Direkomendasikan)

a) Persiapan Repo
- Pastikan .env TIDAK ter-commit (git status harus tidak menampilkan .env).
- Push kode ke GitHub repository.

b) Buat Web Service di Render
1) https://dashboard.render.com → New → Web Service
2) Connect repository: ndchsn/Portfolio
3) Name: andiichsan-portfolio (atau yang Anda mau; akan menentukan subdomain .onrender.com)
4) Region: Asia (Singapore) (lebih dekat)
5) Runtime: Python
6) Build Command:
   ```
   pip install -r requirements.txt
   ```
7) Start Command:
   ```
   python app.py
   ```
8) Environment → tambahkan variabel:
   - FLASK_SECRET_KEY=… 
   - SENDGRID_API_KEY=… 
   - SENDGRID_FROM=… 
   - (Opsional) SMTP_HOST/PORT/USER/PASS jika ingin fallback SMTP
   - (Opsional) LOG_LEVEL=INFO
   - Jangan set PORT; Render akan menyediakannya otomatis.
9) Create Web Service → tunggu build selesai.

c) Tes Produksi
- Kunjungi URL: https://<nama-service>.onrender.com
- Uji kirim di “Contact Me”
- Cek Logs di Render:
  - Harus ada [CONTACT_REQUEST] saat kirim
  - Jika sukses: [CONTACT_SENT] method=sendgrid atau method=smtp

d) Auto-Deploy (opsional)
- Aktifkan Auto Deploy agar setiap push ke branch utama otomatis ter-deploy.

Troubleshooting:
- “Network is unreachable” saat SMTP: host gratis sering blokir SMTP. Pakai SendGrid API.
- “401 Unauthorized” (SendGrid): API Key salah/izin kurang → buat ulang dengan izin “Mail Send”.
- “from not verified” (SendGrid): alamat SENDGRID_FROM belum diverifikasi (Single Sender/Domain Auth).
- Email masuk ke spam: pertimbangkan verifikasi domain (SPF/DKIM) di SendGrid.


## 9. Keamanan Secrets

- .env sudah di-ignore oleh git (cek .gitignore).
- Simpan rahasia (API key, password) hanya di .env lokal dan di Environment Variables platform hosting.
- Jika terlanjur commit secret, segera:
  - Rotate key/password di provider.
  - Hapus dari history (BFG/`git filter-repo`) dan force push.


## 10. Skrip/Perintah Ringkas

- Install dep:
  ```
  python -m pip install -r requirements.txt
  ```
- Run lokal:
  ```
  python app.py
  ```
- Cek env terbaca (opsional, Windows PowerShell):
  ```
  echo $env:SENDGRID_API_KEY
  echo $env:SMTP_HOST
  ```

Selesai. Jika perlu saya siapkan file render.yaml (infra-as-code) agar mudah migrasi/otomasi deployment, beri tahu saya.