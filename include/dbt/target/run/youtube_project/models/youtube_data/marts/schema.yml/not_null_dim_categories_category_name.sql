select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select category_name
from `yt-e2e-data-cycle-project`.`youtube`.`dim_categories`
where category_name is null



      
    ) dbt_internal_test