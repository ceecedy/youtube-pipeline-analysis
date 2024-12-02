WITH region_data AS (
    SELECT * 
    FROM `yt-e2e-data-cycle-project`.`youtube`.`staging_region`  
)

SELECT
    region_code,
    region_name
FROM
    region_data