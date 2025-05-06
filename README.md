# 📘 Dokumentasi Tugas Besar CLO2 Konstruksi Perangkat Lunak

## 🔁 Clone Proyek

Untuk mengunduh source code proyek ini, jalankan perintah berikut di terminal:

```bash
git clone https://github.com/gideonladiyo/CLO2_TB_KPL.git
cd CLO2_TB_KPL
```

---

## 📁 Setup Proyek

Buka terminal proyek, lalu jalankan command:

```bash
pip install -r requirements.txt
```

Seluruh library yang diperlukan di proyek ini akan dinstall terlebih dahulu.

---

## 🚀 Menjalankan API

Setelah masuk ke direktori proyek, jalankan perintah berikut untuk menjalankan API:

```bash
uvicorn app.main:app --port 5151 --reload
```

* `--port 5151` menentukan port untuk API.
* `--reload` memungkinkan hot-reload saat pengembangan.

---

## ✅ Menjalankan Unit Testing

Untuk menjalankan unit test, jalankan perintah berikut dari root direktori proyek:

```bash
pytest -p no:warning
```

* Flag `-p no:warning` digunakan untuk menghilangkan warning output saat testing. Jika tidak menggunakan `-p no:warning` akan terlihat warning yang disebabkan oleh beberapa library yang digunakan.

---

## ⚙️ Performance Testing dengan K6

### 1. Install K6

#### 🔵 Windows

* Pastikan Chocolatey sudah terinstall untuk menginstall K6. Jika belum, instal terlebih dahulu dari:
👉[https://chocolatey.org/install](https://chocolatey.org/install)
* Buka Powershell dan pastikan buka sebagai administrator.
* Jalankan command:

    ```bash
    Get-ExecutionPolicy
    ```

    Jika hasilnya "Restricted", jalankan command berikut:

    ```bash
    Set-ExecutionPolicy AllSigned
    ```

* Lalu jalankan command:

    ```bash
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

* Periksa apakah choco sudah terinstall dengan menjalankan command:

    ```bash
    choco --version
    ```

* Kemdian buka terminal sebagai Administrator, lalu jalankan command:

    ```bash
    choco install k6
    ```

* Setelah diinstall cek k6 dengan command:

    ```bash
    k6 version
    ```

#### 🍏 macOS

Jika menggunakan Homebrew:

```bash
brew install k6
```

#### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install gnupg ca-certificates
curl -s https://dl.k6.io/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/k6-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt update
sudo apt install k6
```

> Untuk distribusi Linux lainnya, silakan lihat [panduan resmi K6](https://k6.io/docs/getting-started/installation/).

---

### 2. Menjalankan Performance Test

1. Jalankan API terlebih dahulu:

   ```bash
   uvicorn app.main:app --port 5151 --reload
   ```

2. Tanpa menghentikan API yang sedang berjalan, jalankan script K6 pada file `k6_testing.py` di direktori `app/tests/performance_test/`

#### Peringatan

* Sebelum melakukan run performance testing, pastikan dua data barang teratas pada file `items.json` di direktori `app/data/` memiliki stock yang cukup untuk melakukan performance testing.
* Pastikan juga bahwa `MAX_ORDERS_PER_DAY` pada file `.env` sudah diubah sekitar 2000 agar cukup melakukan performance testing.
