import logging
import pandas as pd
import requests

# 1. Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("proses_etl.log"),
        logging.StreamHandler()
    ]
)

def extract_data():
    logging.info("--- Memulai proses EXTRACT ---")
    
    df_csv = pd.DataFrame()
    df_api = pd.DataFrame()

    # A. Ambil dari CSV
    try:
        df_csv = pd.read_csv('transaksi.csv')
        logging.info(f"Sukses baca CSV. Total baris: {len(df_csv)}")
    except FileNotFoundError:
        logging.error("Gawat! File 'transaksi.csv' tidak ditemukan.")
    except Exception as e:
        logging.error(f"Error tak terduga saat baca CSV: {e}")

    # B. Ambil dari API
    try:
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data_json = response.json()
        df_api = pd.DataFrame(data_json)
        df_api = df_api[['id', 'name', 'email']] # Ambil kolom penting saja
        
        logging.info(f"Sukses tarik API. Total user: {len(df_api)}")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Gagal koneksi ke API: {e}")
        
    print("\n--- BENTUK TABEL USER dan TRANSAKSI ---")
    print(df_api.head(3))
    print("----------------------------\n")
    print(df_csv.head(3)) 
    print("----------------------------\n")

    return df_csv, df_api

def transform_data(df_transaksi, df_user):
    logging.info("--- Memulai proses TRANSFORM ---")
    
    # Cek kelengkapan data
    if df_transaksi.empty or df_user.empty:
        logging.warning("Salah satu data kosong. Proses transform dihentikan.")
        return pd.DataFrame()

    print("\n--- BENTUK TABEL USER dan TRANSAKSI ---")
    print(df_user.head(3))
    print("----------------------------\n")
    print(df_transaksi.head(3))
    print("----------------------------\n")
    
    # 1. CLEANING NULL (Spesifik kolom 'jumlah')
    jumlah_null = df_transaksi['jumlah'].isnull().sum()
    if jumlah_null > 0:
        logging.warning(f"Ditemukan {jumlah_null} nilai NULL di kolom 'jumlah'. Mengisi dengan 0.")
        df_transaksi['jumlah'] = df_transaksi['jumlah'].fillna(0)

    # 2. MERGE (Gabungkan Transaksi + User)
    # Left Join: Data transaksi tetap ada walaupun user tidak ditemukan
    df_merged = pd.merge(df_transaksi, df_user, left_on='user_id', right_on='id', how='left')
    
    # 3. CLEANING DUPLICATE
    if df_merged.duplicated().any():
        logging.warning("Ditemukan duplikat, menghapus...")
        df_merged = df_merged.drop_duplicates()

    # 4. MEMILIH & MERAPIKAN KOLOM AKHIR
    # Kita rapikan urutannya biar enak dibaca
    df_hasil = df_merged[['transaksi_id', 'tanggal', 'name', 'email', 'jumlah']]
    
    logging.info(f"Transformasi selesai. Menghasilkan {len(df_hasil)} baris data bersih.")
    return df_hasil

def load_data(df_final):
    logging.info("--- Memulai proses LOAD ---")
    
    if df_final.empty:
        logging.warning("Data final kosong, tidak ada yang disimpan.")
        return

    nama_file = 'laporan_final.csv'
    try:
        # index=False supaya nomor baris (0,1,2) tidak ikut tersimpan
        df_final.to_csv(nama_file, index=False)
        logging.info(f"SUKSES! Data berhasil disimpan ke '{nama_file}'")
        
    except PermissionError:
        logging.error(f"Gagal simpan! File '{nama_file}' mungkin sedang dibuka. Tutup dulu filenya.")
    except Exception as e:
        logging.error(f"Gagal menyimpan: {e}")

if __name__ == "__main__":
    logging.info("Script ETL dijalankan.")
    
    try:
        # 1. Extract
        data_transaksi, data_user = extract_data()
        
        # 2. Transform (Kirim hasil extract ke sini)
        hasil_bersih = transform_data(data_transaksi, data_user)
        
        # 3. Load (Kirim hasil transform ke sini)
        load_data(hasil_bersih)
        
        logging.info("Script ETL selesai dengan sukses.")
        
    except Exception as e:
        logging.error(f"Terjadi error fatal di main block: {e}")