
    
    

with dbt_test__target as (

  select pk_channel_id as unique_field
  from `yt-e2e-data-cycle-project`.`youtube`.`dim_channels`
  where pk_channel_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


