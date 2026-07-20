# Naskah Video Demonstrasi 7-10 Menit

## 0:00-0:30 - Pembukaan
Perkenalkan nama, NIM, kelas, mata kuliah, dan nama aplikasi CloudTask.

## 0:30-1:30 - Repository dan Arsitektur
Tampilkan repository. Jelaskan folder `app`, `tests`, Dockerfile, `docker-compose.yml`, `.env.example`, workflow GitHub Actions, dan dokumentasi. Tampilkan diagram arsitektur.

## 1:30-2:15 - Versi dan Menjalankan Container
Jalankan:
- `docker --version`
- `docker compose version`
- `docker compose up -d --build`
- `docker compose ps`

Jelaskan tiga service: app, db, dan adminer.

## 2:15-3:30 - Demonstrasi Fitur
Buka aplikasi. Tambahkan data, tampilkan data, ubah status, coba validasi judul kosong, lalu hapus satu data.

## 3:30-4:20 - Database dan Environment
Buka Adminer dan tunjukkan tabel `tasks`. Jelaskan bahwa aplikasi memakai environment variable dan file `.env` tidak diunggah.

## 4:20-5:10 - Persistent Volume
Buat satu data khusus. Jalankan `docker compose down`, kemudian `docker compose up -d`. Tunjukkan data tetap ada.

## 5:10-5:50 - Automated Testing
Jalankan `pytest -q`. Jelaskan empat test: health check, create, validasi, update-delete.

## 5:50-7:00 - Pipeline Gagal dan Berhasil
Buka GitHub Actions. Tunjukkan workflow gagal, log assertion error, commit perbaikan, dan workflow berhasil. Jelaskan bahwa test menjadi quality gate sebelum Docker build.

## 7:00-8:00 - Health Check dan Simulasi Gangguan
Buka `/health`. Jalankan `docker kill cloudtask-app`, lalu `docker compose ps`. Tunjukkan container kembali berjalan karena restart policy.

## 8:00-9:00 - Analisis Cloud Computing
Jelaskan hubungan source code, image, container, Compose, network, volume, dan CI/CD. Jelaskan dampak bila database gagal dan cara pemulihan.

## 9:00-9:30 - Penutup
Sampaikan kesimpulan, kendala, solusi, dan rencana deployment ke cloud/VPS.
