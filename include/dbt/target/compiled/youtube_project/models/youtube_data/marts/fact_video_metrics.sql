WITH video_metrics_data AS (
    SELECT
        *
    FROM `yt-e2e-data-cycle-project`.`youtube`.`staging_video_metrics`  -- Reference to the staging table for video metrics
),

metrics_filled AS (
    SELECT
        vmd.video_id,
        vmd.region_code,
        vmd.view_count, 
        vmd.like_count, 
        vmd.comment_count, 
        
        -- Use COALESCE to fill in missing values for published_at
        COALESCE(vmd.published_at, CURRENT_TIMESTAMP()) AS published_at,
        
        -- Join with dim_video to get the corresponding video details
        dv.video_id AS dim_video_id,
        
        -- Join with dim_region to get the corresponding region details
        dr.region_code AS dim_region_code
    FROM
        video_metrics_data vmd
    LEFT JOIN `yt-e2e-data-cycle-project`.`youtube`.`dim_videos` dv  -- Reference to the dim_video table to get the corresponding video
        ON vmd.video_id = dv.video_id  -- Join condition for dim_videos
    LEFT JOIN `yt-e2e-data-cycle-project`.`youtube`.`dim_regions` dr  -- Reference to the dim_region table to get the corresponding region
        ON vmd.region_code = dr.region_code  -- Join condition for dim_regions
)

SELECT 
    to_hex(md5(cast(coalesce(cast(mf.video_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(mf.published_at as string), '_dbt_utils_surrogate_key_null_') as string))) AS fact_video_id,  -- Surrogate key based on the combination of mf.video_id and mf.published_at
    mf.video_id,
    mf.region_code,
    mf.view_count,
    mf.like_count,
    mf.comment_count,
    mf.published_at
FROM 
    metrics_filled mf