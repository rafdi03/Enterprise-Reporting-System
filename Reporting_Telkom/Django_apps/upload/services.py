import pandas as pd
import datetime
import subprocess
import os
from sqlalchemy import create_engine, text
from django.conf import settings
from .models import UploadBatch, FileLog
import logging

logger = logging.getLogger(__name__)

class DataIngestionService:
    def __init__(self):
        logger.info("Initializing DataIngestionService")
        db_conf = settings.DATABASES['default']
        self.db_url = f"postgresql://{db_conf['USER']}:{db_conf['PASSWORD']}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['NAME']}"
        self.engine = create_engine(self.db_url)
        logger.info("Database engine created")

    def get_suffix(self):
        now = datetime.datetime.now()
        return f"{now.day}{now.month}{str(now.year)[-2:]}"

    def process_files(self, files):
        logger.info(f"Processing {len(files)} files")
        suffix = self.get_suffix()
        table_name = f"data_raw_{suffix}"
        logger.info(f"Target table name: {table_name}")

        batch = UploadBatch.objects.create(table_name=table_name)
        logger.info(f"Created UploadBatch with id: {batch.id}")

        all_dfs = []

        for f in files:
            logger.info(f"Reading file: {f.name}")
            try:
                df = pd.read_csv(f)
            except Exception as e:
                logger.error(f"Failed to read file {f.name}: {e}")
                return False, None, f"Gagal baca file {f.name}: {str(e)}"

            clean_name = f.name.replace('.csv', '').replace(' ', '_')
            unique_id = f"{clean_name}_{suffix}"

            df['source_file_id'] = unique_id
            df['upload_timestamp'] = datetime.datetime.now()

            all_dfs.append(df)

            FileLog.objects.create(
                batch=batch,
                original_filename=f.name,
                stored_filename=unique_id,
                row_count=len(df)
            )
            logger.info(f"Logged file: {f.name}")

        if all_dfs:
            try:
                final_df = pd.concat(all_dfs, ignore_index=True)
                logger.info(f"Uploading {len(final_df)} rows to {table_name}")

                with self.engine.connect() as conn:
                    logger.info(f"Dropping table {table_name} with CASCADE if it exists")
                    conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                    conn.commit()

                final_df.to_sql(table_name, self.engine, if_exists='replace', index=False)
                logger.info("Upload to database successful")
                return True, suffix, table_name
            except Exception as e:
                logger.error(f"Failed to upload to database: {e}")
                return False, None, f"Gagal upload ke database: {str(e)}"

        logger.warning("No data to process")
        return False, None, "Tidak ada data yang bisa diproses."

    def trigger_dbt(self, suffix):
        logger.info("Triggering dbt run")
        month_name = datetime.datetime.now().strftime('%B')

        dbt_project_path = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'dbt_project'))
        dbt_executable = os.path.abspath(os.path.join(settings.BASE_DIR, '..', '.venv', 'Scripts', 'dbt.exe'))

        logger.debug(f"dbt project path: {dbt_project_path}")
        logger.debug(f"dbt executable path: {dbt_executable}")

        cmd = [
            dbt_executable, "run",
            "--project-dir", dbt_project_path,
            "--profiles-dir", dbt_project_path,
            "--vars", f'{{"date_suffix": "{suffix}", "current_month": "{month_name}"}}'
        ]
        logger.info(f"Executing dbt command: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("dbt run successful")
            logger.debug(f"dbt stdout: {result.stdout}")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            logger.error("dbt run failed")
            logger.error(f"dbt stderr: {e.stderr}")
            return False, e.stderr
