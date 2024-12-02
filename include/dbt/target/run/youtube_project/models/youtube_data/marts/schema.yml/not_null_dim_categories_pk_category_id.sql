select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select pk_category_id
from `yt-e2e-data-cycle-project`.`youtube`.`dim_categories`
where pk_category_id is null



      
    ) dbt_internal_test