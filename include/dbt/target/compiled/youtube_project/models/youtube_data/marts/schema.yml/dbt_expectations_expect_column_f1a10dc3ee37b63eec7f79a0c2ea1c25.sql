





    with grouped_expression as (
    select
        
        
    
  
( 1=1 and length(
        comment_author
    ) >= 1 and length(
        comment_author
    ) <= 255
)
 as expression


    from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_comments`
    

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






