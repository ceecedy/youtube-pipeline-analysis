





    with grouped_expression as (
    select
        
        
    
  
( 1=1 and length(
        region_name
    ) >= 1 and length(
        region_name
    ) <= 100
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






