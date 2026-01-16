{{ config(
    materialized='table',
    alias='reporting_telkom_' ~ var('date_suffix')
) }}

WITH final_logic AS (
    SELECT * FROM {{ ref('int_apply_rules') }}
)

SELECT
    id,
    source_filename as file_name,
    file_date,
    channel_final as channel,
    operator_final as operator,
    NOW() as created_date,

    commercial_name,
    package_name,
    package_type_final as package_type,

    price_clean as price,
    'IDR' as price_uom,
    benefit_detail as benefit,
    
    -- === PERBAIKAN DISINI ===
    -- Gunakan description_combined_raw agar formatnya: ""main_detail"": ... || ...
    description_combined_raw as description,
    
    validity_final as validity,
    'Days' as validity_uom,

    NULL as province,
    city_token as city,

    CASE WHEN quota_category = 'main_quota' THEN gb_from_desc ELSE 0 END as main_quota,
    'GB' as main_quota_uom,
    0 as local_quota,
    'GB' as localquota_uom,

    (CASE WHEN quota_category = 'main_quota' THEN gb_from_desc ELSE 0 END +
     CASE WHEN quota_category = 'youtube' THEN gb_from_desc ELSE 0 END +
     CASE WHEN quota_category = 'games' THEN gb_from_desc ELSE 0 END +
     CASE WHEN quota_category = 'chat_socmed' THEN gb_from_desc ELSE 0 END +
     CASE WHEN quota_category = 'other_video' THEN gb_from_desc ELSE 0 END
    ) as total_data_quota,
    'GB' as total_data_quota_uom,

    NULL as ppmb_total_data_quota,
    'Unknown' as status_4g,

    CASE WHEN quota_category = 'youtube' THEN gb_from_desc ELSE 0 END as youtube,
    CASE WHEN quota_category = 'other_video' THEN gb_from_desc ELSE 0 END as other_video,
    CASE WHEN quota_category = 'chat_socmed' THEN gb_from_desc ELSE 0 END as chat_socmed,
    CASE WHEN quota_category = 'mds' THEN gb_from_desc ELSE 0 END as mds,
    CASE WHEN quota_category = 'games' THEN gb_from_desc ELSE 0 END as games,
    
    0 as music, 0 as weekend, 0 as streaming_apps, 0 as provider_apps,
    0 as sms_onnet, 0 as sms_offnet, 0 as voice_onnet, 0 as voice_offnet, 0 as voice_allnet,

    'Unknown' as dpi, 'No' as unlimited, NOW() as parsed_at, 'Done' as ml_proc_status, NOW() as ml_proc_at,
    
    id as product_id,
    package_name_clean,
    city_token as city_clean,
    'Unknown' as offering_type,
    NULL as activation_date,
    
    los_token as los,
    los_group_final as los_group,
    'Unknown' as umb_layer,

    'Unknown' as msisdn, 'Unknown' as contact_fullname, NULL as ppmb_main_quota, CURRENT_DATE as load_date, CURRENT_DATE as event_date,
    
    channel_final as channel_clean,
    operator_final as operator_clean,
    EXTRACT(WEEK FROM CURRENT_DATE) as week,

    price_group_final as price_group,
    validity_group_final as validity_group,
    region_final as area,
    'Unknown' as zone,

    NULL as "%", NULL as xx, NULL as "segment price", NULL as "weekly segment", NULL as "daily segment",
    CASE WHEN quota_category = 'main_quota' THEN gb_from_desc ELSE 0 END as total_main_quota,
    operator_final as "segment operator"

FROM final_logic