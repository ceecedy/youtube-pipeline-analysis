select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select channel_title
from `yt-e2e-data-cycle-project`.`youtube`.`dim_channels`
where channel_title is null



      
    ) dbt_internal_test