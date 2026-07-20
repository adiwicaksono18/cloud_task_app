# Checklist Bukti Wajib UAS

## Identitas dan Repository
- [ ] Nama, NIM, dan kelas sudah ditulis.
- [ ] Repository GitHub dapat diakses dosen.
- [ ] Riwayat commit menunjukkan perkembangan.
- [ ] `.env` tidak ada di repository.
- [ ] `.env.example` tersedia.

## Aplikasi
- [ ] Data dapat ditampilkan.
- [ ] Data dapat ditambahkan.
- [ ] Data dapat diubah.
- [ ] Data dapat dihapus.
- [ ] Validasi input dapat ditunjukkan.
- [ ] Aplikasi terhubung PostgreSQL.

## Docker
- [ ] Screenshot `docker --version`.
- [ ] Screenshot `docker compose version`.
- [ ] Screenshot `docker compose up -d --build`.
- [ ] Screenshot `docker compose ps`.
- [ ] Minimal container app dan db berjalan.
- [ ] Service Adminer berjalan sebagai nilai tambah.
- [ ] Docker image berhasil dibangun.

## Volume dan Environment
- [ ] Screenshot data sebelum `docker compose down`.
- [ ] Screenshot data setelah `docker compose up -d`.
- [ ] Data tetap tersedia.
- [ ] Nilai credential berasal dari `.env`.

## Testing dan CI/CD
- [ ] `pytest -q` menghasilkan minimal 3 test berhasil.
- [ ] Workflow GitHub Actions gagal dapat dibuka.
- [ ] Log penyebab kegagalan ditunjukkan.
- [ ] Commit perbaikan tersedia.
- [ ] Workflow GitHub Actions berhasil dapat dibuka.
- [ ] Job Docker build berhasil.

## Health Check dan Ketahanan
- [ ] Endpoint `/health` menunjukkan `healthy`.
- [ ] Status health container ditunjukkan.
- [ ] Container dihentikan/dibunuh secara terkontrol.
- [ ] Restart policy dan pemulihan ditunjukkan.

## Luaran
- [ ] Laporan PDF 10-15 halaman.
- [ ] Video demonstrasi 7-10 menit.
- [ ] Diagram arsitektur.
- [ ] Presentasi maksimal 8 slide.
- [ ] Form link pengumpulan lengkap.
