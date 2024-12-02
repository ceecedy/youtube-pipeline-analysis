select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select comment_count
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
where comment_count is null



      
    ) dbt_internal_test