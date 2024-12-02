select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select title
from `yt-e2e-data-cycle-project`.`youtube`.`dim_videos`
where title is null



      
    ) dbt_internal_test