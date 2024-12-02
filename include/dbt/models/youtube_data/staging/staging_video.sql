with raw_video as (
    select * 
    from {{ source('youtube', 'raw_youtube_video_data') }} 
)

select 
    video_id,
    title,
    description,
    channel_id,
    category_id,
    published_at
from raw_video
where video_id is not null
  and channel_id is not null
  and category_id is not null