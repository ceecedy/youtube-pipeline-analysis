
    
    

with dbt_test__target as (

  select fact_video_id as unique_field
  from `yt-e2e-data-cycle-project`.`youtube`.`fact_video_metrics`
  where fact_video_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


