select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select region_name
from `yt-e2e-data-cycle-project`.`youtube`.`dim_regions`
where region_name is null



      
    ) dbt_internal_test