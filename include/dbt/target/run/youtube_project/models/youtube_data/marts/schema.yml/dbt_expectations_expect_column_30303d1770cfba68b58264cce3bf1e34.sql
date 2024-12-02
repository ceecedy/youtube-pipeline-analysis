select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      with relation_columns as (

        
        select
            cast('FACT_COMMENT_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('COMMENT_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('VIDEO_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('COMMENT_AUTHOR' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('COMMENT_TEXT' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('LIKE_COUNT' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('PUBLISHED_AT' as string) as relation_column,
            cast('TIMESTAMP' as string) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'COMMENT_ID'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data
      
    ) dbt_internal_test