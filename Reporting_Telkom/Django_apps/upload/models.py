from django.db import models

class UploadBatch(models.Model):
    """
    Menandakan satu kali kegiatan upload (misal: Upload tanggal 1 Januari).
    Ini ibarat 'Folder' logikanya.
    """
    upload_date = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=100) # Nama tabel raw di DB (misal: data_raw_1126)
    
    def __str__(self):
        return self.table_name

class FileLog(models.Model):
    """
    Mencatat detail setiap file yang ada di dalam Batch tersebut.
    """
    batch = models.ForeignKey(UploadBatch, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255) # Nama file asli (Indosat.csv)
    stored_filename = models.CharField(max_length=255)   # Nama unik di tabel (Indosat_1126)
    row_count = models.IntegerField(default=0)           # Jumlah baris data
    
    def __str__(self):
        return self.original_filename