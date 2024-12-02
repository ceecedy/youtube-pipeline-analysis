





    with grouped_expression as (
    select
        
        
    
  
( 1=1 and length(
        channel_title
    ) >= 1 and length(
        channel_title
    ) <= 255
)
 as expression


    from `yt-e2e-data-cycle-project`.`youtube`.`dim_channels`
    

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






