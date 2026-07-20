# CloudTask - UAS Cloud Computing

CloudTask adalah aplikasi manajemen tugas sederhana berbasis Flask dan PostgreSQL. Proyek ini dibuat untuk membuktikan implementasi aplikasi multi-container, Docker Compose, persistent volume, environment variable, health check, automated testing, dan pipeline GitHub Actions.

## Arsitektur

Pengguna -> Container Flask -> Container PostgreSQL

Service tambahan: Adminer untuk melihat isi database melalui browser.

## Fitur

- Menampilkan data tugas.
- Menambahkan data tugas.
- Mengubah data tugas.
- Menghapus data tugas.
- Validasi judul, deskripsi, dan status.
- Endpoint health check pada `/health`.
- Empat automated test menggunakan Pytest.
- Pipeline GitHub Actions untuk testing dan Docker build.
- Persistent volume untuk database PostgreSQL.

## Menjalankan dengan Docker

1. Salin environment example:

```bash
cp .env.example .env
```

Pada Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

2. Ubah password dan secret key di file `.env`.

3. Build dan jalankan service:

```bash
docker compose up -d --build
```

4. Periksa container:

```bash
docker compose ps
```

5. Buka aplikasi:

- Aplikasi: `http://localhost:5000`
- Health check: `http://localhost:5000/health`
- Adminer: `http://localhost:8080`

Konfigurasi Adminer:
- System: PostgreSQL
- Server: `db`
- Username: sesuai `POSTGRES_USER`
- Password: sesuai `POSTGRES_PASSWORD`
- Database: sesuai `POSTGRES_DB`

## Automated Testing Lokal

```bash
python -m venv .venv
```

Aktifkan virtual environment, lalu:

```bash
pip install -r requirements.txt
pytest -q
```

Target hasil: `4 passed`.

## Pengujian Persistent Volume

1. Tambahkan minimal satu data melalui aplikasi.
2. Hentikan dan hapus container tanpa menghapus volume:

```bash
docker compose down
```

3. Jalankan kembali:

```bash
docker compose up -d
```

4. Buka aplikasi dan tunjukkan bahwa data masih tersedia.

Catatan: jangan memakai `docker compose down -v` karena opsi `-v` menghapus volume database.

## Simulasi Ketahanan Layanan

1. Pastikan semua service sehat:

```bash
docker compose ps
```

2. Paksa container aplikasi berhenti:

```bash
docker kill cloudtask-app
```

3. Tunggu beberapa detik lalu periksa kembali:

```bash
docker compose ps
docker inspect --format='{{json .State.Health}}' cloudtask-app
```

Restart policy `unless-stopped` akan menjalankan kembali container setelah proses dihentikan secara paksa.

## Membuat Bukti Pipeline Gagal dan Berhasil

Lakukan secara terkontrol:

1. Pada test health check, ubah sementara:

```python
assert response.status_code == 200
```

menjadi:

```python
assert response.status_code == 500
```

2. Commit dan push:

```bash
git add .
git commit -m "test: simulate controlled pipeline failure"
git push
```

3. Ambil screenshot workflow yang gagal dan log assertion error.
4. Kembalikan assertion menjadi `200`.
5. Commit dan push kembali:

```bash
git add .
git commit -m "fix: restore health endpoint test"
git push
```

6. Ambil screenshot workflow yang berhasil.

## Rekomendasi Riwayat Commit

```text
chore: initialize CloudTask repository
feat: add task model and CRUD features
feat: add form validation and health endpoint
chore: add Dockerfile and docker compose services
test: add automated tests
ci: add GitHub Actions testing and docker build
test: simulate controlled pipeline failure
fix: restore health endpoint test
docs: complete README and UAS evidence
```

## Perintah Penting untuk Video

```bash
docker --version
docker compose version
docker compose up -d --build
docker compose ps
docker compose logs app
pytest -q
```

## Keamanan

- File `.env` tidak boleh diunggah.
- Password dan secret key hanya ditulis di `.env`.
- Repository hanya menyimpan `.env.example`.
- Jangan menampilkan password secara jelas dalam video atau screenshot.
