select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      with relation_columns as (

        
        select
            cast('VIDEO_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('TITLE' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('DESCRIPTION' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CHANNEL_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CATEGORY_ID' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'TITLE'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data
      
    ) dbt_internal_test