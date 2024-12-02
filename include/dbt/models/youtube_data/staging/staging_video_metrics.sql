with raw_video_metrics as (
    select * 
    from {{ source('youtube', 'raw_youtube_video_data') }}
)

select 
    video_id,
    region_code,
    SAFE_CAST(view_count as INT64) as view_count,
    SAFE_CAST(like_count as INT64) as like_count,
    SAFE_CAST(comment_count as INT64) as comment_count,
    published_at
from raw_video_metrics
where video_id is not null 
  and region_code is not null
