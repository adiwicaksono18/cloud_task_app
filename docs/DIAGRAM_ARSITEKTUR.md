# Diagram Arsitektur

```mermaid
flowchart LR
    U[Pengguna / Browser]
    GH[GitHub Repository]
    GA[GitHub Actions CI]
    IMG[Docker Image Flask]
    APP[Container App Flask]
    DB[(Container PostgreSQL)]
    ADM[Container Adminer]
    VOL[(Persistent Volume)]
    NET[Docker Bridge Network]

    U -->|HTTP :5000| APP
    U -->|HTTP :8080| ADM
    APP -->|SQL :5432| DB
    ADM -->|SQL :5432| DB
    DB --> VOL

    GH --> GA
    GA -->|pytest| GA
    GA -->|docker build| IMG
    IMG --> APP

    APP --- NET
    DB --- NET
    ADM --- NET
```

Penjelasan:
- Pengguna mengakses aplikasi Flask melalui port 5000.
- Aplikasi berkomunikasi dengan PostgreSQL menggunakan nama service `db` pada internal Docker network.
- Adminer menjadi service ketiga untuk pemeriksaan database.
- Data PostgreSQL disimpan pada named volume `cloudtask-postgres-data`.
- GitHub Actions menjalankan automated testing sebelum Docker image dibangun.
