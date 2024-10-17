# Bot Perpustakaan UGM

Selamat datang di **Bot Perpustakaan UGM**! Bot ini memungkinkan pengguna untuk dengan mudah memesan kursi di perpustakaan UGM melalui Telegram.

## Fitur
- **Memesan kursi** di perpustakaan UGM.
- **Memeriksa ketersediaan** kursi.

## Prasyarat
- Python 3.x
- Library:
  - `python-telegram-bot`
  - Dependensi lainnya (jika ada)

## Petunjuk Pengaturan

### 1. Kloning Repository
Untuk memulai, klon repository dengan menggunakan perintah berikut:
```bash
git clone https://github.com/username-anda/ugm-library-seat-booking-bot.git
cd ugm-library-seat-booking-bot
```

### 2. Instal Dependensi
Pastikan Anda memiliki `pip` terinstal, lalu jalankan perintah berikut untuk menginstal library yang diperlukan:
```bash
pip install -r requirements.txt
```

### 3. Menangkap `SESSION_ID` dan `GROUP_MENU` dengan Proxyman
`SESSION_ID` dan `GROUP_MENU` berfungsi untuk otentikasi bot saat mengambil data kursi dan melakukan reservasi. Untuk menangkap `SESSION_ID` dan `GROUP_MENU`, ikuti langkah-langkah berikut:

1. **Instal Proxyman**:
   - Buka Proxyman dan konfigurasikan pengaturan proxy.
   - Aktifkan SSL Proxying dan tambahkan aturan untuk domain `*.ugm.ac.id`.

2. **Instal Sertifikat Proxyman**:
   - Instal sertifikat Proxyman di sistem Anda.

3. **Mulai Menangkap Lalu Lintas**:
   - Buka aplikasi UGM Simaster dan buka salah satu menu (contoh Perpustakaan).

4. **Analisis Permintaan**:
   - Di Proxyman, cari permintaan terkait yang mirip dengan contoh URL berikut:
     ```
     https://simaster.ugm.ac.id/services/simaster/ongoing?sesId=xxxx-xxxx=&groupMenu=yyyy-yyyy=&menu=999
     ```
   - Dari URL tersebut, Anda dapat mengambil nilai `sesId` dan `groupMenu` sebagai berikut:
     - `SESSION_ID`: `xxxx-xxxx`
     - `GROUP_MENU`: `yyyy-yyyy`

### 4. Konfigurasi
Sebelum menjalankan bot, Anda perlu mengatur token bot Telegram dan variabel konfigurasi lainnya.

Buka file `config.py` (atau file konfigurasi yang Anda gunakan) dan ubah variabel berikut:
```python
TELEGRAM_TOKEN = '{YOUR_TELEGRAM_BOT_TOKEN}'  # Ganti dengan Token Bot Telegram Anda
SESSION_ID = "{YOUR_SESSION_ID}"                # Ganti dengan Session ID Anda
GROUP_MENU = "{GROUP_MENU}"                      # Ganti dengan Group Menu ID Anda
```

### 5. Jalankan Bot
Setelah mengatur konfigurasi, Anda dapat menjalankan bot menggunakan perintah berikut:
```bash
python bot.py
```

### 6. Penggunaan
- Mulai bot di Telegram dengan mencari nama pengguna dan klik 'Start'.
- Ikuti petunjuk untuk memesan kursi di perpustakaan UGM.

## Kontribusi
Kontribusi sangat diterima! Jika Anda memiliki saran atau perbaikan, silakan buka isu atau kirim permintaan tarik (pull request).

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.
