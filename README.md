# 🚴🏻‍♀️ Bike Sharing Dashboard 🚴🏻‍♀️

## 💡 Deskripsi Proyek
Dashboard ini dibuat untuk menganalisis data penyewaan sepeda menggunakan dataset Bike Sharing Dataset from Capital Bikeshare system, Washington D.C., USA pada tahun 2011-2012. Dashboard dibuat menggunakan Streamlit untuk memvisualisasikan hasil analisis, agar mudah dipahami dan eksploratif. 

## 📍 Tujuan Analisis
Beberapa tujuan utama dari proyek ini yaitu:
- Menganalisis tren penyewaan sepeda dari tahun 2011-2012
- Membandingkan jumlah pengguna casual dan registered
- Mengidentifikasi kondisi jumlah penyewa tertinggi
- Mengetahui faktor eksternal seperti cuaca dan musim terhadap jumlah penyewaan sepeda

## 📥 Dataset
Dataset yang digunakan berisi data penyewaan sepeda harian dengan beberapa fitur yaitu:
- dteday: Tanggal
- weekday: hari dalam seminggu 
- casual: Penyewa tidak terdaftar
- registered: Penyewa terdaftar
- cnt: total penyewa
- temp: temperatur
- weathersit: kondisi cuaca
- season: musim

## 🛠️ Tools dan Library
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit

## ⚙️ Cara Menjalankan Dashboard
Ikuti langkah langkah ini untuk menjalankan aplikasi dashboard secara lokal:
### 1️⃣ Setup Environment 
```
python -m venv .venv
.venv\Scripts\activate #Untuk pengguna Windows
source .venv/bin/activate #Untuk pengguna Linux/ Mac
pip install -r requirements.txt
```
### 2️⃣ Setup Folder Project
```
mkdir Submission
cd dashboard
```
### 3️ Run steamlit app
```
streamlit run dashboard.py
```

## 🏷️ Catatan
- Pastikan Python sudah terinstall
- Pastikan file requirements.txt tersedia
- Jika eror, cek kembali apakah virtual environment sudah aktif