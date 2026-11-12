# Bike Sharing Analytics Dashboard

## Deskripsi Project
Project ini merupakan analisis data penyewaan sepeda menggunakan Bike Sharing Dataset periode 2011–2012. Analisis dilakukan untuk memahami pola penyewaan berdasarkan waktu, musim, dan kondisi cuaca.

Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Business Questions
1. Bagaimana pola rata-rata jumlah penyewaan sepeda per jam antara hari kerja dan akhir pekan, serta pada jam berapa permintaan tertinggi terjadi?
2. Bagaimana perbedaan rata-rata penyewaan pengguna casual dan registered pada setiap musim, serta kelompok pengguna mana yang menunjukkan perubahan permintaan paling besar antar musim?
3. Bagaimana perbedaan rata-rata penyewaan berdasarkan kondisi cuaca, serta kondisi cuaca mana yang berkaitan dengan permintaan tertinggi dan terendah?

## Dataset
- `day_data.csv`: Data penyewaan sepeda harian.
- `hour_data.csv`: Data penyewaan sepeda per jam.

## Fitur Dashboard
- Filter tahun, musim, dan kondisi cuaca.
- Ringkasan KPI penyewaan.
- Analisis penyewaan berdasarkan jam.
- Analisis penyewaan berdasarkan musim.
- Analisis penyewaan berdasarkan kondisi cuaca.
- Analisis tambahan berdasarkan kelompok waktu.
- Insight otomatis sesuai filter yang dipilih.

## Insight Utama
- Permintaan tertinggi pada hari kerja terjadi pukul 17.00.
- Permintaan tertinggi pada akhir pekan terjadi pukul 13.00.
- Pengguna registered menunjukkan perubahan penyewaan antar musim lebih besar dibanding casual.
- Kondisi cuaca Clear memiliki rata-rata penyewaan tertinggi, sedangkan Light Rain/Snow terendah.

## Cara Menjalankan Dashboard

1. Instal Python.
2. Masukkan `dashboard.py`, `day_data.csv`, `hour_data.csv`, dan `requirements.txt` dalam satu folder.
3. Instal library:

   `pip install -r requirements.txt`

4. Jalankan dashboard:

   `streamlit run dashboard.py`

## Tools
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit