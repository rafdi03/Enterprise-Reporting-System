{% macro extract_gb(text_col) %}
    CASE
        -- Case 1: Detect GB (misal: "20gb", "20.5 gb")
        -- Kita pakai regex yang sudah lowercase karena di staging text sudah di-lower
        WHEN {{ text_col }} ~ '([0-9]+([.,][0-9]+)?)\s*gb'
        THEN CAST(
            REPLACE(
                -- Ambil angkanya saja menggunakan SUBSTRING
                SUBSTRING({{ text_col }} FROM '([0-9]+(?:[.,][0-9]+)?)\s*gb'),
                ',', '.'
            ) AS NUMERIC
        )

        -- Case 2: Detect MB (misal: "500mb")
        WHEN {{ text_col }} ~ '([0-9]+([.,][0-9]+)?)\s*mb'
        THEN CAST(
            REPLACE(
                SUBSTRING({{ text_col }} FROM '([0-9]+(?:[.,][0-9]+)?)\s*mb'),
                ',', '.'
            ) AS NUMERIC
        ) / 1024.0

        -- Default 0
        ELSE 0
    END
{% endmacro %}
