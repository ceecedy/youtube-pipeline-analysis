






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and channel_published_at >= 1900-01-01 and channel_published_at <= CURRENT_TIMESTAMP()
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







