WITH video_data AS (
    SELECT * 
    FROM `yt-e2e-data-cycle-project`.`youtube`.`staging_video`  
),

video_filled AS (
    SELECT
        video_id,
        
        -- Clean invalid characters from title and provide a default value if necessary
        COALESCE(
            REGEXP_REPLACE(title, r'[\x00-\x1F\x7F-\x9F\xAD�]', ''), 
            'No Title Available'
        ) AS title,
        
        -- Clean invalid characters from description and provide a default value if necessary
        COALESCE(
            REGEXP_REPLACE(description, r'[\x00-\x1F\x7F-\x9F\xAD�]', ''), 
            'No Description Available'
        ) AS description,
        
        channel_id,
        category_id
    FROM
        video_data
)

SELECT
    v.video_id,
    v.title,
    v.description,
    v.channel_id,
    v.category_id
FROM
    video_filled v