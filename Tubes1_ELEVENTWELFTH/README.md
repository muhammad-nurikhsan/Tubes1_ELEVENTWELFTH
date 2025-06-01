# TUGAS BESAR STRATEGI ALGORITMA IF 2211

## Pemanfaatan Algoritma Greedy dalam Pembuatan Bot Permainan Diamonds

## I. Algoritma Greedy yang Diimplementasikan

Bot ini menggunakan pendekatan algoritma greedy dengan strategi utama memilih diamond berdasarkan rasio poin terhadap jarak (density). Bot akan selalu mengejar diamond yang paling menguntungkan secara lokal. Jika tidak tersedia diamond yang layak, bot akan memanfaatkan red button atau teleportasi sebagai opsi alternatif. Bot juga secara otomatis kembali ke base saat inventory penuh atau waktu hampir habis untuk menghindari kehilangan poin.

## II. Requirement Program dan Instalasi

Untuk menjalankan game Diamonds dan bot ini, Anda memerlukan:

- Node.js: https://nodejs.org/en
- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Yarn: dapat diinstal melalui perintah berikut

```sh
npm install --global yarn
```

- Python: https://www.python.org/downloads/

## III. Cara Menjalankan Program

### Menjalankan Game Engine

1. Download dan extract release game engine.
2. Masuk ke direktori utama proyek (misal `tubes1-IF2110-game-engine-1.1.0`).
3. Jalankan perintah berikut di terminal:

```sh
yarn
./scripts/copy-env.bat             # Windows
chmod +x ./scripts/copy-env.sh     # Linux/macOS
./scripts/copy-env.sh
```

4. Jalankan database:

```sh
docker compose up -d database
```

5. Setup database:

```sh
./scripts/setup-db-prisma.bat              # Windows
chmod +x ./scripts/setup-db-prisma.sh      # Linux/macOS
./scripts/setup-db-prisma.sh
```

6. Build dan jalankan game engine:

```sh
npm run build
npm run start
```

7. Akses frontend di browser melalui: http://localhost:8082/

### Menjalankan Bot

1. Download dan extract bot starter pack.
2. Masuk ke direktori utama bot (misal `tubes1-IF2110-bot-starter-pack-1.0.1`).
3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Jalankan bot:

```sh
python main.py --logic Ochobot --email=bot@email.com --name=ochobot --password=123 --team=etimo
```

> Pastikan `Ochobot` sudah didaftarkan dalam file `main.py` pada dictionary `CONTROLLERS`.

## IV. Author

| Nama                     | NIM       |
| ------------------------ | --------- |
| Devina Kartika           | 123140036 |
| Muhammad Nurikhsan       | 123140057 |
| Aryasatya Widyanta Akbar | 123140164 |
