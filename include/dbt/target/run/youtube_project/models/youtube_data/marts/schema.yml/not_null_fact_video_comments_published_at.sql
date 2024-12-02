select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select published_at
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_comments`
where published_at is null



      
    ) dbt_internal_test