import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Setup koneksi ke database Postgres Anda
# Format: postgresql+pg8000://username:password@host:port/database_name
engine = create_engine('postgresql+pg8000://postgres:Aryaguna2022@localhost:5432/ecom')

# 2. Lokasi folder CSV Anda (sesuaikan dengan path di komputer Anda)
folder_path = r'C:\Users\aryag\Downloads\archive (1)'

# 3. Loop semua file di folder dan import
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        # Buat nama tabel dari nama file (hilangkan .csv dan _dataset biar rapi)
        table_name = file.replace('.csv', '').replace('_dataset', '')
        
        print(f"Mengimpor {file} ke tabel {table_name}...")
        
        # Baca CSV
        file_full_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_full_path)
        
        # Masukkan ke SQL (if_exists='replace' akan membuat tabel baru/menimpa)
        df.to_sql(table_name, engine, index=False, if_exists='replace')

print("Selesai!")