select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select pk_channel_id
from `yt-e2e-data-cycle-project`.`youtube`.`dim_channels`
where pk_channel_id is null



      
    ) dbt_internal_test