
    
    

with dbt_test__target as (

  select pk_category_id as unique_field
  from `yt-e2e-data-cycle-project`.`youtube`.`dim_categories`
  where pk_category_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


