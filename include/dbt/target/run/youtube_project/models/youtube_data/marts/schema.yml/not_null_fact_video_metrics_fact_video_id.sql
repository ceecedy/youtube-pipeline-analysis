select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select fact_video_id
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
where fact_video_id is null



      
    ) dbt_internal_test