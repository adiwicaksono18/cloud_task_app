# Rancangan Presentasi Maksimal 8 Slide

## Slide 1 - Identitas Proyek
Nama, NIM, kelas, CloudTask, tujuan proyek.

## Slide 2 - Permasalahan dan Solusi
Masalah pengelolaan tugas dan kebutuhan penerapan cloud computing. Solusi aplikasi CRUD multi-container.

## Slide 3 - Arsitektur Sistem
Diagram pengguna -> Flask -> PostgreSQL, ditambah Adminer, volume, network, dan GitHub Actions.

## Slide 4 - Implementasi Aplikasi
Fitur tampil, tambah, ubah, hapus, validasi input, dan endpoint health check.

## Slide 5 - Implementasi Docker
Dockerfile, tiga service Docker Compose, network, depends_on, restart policy, volume, dan environment variable.

## Slide 6 - Automated Testing dan CI/CD
Empat pengujian Pytest. Alur checkout -> setup Python -> install dependency -> test -> Docker build. Bukti pipeline gagal dan berhasil.

## Slide 7 - Pengujian Ketahanan
Persistent volume, health check, simulasi container mati, restart policy, dan hasil pengujian.

## Slide 8 - Kesimpulan dan Pengembangan
Komponen wajib berhasil diterapkan. Rencana cloud: registry, VPS, reverse proxy, HTTPS, managed database, backup, monitoring.
