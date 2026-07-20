# LAPORAN UJIAN AKHIR SEMESTER CLOUD COMPUTING

## IMPLEMENTASI APLIKASI CLOUDTASK MENGGUNAKAN DOCKER MULTI-CONTAINER DAN CI/CD GITHUB ACTIONS

**Nama:** [ISI NAMA]  
**NIM:** [ISI NIM]  
**Kelas:** [ISI KELAS]  
**Program Studi:** S1 Informatika  
**Mata Kuliah:** Cloud Computing  
**Dosen Penguji:** Dr. Dhendra Marutho, S.Kom., M.Kom.  
**Tahun:** 2026  

> Dokumen ini merupakan draft isi laporan. Tambahkan screenshot pada bagian bertanda **BUKTI** agar setelah diformat menjadi 10-15 halaman.

# BAB I PENDAHULUAN

## 1.1 Latar Belakang

Aplikasi modern tidak hanya dinilai dari fungsi yang terlihat oleh pengguna, tetapi juga dari cara aplikasi tersebut dibangun, dijalankan, diuji, dan dipelihara. Pada pola pengembangan konvensional, aplikasi dan database sering dipasang langsung pada satu komputer. Cara tersebut dapat menimbulkan perbedaan konfigurasi antarkomputer, konflik dependency, kesulitan pemindahan aplikasi, dan risiko proses instalasi yang tidak konsisten.

Containerization menggunakan Docker memungkinkan aplikasi beserta dependency-nya dibungkus menjadi Docker image yang dapat dijalankan sebagai container. Konfigurasi yang sama dapat digunakan pada komputer pengembang, lingkungan pengujian, maupun server. Docker Compose melengkapi Docker dengan kemampuan mendefinisikan beberapa service secara deklaratif dalam satu file. Dalam proyek ini, aplikasi web, database, dan alat administrasi database dijalankan sebagai container yang terpisah tetapi tetap terhubung melalui internal network.

Selain containerization, kualitas aplikasi perlu dijaga melalui automated testing dan continuous integration. Pengujian otomatis berfungsi sebagai quality gate sebelum Docker image dibangun. Apabila test gagal, proses build tidak dilanjutkan sehingga kesalahan dapat ditemukan lebih awal. GitHub Actions digunakan untuk menjalankan proses tersebut setiap kali kode dikirim ke repository.

Berdasarkan kebutuhan tersebut, dikembangkan CloudTask, yaitu aplikasi manajemen tugas sederhana yang menerapkan operasi CRUD, validasi input, koneksi PostgreSQL, multi-container Docker Compose, persistent volume, health check, restart policy, automated testing, dan pipeline CI/CD. Kompleksitas fitur sengaja dibuat sederhana agar fokus proyek berada pada penerapan konsep cloud computing secara utuh dan dapat diverifikasi.

## 1.2 Permasalahan

Permasalahan yang diselesaikan adalah:
1. Bagaimana membangun aplikasi yang dapat menampilkan, menambahkan, mengubah, dan menghapus data pada database.
2. Bagaimana memisahkan aplikasi dan database menjadi service container yang berbeda.
3. Bagaimana mempertahankan data ketika container dihentikan dan dibuat kembali.
4. Bagaimana memeriksa kesehatan layanan dan memulihkan container ketika terjadi gangguan.
5. Bagaimana menjalankan automated testing dan Docker build secara otomatis melalui GitHub Actions.

## 1.3 Tujuan

Proyek ini bertujuan membangun CloudTask sebagai aplikasi multi-container yang mudah dijalankan, memiliki data persisten, menggunakan konfigurasi environment yang aman, dapat diuji secara otomatis, dan memiliki pipeline CI/CD yang dapat menunjukkan kondisi gagal serta berhasil.

## 1.4 Manfaat

Manfaat proyek adalah memberikan pengalaman praktis mengenai hubungan source code, Docker image, container, Docker Compose, network, volume, health check, automated testing, dan CI/CD. Proyek juga dapat menjadi dasar untuk pengembangan aplikasi yang akan dipindahkan ke VPS atau layanan cloud.

# BAB II ANALISIS DAN ARSITEKTUR

## 2.1 Deskripsi Aplikasi

CloudTask merupakan aplikasi web untuk mengelola daftar tugas. Pengguna dapat melihat seluruh tugas, menambahkan tugas baru, mengubah judul, deskripsi dan status, serta menghapus tugas. Setiap input divalidasi agar data yang masuk ke database sesuai aturan.

