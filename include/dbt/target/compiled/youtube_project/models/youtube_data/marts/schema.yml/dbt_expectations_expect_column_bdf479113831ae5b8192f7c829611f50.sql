






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and published_at >= 1900-01-01 and published_at <= 2100-12-31
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







