WITH channel_data AS (
    SELECT * 
    FROM {{ ref('staging_channel') }}  
),

channel_filled AS (
    SELECT
        channel_id,
        
        -- Clean invalid characters from channel title
        COALESCE(
            REGEXP_REPLACE(channel_title, r'[\x00-\x1F\x7F-\x9F\xAD�]', ''), 
            'No Channel Title Available'
        ) AS channel_title,
        
        -- Clean invalid characters from channel description
        COALESCE(
            REGEXP_REPLACE(channel_description, r'[\x00-\x1F\x7F-\x9F\xAD�]', ''), 
            'No Channel Description Available'
        ) AS channel_description,
        
        -- If channel_published_at is NULL, replace with CURRENT_TIMESTAMP
        COALESCE(channel_published_at, CURRENT_TIMESTAMP()) AS channel_published_at
    FROM
        channel_data
),

ranked_channels AS (
    SELECT
        ROW_NUMBER() OVER (PARTITION BY channel_id ORDER BY channel_id) AS row_num,  
        channel_id,
        channel_title,
        channel_description,
        channel_published_at
    FROM
        channel_filled
)

SELECT
    channel_id,
    channel_title,
    channel_description,
    channel_published_at
FROM
    ranked_channels
WHERE
    row_num = 1 -- Keeps only the first row for each unique channel_id
