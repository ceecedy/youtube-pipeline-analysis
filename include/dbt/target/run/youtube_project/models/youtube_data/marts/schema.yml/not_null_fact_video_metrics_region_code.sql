select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select region_code
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
where region_code is null



      
    ) dbt_internal_test