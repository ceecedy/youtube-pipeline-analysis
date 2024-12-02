select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select video_id
from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_comments`
where video_id is null



      
    ) dbt_internal_test