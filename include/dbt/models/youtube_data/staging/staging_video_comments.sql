with raw_comments as (
    select * 
    from {{ source('youtube', 'raw_youtube_comment_data') }}
)

select 
    comment_id,
    video_id,
    comment_author,
    comment_text,
    like_count,
    published_at
from raw_comments
where comment_id is not null
  and video_id is not null
