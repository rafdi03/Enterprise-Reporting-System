      
import logging
import pandas as pd
import requests

# ... (Bagian Konfigurasi Logging JANGAN DIHAPUS, biarkan sama seperti sebelumnya) ...
# logging.basicConfig(...) 

def extract_data():
    logging.info("--- Memulai proses EXTRACT ---")
    
    # Wadah untuk hasil (inisialisasi kosong dulu)
    df_csv = pd.DataFrame()
    df_api = pd.DataFrame()

    # 1. EXTRACT CSV
    try:
        df_csv = pd.read_csv('transaksi.csv')
        logging.info(f"Sukses baca CSV. Total baris: {len(df_csv)}")
    except FileNotFoundError:
        logging.error("Gawat! File 'transaksi.csv' tidak ditemukan.")
    except Exception as e:
        logging.error(f"Error tak terduga saat baca CSV: {e}")

    # 2. EXTRACT API
    try:
        # Kita pakai API dummy untuk simulasi data User
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url, timeout=10) # Timeout biar gak nunggu selamanya
        
        # Cek apakah status code 200 (OK)?
        response.raise_for_status() 
        
        data_json = response.json()
        df_api = pd.DataFrame(data_json)
        # Kita cuma butuh kolom id, name, email biar simpel
        df_api = df_api[['id', 'name', 'email']]
        
        logging.info(f"Sukses tarik API. Total user: {len(df_api)}")
        
        # TAMBAHAN: Intip 3 baris pertama
        print("\n--- BENTUK TABEL API ---")
        print(df_api.head(3)) 
        print("----------------------------\n")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Gagal koneksi ke API: {e}")
    

    return df_csv, df_api

def transform_data(df_transaksi, df_user): # Perhatikan kita tambah parameter input
    logging.info("--- Memulai proses TRANSFORM ---")
    # Cek dulu apa datanya ada isinya?
    jumlah_null = df_transaksi.isnull().sum()
    if jumlah_null['jumlah'] > 0 : 
        logging.warning(f"ditemukan {jumlah_null['jumlah']} nilai NULL di data transaksi.")
        df_transaksi['jumlah'] = df_transaksi['jumlah'].fillna(0)
        logging.info("Nilai NULL di kolom 'jumlah' diisi dengan 0.")
    
    df_merged = pd.merge(df_transaksi, df_user, left_on='user_id', right_on='id', how='left')
    logging.info("Data siap diproses...")
    if df_merged.duplicated().any():
        logging.warning("Ditemukan data duplikat setelah merge. Menghapus duplikat...")
        df_merged = df_merged.drop_duplicates()
    df_hasil = df_merged[['transaksi_id', 'user_id', 'name', 'email', 'jumlah']]
    logging.info("Transformasi data selesai. menghasilkan {} baris.".format(len(df_hasil)))
    logging.info(f"Contoh data hasil transformasi:\n{df_hasil.to_string(index=False)}")
    return df_hasil
# 1. Konfigurasi Logging
# Kita atur agar log dicatat ke file 'proses_etl.log' DAN juga muncul di layar
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("proses_etl.log"), # Simpan ke file
        logging.StreamHandler()                # Tampilkan di terminal
    ]
)

def load_data():
    logging.info("--- Memulai proses LOAD ---")
    # Nanti logika simpan data di sini
    pass

if __name__ == "__main__":
    logging.info("Script ETL dijalankan.")
    
    try:
        # Perhatikan alur data: Output extract -> Input transform
        data_transaksi, data_user = extract_data()
        
        # Kirim hasil extract ke transform
        hasil_bersih = transform_data(data_transaksi, data_user)
        
        load_data()
        logging.info("Script ETL selesai dengan sukses.")
        
    except Exception as e:
        logging.error(f"Terjadi error fatal: {e}")

