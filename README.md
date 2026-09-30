# UTS Web Application Development - Pemesanan Shuttle Kampus

Proyek ini adalah aplikasi web untuk memanajemen pemesanan shuttle bus kampus, dibuat untuk memenuhi tugas UTS.

## Teknologi yang Digunakan
- **Backend:** FastAPI, Pydantic, Uvicorn (Python)
- **Frontend:** Vue 3, Vite, Fetch API (JavaScript)
- **Database:** In-memory dataset (List of Dictionaries di Python)

---

## Cara Menjalankan Server

### 1. Menjalankan Backend (FastAPI)
Buka terminal baru dan jalankan perintah berikut:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend akan berjalan di `http://localhost:8000`.

### 2. Menjalankan Frontend (Vue 3 + Vite)
Buka terminal baru yang lain dan jalankan perintah berikut:

```bash
cd frontend
npm install
npm run dev
```
Frontend akan berjalan di `http://localhost:5173` (atau port lain yang ditampilkan di terminal). Buka URL tersebut di browser.

---

## Verifikasi Kriteria Penilaian

### Backend
1. **Dataset in-memory (Min 12 baris):** Terdapat di `backend/app/data.py` dengan 12 baris data rute shuttle sintetis.
2. **GET /sessions (Pagination + Search):** Diimplementasikan di `main.py`. Menerima parameter `?q=`, `?page=`, dan `?limit=`.
3. **GET /sessions/{id} (404):** Jika ID tidak ditemukan, mengembalikan HTTP 404 Not Found.
4. **POST /sessions (Pydantic, 201):** Menggunakan `SessionCreate` (Pydantic BaseModel) untuk validasi, mengembalikan status 201 Created.
5. **DELETE /sessions/{id} (204):** Menghapus data dari list in-memory dan mengembalikan status 204 No Content (atau 404 jika gagal).
6. **CORS:** Diaktifkan menggunakan `CORSMiddleware` agar frontend (`localhost:5173`) bisa mengakses API.

### Frontend
1. **Daftar dari API:** Data ditampilkan dalam bentuk tabel, diambil dari `GET /sessions`.
2. **Empat State + Retry:**
   - **Loading:** Teks "Memuat data..." saat fetch data.
   - **Error:** Pesan error dan tombol "Coba Lagi" (bisa diuji dengan mematikan server backend).
   - **Empty:** Pesan jika tidak ada pesanan di tabel.
   - **Data:** Menampilkan data di tabel beserta tombol Hapus.
3. **Form Create dengan Validasi:** Terdapat di kolom kiri dengan validasi sederhana (semua field wajib diisi sebelum bisa klik Pesan).
4. **Hapus dengan Konfirmasi:** Saat tombol "Hapus" diklik, muncul `confirm()` (Pop-up peringatan dari browser).

---

## Pengungkapan AI
Dalam pembuatan proyek ini, saya menggunakan bantuan AI (Antigravity CLI) dengan proporsi sebagai berikut:
- **Ideasi:** Membantu memunculkan ide domain (Pemesanan Shuttle).
- **Boilerplate:** Menghasilkan template dasar Vue.js dan FastAPI.
- **Debugging:** Membantu menemukan penyebab dan solusi error pada kofigurasi CORS.