## 2.2 Pengguna

Aplikasi memiliki satu jenis pengguna, yaitu pengguna umum atau operator. Autentikasi tidak diterapkan karena fokus proyek berada pada implementasi cloud computing. Pada pengembangan berikutnya, autentikasi dapat ditambahkan tanpa mengubah konsep container utama.

## 2.3 Teknologi

Teknologi yang digunakan:
- Python dan Flask sebagai web framework.
- Flask-SQLAlchemy sebagai ORM.
- PostgreSQL sebagai database.
- Adminer sebagai alat pemeriksaan database.
- Gunicorn sebagai application server.
- Docker dan Docker Compose sebagai container platform dan orkestrasi lokal.
- Pytest sebagai automated testing.
- GitHub dan GitHub Actions sebagai repository dan pipeline CI/CD.

## 2.4 Arsitektur Aplikasi

Arsitektur minimal terdiri dari pengguna, aplikasi Flask, dan PostgreSQL. Proyek menggunakan satu service tambahan yaitu Adminer. Browser mengakses aplikasi melalui port 5000. Container aplikasi terhubung ke PostgreSQL menggunakan hostname `db`, yaitu nama service pada Docker Compose. Adminer mengakses database melalui network yang sama. Database menyimpan file datanya pada named volume sehingga data berada di luar lifecycle container.

**BUKTI:** Masukkan gambar diagram arsitektur dari `docs/DIAGRAM_ARSITEKTUR.md`.

## 2.5 Fungsi Setiap Container

Container `app` menjalankan source code Flask menggunakan Gunicorn. Container `db` menjalankan PostgreSQL dan menangani penyimpanan data. Container `adminer` menyediakan antarmuka web untuk memeriksa tabel dan isi database. Ketiga container dihubungkan oleh bridge network bernama `cloudtask-network`.

## 2.6 Hubungan Komponen Cloud Computing

Source code digunakan saat Docker build untuk menghasilkan image aplikasi. Image adalah template read-only yang berisi sistem dasar, dependency, dan kode aplikasi. Ketika image dijalankan, Docker membuat container sebagai instance yang aktif. Docker Compose mendefinisikan bagaimana container dibangun, port yang dipublikasikan, environment variable, network, volume, dependency antarlayanan, health check, dan restart policy.

Network menyediakan komunikasi internal antarkontainer tanpa harus mempublikasikan port database ke host. Volume menyimpan data PostgreSQL secara persisten. GitHub Actions mengambil source code dari repository, memasang dependency, menjalankan test, dan membangun Docker image ketika seluruh test berhasil.

## 2.7 Alasan Multi-Container

Pemisahan service membuat setiap komponen memiliki tanggung jawab yang jelas. Aplikasi dapat dibangun ulang tanpa menghapus database. Database dapat diperbarui atau dipelihara secara terpisah. Log dan status masing-masing service lebih mudah diperiksa. Pendekatan ini juga mengurangi konflik dependency karena aplikasi dan database memiliki runtime yang berbeda.

# BAB III IMPLEMENTASI APLIKASI

## 3.1 Struktur Folder

Struktur utama repository:
- `app/` berisi factory aplikasi, model, route, template, dan stylesheet.
- `tests/` berisi automated test.
- `.github/workflows/` berisi pipeline CI/CD.
- `Dockerfile` berisi langkah pembuatan image.
- `docker-compose.yml` berisi deklarasi seluruh service.
- `.env.example` berisi contoh environment variable.
- `docs/` berisi diagram, laporan, video, presentasi, dan checklist.

**BUKTI:** Masukkan screenshot struktur repository.

## 3.2 Model Database

Tabel `tasks` memiliki kolom `id`, `title`, `description`, `status`, dan `created_at`. Kolom judul wajib diisi. Status hanya menerima `pending`, `in_progress`, atau `done`.

## 3.3 Fitur CRUD

Halaman utama menampilkan seluruh data dari PostgreSQL. Form tambah menyimpan data baru. Form ubah memperbarui data berdasarkan ID. Tombol hapus menghapus baris dari database. Seluruh operasi dilakukan melalui ORM agar kode lebih terstruktur.

**BUKTI:** Masukkan screenshot halaman daftar, tambah, ubah, dan hasil hapus.

## 3.4 Validasi Input

