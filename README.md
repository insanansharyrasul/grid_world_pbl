# Grid World Search - Navigasi Robot Pertanian

## Daftar Isi
- [Grid World Search - Navigasi Robot Pertanian](#grid-world-search---navigasi-robot-pertanian)
  - [Daftar Isi](#daftar-isi)
  - [Fitur Utama](#fitur-utama)
  - [Instalasi](#instalasi)
    - [Prasyarat](#prasyarat)
    - [Langkah Instalasi](#langkah-instalasi)
  - [Cara Penggunaan](#cara-penggunaan)
    - [1. Memilih Dataset](#1-memilih-dataset)
    - [2. Melihat Peta Awal](#2-melihat-peta-awal)
    - [3. Memilih Algoritma](#3-memilih-algoritma)
      - [Opsi 1-4: Jalankan Algoritma Tunggal](#opsi-1-4-jalankan-algoritma-tunggal)
      - [Opsi 5: Run All Algorithms (Comparison)](#opsi-5-run-all-algorithms-comparison)
  - [Format Dataset](#format-dataset)
    - [Contoh Dataset dengan Berbagai Ukuran](#contoh-dataset-dengan-berbagai-ukuran)
  - [Tips Penggunaan](#tips-penggunaan)
  - [Troubleshooting](#troubleshooting)
    - [Program stuck saat menjalankan algoritma](#program-stuck-saat-menjalankan-algoritma)
    - [Visualisasi tidak muncul dengan benar](#visualisasi-tidak-muncul-dengan-benar)
    - [Error "File not found"](#error-file-not-found)

---

## Fitur Utama

- **3 Algoritma Pencarian:**
  - BFS (Breadth-First Search)
  - UCS (Uniform Cost Search)
  - A* dengan 2 heuristik (Manhattan & Euclidean)

- **Mode Perbandingan:** Jalankan semua algoritma sekaligus dan lihat tabel perbandingan performa

- **Visualisasi Step-by-Step:** Lihat proses pencarian algoritma secara real-time (opsional)

- **Analisis Performa Lengkap:**
  - Waktu eksekusi
  - Jumlah node yang dikunjungi
  - Total cost jalur
  - Perbandingan efisiensi

-  **Multi Dataset:** 10 skenario grid berbeda untuk pengujian

---

## Instalasi

### Prasyarat
- Python 3.7 atau lebih baru
- Sistem operasi: Linux, macOS, atau Windows

### Langkah Instalasi

1. **Clone repository:**
   ```bash
   git clone https://github.com/insanansharyrasul/grid_world_pbl.git
   cd grid_world_pbl
   ```

2. **Struktur folder:**
   ```
   grid_world_pbl/
   ├── src/
   │   ├── main.py              # Program utama
   │   ├── grid_environment.py  # Representasi grid dan visualisasi
   │   ├── bfs.py               # Algoritma BFS
   │   ├── ucs.py               # Algoritma UCS
   │   ├── a_star.py            # Algoritma A*
   │   └── utils.py             # MinHeap dan utilitas lain
   └── datasets/
       ├── dataset0.txt         # Grid 5x5
       ├── dataset1.txt         # Grid 10x10
       └── ...
   ```

3. **Jalankan program:**
   ```bash
   cd src
   python main.py
   ```

---

## Cara Penggunaan

### 1. Memilih Dataset

Saat program dijalankan, Anda akan melihat menu pemilihan dataset:

```
============================================================
DAFTAR DATASET TERSEDIA
============================================================
  1. dataset0.txt
  2. dataset1.txt
  3. dataset2.txt
  ...
  0. Keluar
============================================================
Pilih dataset (masukkan nomor): 
```

**Ketik nomor** dataset yang ingin digunakan (contoh: `1` untuk dataset0.txt).

---

### 2. Melihat Peta Awal

Setelah memilih dataset, peta akan ditampilkan:

```
============================================================
 S   .   &   @   . 
 .   #       #   & 
 &   #   @   #   . 
 .   &   .   #   @ 
 G   .   &   .   . 
============================================================
```

**Keterangan Warna:**
- **S** (hijau terang) = Start
- **G** (biru) = Goal
- **#** (merah) = Rintangan
- **@** (kuning) = Tanah Gembur (cost 3)
- **&** (magenta) = Tanah Lumpur (cost 15)
- **.** (putih) = Tanah Kering (cost 1)

---

### 3. Memilih Algoritma

Anda akan melihat menu algoritma:

```
============================================================
PILIH ALGORITMA
============================================================
  1. BFS (Breadth-First Search)
  2. UCS (Uniform Cost Search)
  3. A* (Manhattan Heuristic)
  4. A* (Euclidean Heuristic)
  5. Run All Algorithms (Comparison)
  0. Kembali
============================================================
Pilih algoritma (masukkan nomor): 
```

#### Opsi 1-4: Jalankan Algoritma Tunggal

Setelah memilih algoritma (1-4), Anda akan ditanya:

```
Aktifkan visualisasi step-by-step? (y/n):
```

- **Ketik `y`:** Proses pencarian ditampilkan langkah demi langkah (animasi)
- **Ketik `n`:** Langsung menampilkan hasil akhir

#### Opsi 5: Run All Algorithms (Comparison)

Mode ini menjalankan **semua algoritma sekaligus** dan menampilkan perbandingan.

---

## Format Dataset

Dataset disimpan dalam file `.txt` di folder `datasets/`. Format:

```
[ukuran_baris] [ukuran_kolom]
S . & @ .
. # . # &
& # @ # .
. & . # @
G . & . .
```

**Aturan:**
1. Baris pertama: dimensi grid (opsional)
2. Baris berikutnya: isi grid dengan spasi sebagai pemisah
3. Harus ada **tepat satu** `S` (Start) dan **satu** `G` (Goal)
4. Simbol yang valid: `S`, `G`, `.`, `@`, `&`, `#`

### Contoh Dataset dengan Berbagai Ukuran

**Dataset kecil (5x5):**
```
5 5
S . . . .
. # . # .
. . . . .
. # # # .
. . . . G
```

**Dataset besar (10x10):**
```
10 10
S . . @ & . . . @ .
. # . # & . # . # .
. . @ . . . . @ . .
@ # # # . . # # # &
. . . . . . . . . .
& @ . # # # . @ & .
. . . . . . . . . @
. # # . @ . # # . .
@ . & . . . & . @ .
. . . . . . . . . G
```
---

## Tips Penggunaan

1. **Untuk dataset kecil (5x5 - 7x7):** Aktifkan visualisasi step-by-step untuk memahami cara kerja algoritma
2. **Untuk dataset besar (>10x10):** Nonaktifkan visualisasi agar lebih cepat
3. **Untuk analisis performa:** Gunakan opsi 5 (Run All Algorithms)
4. **Untuk laporan:** Screenshot tabel perbandingan dan analisis performa

---


## Troubleshooting

### Program stuck saat menjalankan algoritma
- **Penyebab:** Dataset terlalu besar atau tidak ada jalur
- **Solusi:** Coba dataset lebih kecil atau cek apakah ada jalur valid

### Visualisasi tidak muncul dengan benar
- **Penyebab:** Terminal tidak mendukung ANSI color codes
- **Solusi:** Gunakan terminal modern (tidak mendukung cmd Windows lama)

### Error "File not found"
- **Penyebab:** Program tidak dijalankan dari folder `src/`
- **Solusi:** 
  ```bash
  cd src
  python main.py
  ```
