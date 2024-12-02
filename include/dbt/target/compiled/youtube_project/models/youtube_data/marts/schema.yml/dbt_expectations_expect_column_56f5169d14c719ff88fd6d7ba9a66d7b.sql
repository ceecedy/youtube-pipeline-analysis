


    with grouped_expression as (
    select
        
        
    
  
count(distinct comment_count) > 0
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


