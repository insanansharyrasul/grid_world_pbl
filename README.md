# Grid World Search - Navigasi Robot Pertanian

Proyek ini mengimplementasikan dan membandingkan tiga algoritma pencarian jalur (*pathfinding*) untuk navigasi robot di lahan pertanian berbentuk grid: **BFS (Breadth-First Search)**, **UCS (Uniform Cost Search)**, dan **A\* (A-Star)**.

## 📋 Daftar Isi
- [Deskripsi Masalah](#deskripsi-masalah)
- [Fitur Utama](#fitur-utama)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Penjelasan Output](#penjelasan-output)
- [Format Dataset](#format-dataset)
- [Algoritma yang Digunakan](#algoritma-yang-digunakan)

---

## 🎯 Deskripsi Masalah

Robot pertanian harus mencari jalur dari titik **Start (S)** ke titik **Goal (G)** di area lahan berbentuk grid dengan berbagai jenis terrain:

| Simbol | Deskripsi           | Bobot (Cost)           |
| ------ | ------------------- | ---------------------- |
| `.`    | Tanah Kering        | 1                      |
| `@`    | Tanah Gembur        | 3                      |
| `&`    | Tanah Lumpur        | 15                     |
| `#`    | Rintangan           | ∞ (Tidak bisa dilalui) |
| `S`    | Start (Posisi Awal) | 1                      |
| `G`    | Goal (Tujuan)       | 1                      |

**Tujuan:** Menemukan jalur dengan **total cost terendah** sambil menghindari rintangan.

---

## ✨ Fitur Utama

- ✅ **3 Algoritma Pencarian:**
  - BFS (Breadth-First Search)
  - UCS (Uniform Cost Search)
  - A* dengan 2 heuristik (Manhattan & Euclidean)

- 📊 **Mode Perbandingan:** Jalankan semua algoritma sekaligus dan lihat tabel perbandingan performa

- 🎬 **Visualisasi Step-by-Step:** Lihat proses pencarian algoritma secara real-time (opsional)

- 📈 **Analisis Performa Lengkap:**
  - Waktu eksekusi
  - Jumlah node yang dikunjungi
  - Total cost jalur
  - Perbandingan efisiensi

- 🗂️ **Multi Dataset:** 10 skenario grid berbeda untuk pengujian

---

## 🚀 Instalasi

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

## 📖 Cara Penggunaan

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
- 🟢 **S** (hijau terang) = Start
- 🔵 **G** (biru) = Goal
- 🔴 **#** (merah) = Rintangan
- 🟡 **@** (kuning) = Tanah Gembur (cost 3)
- 🟣 **&** (magenta) = Tanah Lumpur (cost 15)
- ⚪ **.** (putih) = Tanah Kering (cost 1)

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

## 📊 Penjelasan Output

### Output untuk Algoritma Tunggal (Opsi 1-4)

Setelah algoritma selesai, Anda akan melihat output seperti ini:

```
============================================================
RINGKASAN HASIL - A* (Manhattan)
============================================================

Status: SUCCESS - Jalur ditemukan!
Total Cost: 21
Nodes Visited: 15
Path Length: 9 langkah
Execution Time: 0.2451 ms
Throughput: 61.20 nodes/ms

Jalur yang Ditemukan:
(0,0) -> (1,0) -> (2,0) -> (3,0) -> (3,1) -> (3,2) -> (4,2) -> (4,1) -> (4,0)

Format Output Standar:
Path (A* (Manhattan), cost=21): (0,0) -> (1,0) -> (2,0) -> (3,0) -> (3,1) -> (3,2) -> (4,2) -> (4,1) -> (4,0)

Ringkasan:
A* (Manhattan): 15 node, cost 21, 0.2451 ms
============================================================
```

**Penjelasan:**
- **Status:** Apakah jalur berhasil ditemukan
- **Total Cost:** Jumlah bobot terrain yang dilewati (semakin rendah semakin baik)
- **Nodes Visited:** Jumlah sel yang diperiksa algoritma (semakin sedikit semakin efisien)
- **Path Length:** Panjang jalur dalam jumlah langkah
- **Execution Time:** Waktu yang dibutuhkan algoritma (dalam milidetik)
- **Throughput:** Efisiensi (nodes per ms)
- **Jalur yang Ditemukan:** Urutan koordinat dari Start ke Goal

#### Visualisasi Step-by-Step (jika diaktifkan)

Jika Anda mengaktifkan visualisasi (`y`), layar akan menampilkan proses pencarian secara real-time:

```
============================================================
 S   .   &   @   . 
 .   #       #   & 
 &   #   @   #   . 
 .   &   X   #   @     <- X menunjukkan node yang sedang diproses
 G   .   &   .   . 
============================================================
Current Cost: 16
Nodes Visited: 12
============================================================
```

**Simbol tambahan:**
- 🟨 **X** (kuning terang) = Node yang sedang diproses
- 🟩 **\*** (hijau) = Bagian dari jalur yang ditemukan
- 🔲 **. (abu-abu)** = Node yang sudah dikunjungi

---

### Output untuk Run All Algorithms (Opsi 5)

Mode ini memberikan **analisis perbandingan lengkap**:

#### 1. Progress Eksekusi
```
[1/4] Running BFS (Breadth First Search)...
✓ BFS: 24 nodes, cost 21, 0.3215 ms

[2/4] Running UCS (Uniform Cost Search)...
✓ UCS: 18 nodes, cost 21, 0.2890 ms

[3/4] Running A* (Manhattan Heuristic)...
✓ A* (Manhattan): 15 nodes, cost 21, 0.2451 ms

[4/4] Running A* (Euclidean Heuristic)...
✓ A* (Euclidean): 16 nodes, cost 21, 0.2567 ms
```

#### 2. Tabel Perbandingan
```
================================================================================
TABEL PERBANDINGAN ALGORITMA
================================================================================

Algoritma            Status       Cost       Nodes      Time (ms)      
--------------------------------------------------------------------------------
BFS                  SUCCESS      21.00      24         0.3215         
UCS                  SUCCESS      21.00      18         0.2890         
A* (Manhattan)       SUCCESS      21.00      15         0.2451         
A* (Euclidean)       SUCCESS      21.00      16         0.2567         
================================================================================
```

#### 3. Analisis Performa

**a) Analisis Waktu Eksekusi:**
```
1. ANALISIS WAKTU EKSEKUSI:
   Tercepat: A* (Manhattan) - 0.2451 ms
   Terlambat: BFS - 0.3215 ms
   Rata-rata: 0.2781 ms
   Speedup: A* (Manhattan) 1.31x lebih cepat dari BFS
```

**b) Analisis Efisiensi Node:**
```
2. ANALISIS EFISIENSI NODE:
   Paling Efisien: A* (Manhattan) - 15 nodes
   Kurang Efisien: BFS - 24 nodes
   Rata-rata: 18.3 nodes
   Efisiensi: A* (Manhattan) mengeksplorasi 37.5% lebih sedikit node
```

**c) Analisis Optimality (Cost):**
```
3. ANALISIS OPTIMALITY (COST):
   Cost Terendah: BFS - 21
   Cost Tertinggi: BFS - 21
   Algoritma Optimal: BFS, UCS, A* (Manhattan), A* (Euclidean) (semua menemukan path optimal)
```

**d) Ringkasan Hasil:**
```
4. RINGKASAN HASIL:
   BFS: 24 node, cost 21, 0.3215 ms
   UCS: 18 node, cost 21, 0.2890 ms
   A* (Manhattan): 15 node, cost 21, 0.2451 ms
   A* (Euclidean): 16 node, cost 21, 0.2567 ms
```

