{{ config(materialized='view') }}

WITH base AS (
    SELECT * FROM {{ ref('int_base_extraction') }}
),

logic_apply AS (
    SELECT
        *,
        -- LOGIC RULES (Gunakan _clean columns untuk logic)
        CASE
            WHEN description_clean LIKE '%fun services%' 
                 AND package_name_clean LIKE '%genflix%' 
                 AND package_name_clean NOT LIKE '%susun gambar%' 
                 AND package_name_clean NOT LIKE '%popgames%' 
            THEN 'other_video'

            WHEN (description_clean LIKE '%klikfilm%' OR description_clean LIKE '%lionsgate%' 
                  OR description_clean LIKE '%viu%' OR description_clean LIKE '%vision plus%' 
                  OR description_clean LIKE '%other video%')
                 AND description_clean NOT LIKE '%trivia%'
            THEN 'other_video'

            WHEN description_clean LIKE '%trivia time%' 
                 AND package_name_clean NOT LIKE '%match quiz 3 days%'
            THEN 'games'

            WHEN package_name_clean LIKE '%youtube%' OR description_clean LIKE '%youtube%' 
            THEN 'youtube'

            WHEN package_name_clean LIKE '%game%' OR description_clean LIKE '%mobile legends%' 
                 OR description_clean LIKE '%free fire%' OR description_clean LIKE '%pubg%'
            THEN 'games'

            WHEN package_name_clean LIKE '%sosmed%' OR description_clean LIKE '%whatsapp%' 
                 OR description_clean LIKE '%facebook%' OR description_clean LIKE '%instagram%'
                 OR description_clean LIKE '%tiktok%'
            THEN 'chat_socmed'
            
            WHEN package_name_clean LIKE '%night%' OR description_clean LIKE '%malam%' 
                 OR description_clean LIKE '%00-06%'
            THEN 'mds'

            ELSE 'main_quota'
        END AS quota_category,

        CASE
            WHEN commercial_name_clean LIKE '%akrab%' OR package_name_clean LIKE '%combo%' THEN 'Combo'
            WHEN commercial_name_clean LIKE '%unlimited%' OR package_name_clean LIKE '%unlimited%' THEN 'Unlimited'
            WHEN commercial_name_clean LIKE '%roaming%' THEN 'Roaming'
            WHEN commercial_name_clean LIKE '%video%' OR commercial_name_clean LIKE '%music%' THEN 'DPI'
            ELSE 'Internet'
        END AS package_type_final

    FROM base
)

SELECT 
    *,
    -- Price Group
    CASE 
        WHEN price_clean >= 75000 THEN 'High'
        WHEN price_clean >= 35000 AND price_clean < 75000 THEN 'Medium'
        ELSE 'Low'
    END AS price_group_final,

    -- Validity Group
    CASE
        WHEN validity_final <= 1 THEN 'Daily'
        WHEN validity_final <= 7 THEN 'Weekly'
        WHEN validity_final <= 30 THEN 'Monthly'
        ELSE '>30Days'
    END AS validity_group_final

FROM logic_apply