select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      





    with grouped_expression as (
    select
        
        
    
  
( 1=1 and length(
        region_code
    ) >= 2 and length(
        region_code
    ) <= 5
)
 as expression


    from `yt-e2e-data-cycle-project`.`youtube`.`dim_regions`
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







      
    ) dbt_internal_test