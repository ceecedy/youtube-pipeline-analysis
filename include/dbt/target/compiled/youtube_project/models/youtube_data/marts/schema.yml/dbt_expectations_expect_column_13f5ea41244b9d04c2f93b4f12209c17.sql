





    with grouped_expression as (
    select
        
        
    
  
( 1=1 and length(
        description
    ) >= 0 and length(
        description
    ) <= 1000
)
 as expression


    from `yt-e2e-data-cycle-project`.`youtube`.`dim_videos`
    

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






