
{% macro extract_days(text_col) %}
    -- Menggunakan SUBSTRING untuk mengambil angka hari
    -- Regex: (\d+) ambil angka, diikuti spasi opsional, lalu kata day/days/d
    CAST(
        NULLIF(
            SUBSTRING({{ text_col }} FROM '(\d+)\s*(?:days?|d)'),
            ''
        )
        AS INT
    )
{% endmacro %}
