WITH region_data AS (
    SELECT * 
    FROM {{ ref('staging_region') }}  
)

SELECT
    region_code,
    region_name
FROM
    region_data
