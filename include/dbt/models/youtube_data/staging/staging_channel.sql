with raw_channel as (
    select * 
    from {{ source('youtube', 'raw_youtube_video_data') }} 
)

select 
    channel_id,
    channel_title,
    channel_description,
    channel_published_at
from raw_channel
where channel_id is not null
