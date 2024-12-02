






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and published_at >= TIMESTAMP('1900-01-01 00:00:00') and published_at <= TIMESTAMP('2100-12-31 23:59:59')
)
 as expression


    from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
    

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