#### 4. Algoritma Terbaik
```
ALGORITMA TERBAIK:
   A* (Manhattan)
   └─ Cost: 21
   └─ Nodes: 15
   └─ Time: 0.2451 ms

Path (A* (Manhattan), cost=21): (0,0) -> (1,0) -> (2,0) -> (3,0) -> (3,1) -> (3,2) -> (4,2) -> (4,1) -> (4,0)
```

#### 5. Visualisasi Jalur Terbaik
```
Visualisasi Jalur Terbaik (A* (Manhattan)):
============================================================
 S   .   &   @   . 
 *   #       #   & 
 *   #   @   #   . 
 *   *   *   #   @ 
 G   *   *   .   . 
============================================================
```

Jalur ditandai dengan simbol **\*** berwarna hijau.

---

## 📁 Format Dataset

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

## 🧠 Algoritma yang Digunakan

### 1. BFS (Breadth-First Search)
- **Kategori:** Uninformed Search
- **Strategi:** Eksplorasi level-by-level (melebar)
- **Struktur Data:** Queue (FIFO)
- **Optimality:** ✅ Optimal pada graph dengan bobot seragam
- **Kelebihan:** Sederhana, menjamin jalur terpendek (dalam jumlah langkah)
- **Kekurangan:** Tidak mempertimbangkan cost, bisa lambat pada grid besar

