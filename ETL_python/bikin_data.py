import pandas as pd

data = {
    'transaksi_id': [101, 102, 103, 104, 105, 106],
    'user_id': [1, 2, 999, 2, 1, 5], # user_id 999 tidak ada di API (simulasi data kotor)
    'jumlah': [50000, 25000, None, 100000, 50000, 75000], # Ada None (null)
    'tanggal': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02', '2023-01-01', '2023-01-03']
}

df = pd.DataFrame(data)
df.to_csv('transaksi.csv', index=False)
print("File transaksi.csv berhasil dibuat!")