Validasi dilakukan pada sisi HTML dan server. Judul wajib diisi, panjang minimal tiga karakter, dan maksimal seratus karakter. Deskripsi maksimal lima ratus karakter. Status harus termasuk nilai yang diizinkan. Validasi server tetap diperlukan karena validasi browser dapat dilewati.

**BUKTI:** Masukkan screenshot pesan validasi ketika judul kosong.

## 3.5 Konfigurasi Environment

Aplikasi membaca `DATABASE_URL` dan `SECRET_KEY` dari environment. PostgreSQL membaca nama database, username, dan password dari file `.env`. Repository hanya menyimpan `.env.example`, sedangkan `.env` dimasukkan ke `.gitignore`.

# BAB IV IMPLEMENTASI CONTAINER

## 4.1 Dockerfile

Dockerfile menggunakan base image `python:3.12-slim`. Working directory ditetapkan pada `/app`. Dependency dipasang dari `requirements.txt`, source code disalin, port 5000 diekspos, dan aplikasi dijalankan menggunakan Gunicorn. Container menggunakan user non-root sebagai praktik keamanan dasar.

**BUKTI:** Masukkan screenshot Dockerfile dan proses Docker build berhasil.

## 4.2 Docker Image

Docker image dibangun melalui perintah `docker compose up -d --build` atau melalui job Docker build pada GitHub Actions. Image menjadi paket yang konsisten karena versi Python, dependency, source code, dan command aplikasi didefinisikan dalam Dockerfile.

## 4.3 Docker Compose

Docker Compose mengelola tiga service. Service `app` dibangun dari Dockerfile. Service `db` menggunakan image PostgreSQL. Service `adminer` menggunakan image Adminer. `depends_on` dengan kondisi healthy mencegah aplikasi dijalankan sebelum database siap.

**BUKTI:** Masukkan screenshot `docker compose ps` yang memperlihatkan tiga container.

## 4.4 Network

Network `cloudtask-network` menggunakan driver bridge. Komunikasi database hanya berlangsung pada internal network. Aplikasi mengakses database dengan hostname `db`, bukan `localhost`, karena setiap container memiliki network namespace sendiri.

## 4.5 Persistent Volume

Named volume `cloudtask-postgres-data` dipasang pada `/var/lib/postgresql/data`. Ketika container database dihapus melalui `docker compose down`, volume tidak ikut dihapus. Pada saat container dibuat kembali, PostgreSQL menggunakan data pada volume yang sama.

Tanpa volume, data disimpan pada writable layer container. Apabila container dihapus, data berisiko hilang karena writable layer tersebut ikut dihapus. Oleh sebab itu, volume merupakan komponen penting untuk data yang bersifat persisten.

## 4.6 Health Check dan Restart Policy

Health check database menggunakan `pg_isready`. Health check aplikasi mengakses endpoint `/health`. Endpoint tersebut tidak hanya memeriksa proses Flask, tetapi juga menjalankan query `SELECT 1` agar koneksi database ikut diverifikasi. Restart policy `unless-stopped` membantu menjalankan kembali container ketika proses berhenti secara tidak normal.

# BAB V IMPLEMENTASI CI/CD

## 5.1 Automated Testing

Empat automated test diterapkan:
1. Memastikan endpoint health check menghasilkan status 200 dan nilai `healthy`.
2. Memastikan data valid dapat disimpan.
3. Memastikan judul kosong ditolak.
4. Memastikan proses update dan delete berjalan.

Test menggunakan SQLite sementara untuk mempercepat pengujian dan menjaga isolasi. Logika aplikasi yang diuji tetap sama dengan aplikasi produksi yang menggunakan PostgreSQL.

**BUKTI:** Masukkan screenshot `pytest -q` dengan hasil empat test berhasil.

## 5.2 Workflow GitHub Actions

Workflow memiliki dua job. Job pertama melakukan checkout, menyiapkan Python, memasang dependency, dan menjalankan Pytest. Job kedua bergantung pada job pertama dan hanya berjalan jika automated test berhasil. Job kedua membangun Docker image tanpa melakukan push ke registry.

## 5.3 Pipeline Gagal

Pipeline gagal dibuat secara terkontrol dengan mengubah sementara ekspektasi status health check dari 200 menjadi 500. GitHub Actions mendeteksi assertion error dan menghentikan workflow sebelum job Docker build. Kegagalan tersebut membuktikan fungsi automated testing sebagai quality gate.

**BUKTI:** Masukkan link dan screenshot workflow gagal serta bagian log assertion error.

## 5.4 Pipeline Berhasil

