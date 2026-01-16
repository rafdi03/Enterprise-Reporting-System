from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd

class UploadServiceTest(TestCase):
    @patch('upload.services.subprocess.run')
    @patch('upload.services.pd.read_csv')
    @patch('upload.services.create_engine')
    def test_upload_and_dbt_trigger(self, mock_engine, mock_read_csv, mock_subprocess):
        # 1. Setup Mock
        mock_subprocess.return_value = MagicMock(stdout="dbt run successful", stderr="", returncode=0)
        # Mocking pandas DataFrame
        mock_read_csv.return_value = pd.DataFrame({'col1': ['val1'], 'col2': ['val2']})

        # 2. Prepare request
        # Membuat file CSV dummy di memori
        csv_content = b"col1,col2\nval1,val2"
        dummy_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

        # 3. Kirim POST request ke view
        client = Client()
        response = client.post(reverse('upload'), {'files': [dummy_file]})

        # 4. Assertions
        self.assertEqual(response.status_code, 200) # Halaman upload-nya sendiri mengembalikan 200
        self.assertIn(b"Transformasi dbt SUKSES!", response.content)

        # Cek apakah subprocess.run (untuk dbt) dipanggil
        self.assertTrue(mock_subprocess.called)

        # Cek argumen yang digunakan untuk memanggil dbt
        dbt_call_args = mock_subprocess.call_args[0][0]
        self.assertIn('run', dbt_call_args)
        self.assertIn('--project-dir', dbt_call_args)
