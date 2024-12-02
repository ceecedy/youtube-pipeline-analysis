with raw_category as (
    select * 
    from {{ source('youtube', 'raw_youtube_video_data') }} 
)

select 
    category_id,
    category_name,
    category_description
from raw_category
where category_id is not null