Setelah penyebab kegagalan dianalisis, assertion dikembalikan menjadi 200. Perbaikan di-commit dan di-push. GitHub Actions menjalankan kembali seluruh test. Setelah test berhasil, job Docker build dijalankan dan selesai tanpa error.

**BUKTI:** Masukkan link dan screenshot workflow berhasil.

# BAB VI PENGUJIAN

## 6.1 Pengujian Fungsi

Pengujian manual dilakukan terhadap halaman daftar, tambah, ubah, hapus, dan validasi. Seluruh fungsi berjalan dan perubahan dapat dilihat kembali pada halaman utama maupun Adminer.

## 6.2 Pengujian Container

Perintah `docker compose up -d --build` berhasil membuat image dan menjalankan tiga container. Perintah `docker compose ps` menunjukkan status service dan health check.

## 6.3 Pengujian Persistent Volume

Satu data dibuat sebelum container dihentikan. Setelah menjalankan `docker compose down`, container dihapus tetapi volume tidak dihapus. Ketika `docker compose up -d` dijalankan kembali, data yang sama masih tampil. Hasil ini membuktikan bahwa persistent volume bekerja.

**BUKTI:** Masukkan screenshot data sebelum dan sesudah restart.

## 6.4 Simulasi Kegagalan

Container aplikasi dihentikan secara paksa menggunakan `docker kill cloudtask-app`. Sesaat setelah gangguan, service tidak dapat diakses. Restart policy kemudian membuat container berjalan kembali. Health check berubah dari kondisi awal menjadi sehat setelah aplikasi dan koneksi database siap.

**BUKTI:** Masukkan screenshot command dan perubahan status.

## 6.5 Dampak Kegagalan Service

Jika service aplikasi gagal, pengguna tidak dapat mengakses antarmuka tetapi data database tetap aman. Strategi pemulihan adalah restart policy dan pemeriksaan log. Jika database gagal, endpoint health check aplikasi mengembalikan status tidak sehat karena query verifikasi tidak dapat dilakukan. Strateginya adalah memeriksa log database, kapasitas storage, environment variable, dan volume, kemudian menjalankan ulang service.

## 6.6 Rancangan Pengembangan ke Cloud

Untuk dipindahkan ke layanan cloud, image aplikasi dapat dipublikasikan ke Docker Hub atau GitHub Container Registry. Sebuah VPS dapat menjalankan Docker Compose, sedangkan Nginx digunakan sebagai reverse proxy. HTTPS dapat diterapkan dengan sertifikat TLS. Database dapat tetap dijalankan sebagai container dengan backup berkala atau dipindahkan ke managed PostgreSQL. Environment production disimpan sebagai secret, bukan di repository. Monitoring, centralized logging, backup, dan pembatasan akses network perlu ditambahkan.

# BAB VII KESIMPULAN

CloudTask berhasil menerapkan aplikasi web dengan operasi CRUD, validasi, dan koneksi database. Aplikasi, PostgreSQL, dan Adminer dijalankan sebagai service terpisah melalui Docker Compose. Persistent volume mempertahankan data, environment variable memisahkan credential dari source code, network menghubungkan service, health check memeriksa kondisi aplikasi dan database, serta restart policy membantu pemulihan layanan.

Empat automated test berhasil dijalankan secara lokal dan melalui GitHub Actions. Pipeline gagal berhasil dibuktikan melalui kesalahan test yang dibuat secara terkontrol, kemudian pipeline berhasil setelah perbaikan. Dengan demikian, proyek memenuhi kebutuhan utama implementasi Docker image, multi-container, orkestrasi lokal, automated testing, health check, dan CI/CD.

Kendala yang berpotensi muncul adalah waktu tunggu database, konflik port, kesalahan environment variable, dan image yang belum diperbarui. Solusi yang diterapkan adalah database health check, konfigurasi port melalui `.env`, pemeriksaan log, dan proses build ulang. Pengembangan berikutnya dapat mencakup autentikasi, registry image, deployment ke VPS, reverse proxy, HTTPS, backup database, monitoring, dan scaling aplikasi.

# LAMPIRAN LINK

Nama/NIM/Kelas: [ISI]  
Nama aplikasi: CloudTask  
Link repository GitHub: [ISI]  
Link pipeline gagal: [ISI]  
Link pipeline berhasil: [ISI]  
Link video demonstrasi: [ISI]  
Link image registry (opsional): [ISI]  
Link aplikasi online (opsional): [ISI]  
