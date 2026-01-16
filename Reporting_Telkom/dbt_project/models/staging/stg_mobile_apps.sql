{{ config(materialized='view') }}

SELECT
    -- ID Unik
    MD5(COALESCE(package_name, '') || source_file_id || row_number() OVER ()) as id,
    
    -- Metadata File
    source_file_id AS source_filename,
    
    -- DISPLAY COLUMNS (Huruf Asli)
    TRIM(commercial_name) AS commercial_name,
    TRIM(package_name)    AS package_name,
    
    -- === PERBAIKAN UTAMA: FORMAT JSON RAW ===
    -- Kita gabungkan main_detail dan package_description dengan format khusus
    -- Hasil: ""main_detail"": Isinya... || ""package_description"": Isinya...
    '""main_detail"": ' || COALESCE(CAST(main_detail AS TEXT), '-') || ' || ""package_description"": ' || COALESCE(CAST(package_description AS TEXT), '-') AS description_combined_raw,
    
    -- Kolom Description Clean (Untuk Logic dbt saja, atau kolom tambahan)
    LOWER(TRIM(COALESCE(CAST(package_description AS TEXT), CAST(main_detail AS TEXT), ''))) AS description_clean,
    
    TRIM(CAST(benefit_detail AS TEXT)) AS benefit_detail,
    
    -- LOGIC COLUMNS (Huruf Kecil untuk Regex)
    LOWER(TRIM(commercial_name)) AS commercial_name_clean,
    LOWER(TRIM(package_name))    AS package_name_clean,
    
    LOWER(TRIM(COALESCE(CAST(benefit_app AS TEXT), '')))        AS benefit_app_clean,
    LOWER(TRIM(COALESCE(CAST(benefit_detail AS TEXT), '')))     AS benefit_detail_clean,
    LOWER(TRIM(COALESCE(CAST(main_detail AS TEXT), '')))        AS main_detail_clean,
    
    -- Cleaning Price
    CAST(
        NULLIF(
            REGEXP_REPLACE(CAST(price AS TEXT), '[^0-9]', '', 'g'), 
            ''
        ) AS NUMERIC
    ) AS price_clean,
    
    validity

FROM {{ target.schema }}."data_raw_{{ var('date_suffix') }}"
WHERE package_name IS NOT NULL