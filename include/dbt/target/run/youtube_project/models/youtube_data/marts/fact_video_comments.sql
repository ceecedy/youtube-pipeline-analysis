
  
    

    create or replace table `yt-e2e-data-cycle-project`.`youtube`.`fact_video_comments`
      
    partition by timestamp_trunc(published_at, day)
    

    OPTIONS()
    as (
      WITH comment_data AS (
    SELECT 
        *
    FROM `yt-e2e-data-cycle-project`.`youtube`.`staging_video_comments`  -- Reference to the staging model for raw YouTube comment data
),

comment_filled AS (
    SELECT
        c.comment_id,
        c.video_id,
        c.comment_author,
        
       -- Clean invalid characters from comment_text
        COALESCE(
            REGEXP_REPLACE(c.comment_text, r'[\x00-\x1F\x7F-\x9F\xAD�]', ''), 
            'No Comment Text Available'
        ) AS comment_text,
        
        -- Safely cast like_count to integer
        SAFE_CAST(c.like_count AS INT64) AS like_count,
        
        -- If published_at is missing, set it to the current timestamp
        COALESCE(c.published_at, CURRENT_TIMESTAMP()) AS published_at,

        -- Join the video_id with dim_video to get the corresponding video
        v.video_id AS dim_video_id
    FROM
        comment_data c
    LEFT JOIN 
        `yt-e2e-data-cycle-project`.`youtube`.`dim_videos` v  -- Reference to the dim_video table to get the corresponding video
    ON
        c.video_id = v.video_id
)

SELECT 
    to_hex(md5(cast(coalesce(cast(cf.comment_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(cf.video_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(cf.published_at as string), '_dbt_utils_surrogate_key_null_') as string))) AS fact_comment_id,  -- Surrogate key based on the combination of comment_id, video_id, and published_at
    cf.comment_id,
    cf.video_id, 
    cf.comment_author,
    cf.comment_text,
    cf.like_count,
    cf.published_at
FROM 
    comment_filled cf
    );
  