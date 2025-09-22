# FFMC-SPARTAN-BMKG: Tabulasi Data FFMC per Kecamatan

Proyek ini menyediakan solusi untuk mengolah dan menabulasikan data **FMC (Fine Fuel Moisture Content)** dari produk **SPARTAN BMKG** ([https://spartan.bmkg.go.id/](https://spartan.bmkg.go.id/)).

Alat ini akan membaca file data dari SPARTAN BMKG dan menghasilkan file **CSV** yang berisi data FFMC yang sudah terpilah (clipping) berdasarkan kecamatan di provinsi yang Anda pilih.

### Fitur

* Mengubah data FFMC dari SPARTAN BMKG menjadi format CSV.
* Memisahkan data FFMC per kecamatan untuk provinsi yang Anda tentukan.
* Memuat semua parameter FFMC yang relevan.

---

### Cara Penggunaan

Proyek ini sangat mudah digunakan. Ikuti langkah-langkah berikut:

#### 1. Persiapan Data

Pastikan Anda telah mengunduh data dari halaman **Download Data** SPARTAN BMKG ([https://spartan.bmkg.go.id/Download-Data](https://spartan.bmkg.go.id/Download-Data)) dan letakkan file tersebut di dalam folder proyek ini. Jika anda mendownload file dalam .zip pastikan untuk melakukan ekstraksi terlebih dahulu.
Ekstrak data shp ke dalam folder kerja, jika anda meletakkan shp di folder lain masukkan path shp pada argument `--shapefile`.

#### 2. Menjalankan Skrip

Buka terminal Anda dan jalankan skrip dengan sintaks berikut:

```bash
python3 ./process_ffmc.py --input {nama_file_input} --province {nama_provinsi}
```
atau
```bash
python3 ./process_ffmc.py --input {nama_file_input} --province {nama_provinsi} --shapefile {path_shapefile}
```

# Contoh
```bash
python3 ./process_ffmc.py --input ./ffmc_gsmap20250705.csv --province "KALIMANTAN BARAT"
```

