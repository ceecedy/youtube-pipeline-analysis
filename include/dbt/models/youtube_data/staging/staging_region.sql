with raw_region as (
    select distinct region_code
    from {{ source('youtube', 'raw_youtube_video_data') }} 
)

select 
    region_code,
    case 
        when region_code = 'PH' then 'Philippines'
        when region_code = 'US' then 'United States'
        else 'Unknown'  -- Default value for any unexpected region code
    end as region_name
from raw_region
where region_code is not null