### 2. UCS (Uniform Cost Search)
- **Kategori:** Uninformed Search
- **Strategi:** Eksplorasi berdasarkan cost terendah
- **Struktur Data:** Priority Queue (diurutkan berdasarkan `g(n)`)
- **Optimality:** ✅ Selalu optimal
- **Kelebihan:** Mempertimbangkan cost, optimal untuk weighted graph
- **Kekurangan:** Tidak menggunakan informasi goal, bisa lambat

### 3. A* (A-Star)
- **Kategori:** Informed Search
- **Strategi:** Eksplorasi berdasarkan `f(n) = g(n) + h(n)`
  - `g(n)`: Cost dari start ke node saat ini
  - `h(n)`: Estimasi cost dari node saat ini ke goal (heuristik)
- **Struktur Data:** Priority Queue (diurutkan berdasarkan `f(n)`)
- **Optimality:** ✅ Optimal jika heuristik admissible & consistent

#### Heuristik yang Tersedia:

**a) Manhattan Distance (Recommended)**
```
h(n) = |x_current - x_goal| + |y_current - y_goal|
```
- Cocok untuk grid dengan pergerakan 4-arah (atas, bawah, kiri, kanan)
- Admissible: tidak pernah overestimate jarak sebenarnya

**b) Euclidean Distance**
```
h(n) = √((x_current - x_goal)² + (y_current - y_goal)²)
```
- Jarak garis lurus
- Kurang cocok untuk grid dengan pergerakan terbatas (underestimate)

**Kelebihan A\*:**
- Paling efisien (mengeksplorasi node paling sedikit)
- Optimal dan complete
- Menggunakan informasi goal untuk memandu pencarian

**Kekurangan A\*:**
- Perlu desain heuristik yang baik
- Memory usage lebih tinggi

---

## 🎓 Konsep AI yang Diuji

1. **State-Space Search:** Representasi masalah sebagai ruang state
2. **Informed vs Uninformed Search:** Perbandingan algoritma dengan dan tanpa heuristik
3. **Heuristic Design:** Pemilihan fungsi heuristik yang tepat
4. **Optimality & Completeness:** Jaminan menemukan solusi optimal
5. **Time & Space Complexity:** Analisis efisiensi algoritma

---

## 📝 Tips Penggunaan

1. **Untuk dataset kecil (5x5 - 7x7):** Aktifkan visualisasi step-by-step untuk memahami cara kerja algoritma
2. **Untuk dataset besar (>10x10):** Nonaktifkan visualisasi agar lebih cepat
3. **Untuk analisis performa:** Gunakan opsi 5 (Run All Algorithms)
4. **Untuk laporan:** Screenshot tabel perbandingan dan analisis performa

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran (Project-Based Learning - PBL) mata kuliah Artificial Intelligence.

---

## 🐛 Troubleshooting

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

---

**Happy Pathfinding! 🚜🌾**
