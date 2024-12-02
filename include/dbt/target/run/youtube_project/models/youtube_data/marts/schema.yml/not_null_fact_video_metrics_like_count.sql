select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select like_count
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
where like_count is null



      
    ) dbt_internal_test