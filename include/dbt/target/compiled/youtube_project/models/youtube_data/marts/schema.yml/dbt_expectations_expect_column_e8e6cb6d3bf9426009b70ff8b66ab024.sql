with relation_columns as (

        
        select
            cast('REGION_CODE' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('REGION_NAME' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'REGION_CODE'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data