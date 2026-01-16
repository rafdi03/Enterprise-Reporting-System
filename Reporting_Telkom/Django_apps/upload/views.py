from django.shortcuts import render
from django.contrib import messages
from .forms import CsvUploadForm
from .services import DataIngestionService
import logging
import csv
import json
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def upload_view(request):
    logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        logger.info("Processing POST request")
        form = CsvUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if form.is_valid() and files:
            logger.info("Form is valid and files are present")
            service = DataIngestionService()

            logger.info("Processing files")
            success, suffix, info = service.process_files(files)

            if success:
                messages.success(request, f"Upload CSV berhasil! Tabel '{info}' terbentuk.")
                logger.info("File processing successful, triggering dbt")
                messages.info(request, "Sedang menjalankan dbt transformation...")
                dbt_success, dbt_log = service.trigger_dbt(suffix)

                if dbt_success:
                    messages.success(request, "Transformasi dbt SUKSES! Data Final siap.")
                    logger.info("dbt run successful")
                else:
                    messages.error(request, "Upload sukses, tapi dbt GAGAL. Cek terminal/log.")
                    logger.error("dbt run failed")
            else:
                messages.error(request, f"Gagal: {info}")
                logger.error(f"File processing failed: {info}")

        else:
            messages.error(request, "Form tidak valid.")
            logger.error("Form is not valid or no files were uploaded")

    else:
        form = CsvUploadForm()

    return render(request, 'upload.html', {'form': form})

def report_view(request):
    """
    Menampilkan tabel reporting_telkom terbaru.
    """
    service = DataIngestionService()
    suffix = service.get_suffix() # 140126
    table_name = f"reporting_telkom_{suffix}"
    
    # Ambil data pake Raw SQL agar dinamis
    data = []
    columns = []
    
    try:
        with connection.cursor() as cursor:
            # Cek apakah tabel ada
            cursor.execute("SELECT to_regclass(%s)", [table_name])
            if cursor.fetchone()[0]:
                # Ambil semua data
                # LIMIT 1000 agar browser tidak crash jika data jutaan
                cursor.execute(f'SELECT * FROM "{table_name}" ORDER BY id ASC LIMIT 1000') 
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
                
                # Convert ke list of dict biar mudah di template
                data_list = []
                for row in data:
                    data_list.append(dict(zip(columns, row)))
            else:
                return render(request, 'report_error.html', {'msg': f"Tabel {table_name} belum ada. Silakan upload file dulu."})
                
    except Exception as e:
        return render(request, 'report_error.html', {'msg': str(e)})

    return render(request, 'report_table.html', {
        'table_name': table_name,
        'columns': columns,
        'data': data_list,
        'suffix': suffix
    })

@csrf_exempt
def update_cell_api(request):
    """
    API untuk menyimpan edit user ke Database.
    Menerima: {table, id, column, value}
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            table_name = payload.get('table_name')
            row_id = payload.get('id')
            column = payload.get('column')
            new_value = payload.get('value')
            
            # Validasi keamanan sederhana (Pastikan tabel diawali reporting_telkom)
            if not table_name.startswith('reporting_telkom_'):
                return JsonResponse({'success': False, 'msg': 'Tabel tidak valid'})

            # Update Query Raw
            with connection.cursor() as cursor:
                query = f'UPDATE "{table_name}" SET "{column}" = %s WHERE id = %s'
                cursor.execute(query, [new_value, row_id])
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})
            
    return JsonResponse({'success': False, 'msg': 'Method not allowed'})

def download_report(request, suffix, format_type):
    """
    Download CSV/Excel dari tabel
    """
    table_name = f"reporting_telkom_{suffix}"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{table_name}.csv"'
    
    writer = csv.writer(response)
    
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM "{table_name}"')
        columns = [col[0] for col in cursor.description]
        writer.writerow(columns) # Header
        
        for row in cursor.fetchall():
            writer.writerow(row)
            
    return response