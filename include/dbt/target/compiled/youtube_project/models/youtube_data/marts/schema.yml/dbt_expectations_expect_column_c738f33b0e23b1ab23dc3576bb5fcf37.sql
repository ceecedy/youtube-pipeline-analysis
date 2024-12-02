with relation_columns as (

        
        select
            cast('PK_CATEGORY_ID' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('CATEGORY_ID' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('CATEGORY_NAME' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CATEGORY_DESCRIPTION' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CATEGORY_NAME'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data