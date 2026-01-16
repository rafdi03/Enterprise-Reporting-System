{{ config(materialized='view') }}

WITH src AS (
    SELECT 
        *,
        SUBSTRING(source_filename FROM '202[0-9]{5}') AS file_date_token_found
    FROM {{ ref('stg_mobile_apps') }}
)

SELECT
    *,
    -- Metadata
    'Mobile Apps' AS channel_final,
    SPLIT_PART(source_filename, '_', 1) AS operator_final,
    
    -- Date Fix
    CASE 
        WHEN file_date_token_found IS NOT NULL 
        THEN TO_DATE(file_date_token_found, 'YYYYMMDD')
        ELSE CURRENT_DATE 
    END AS file_date,

    -- LoS Logic
    CASE 
        WHEN source_filename LIKE '%less3%' THEN 'less_than_3_months'
        WHEN source_filename LIKE '%more3%' THEN 'more_than_3_months'
        ELSE 'unknown'
    END AS los_group_final,
    
    CASE 
        WHEN source_filename LIKE '%less3%' THEN 'less3'
        WHEN source_filename LIKE '%more3%' THEN 'more3'
        ELSE 'unknown'
    END AS los_token,
    
    -- Region & City
    SPLIT_PART(source_filename, '_', 2) AS city_token,
    
    CASE
        WHEN LOWER(source_filename) ~ '(medan|sumatera|padang|palembang|aceh|pekanbaru|batam|lampung)' THEN 'Area 1'
        WHEN LOWER(source_filename) ~ '(jakarta|jabo|jabodetabek|bogor|depok|tangerang|bekasi|jaksel)' THEN 'Area 2'
        WHEN LOWER(source_filename) ~ '(jateng|jaktim|lombok|semarang|solo|yogyakarta|surabaya|malang|denpasar|bali)' THEN 'Area 3'
        ELSE 'Area 4'
    END AS region_final,

    -- EXTRACTION
    COALESCE(
        {{ extract_days('package_name_clean') }},
        {{ extract_days('description_clean') }},
        CAST(validity AS INT),
        0
    ) AS validity_final,

    {{ extract_gb('description_clean') }} AS gb_from_desc,
    {{ extract_gb('benefit_detail_clean') }} AS gb_from_benefit,
    {{ extract_gb('package_name_clean') }}   AS gb_from_name

FROM src