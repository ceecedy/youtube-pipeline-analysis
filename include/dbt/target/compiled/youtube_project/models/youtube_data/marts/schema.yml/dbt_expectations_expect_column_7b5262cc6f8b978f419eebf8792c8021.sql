with relation_columns as (

        
        select
            cast('PK_CHANNEL_ID' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('CHANNEL_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CHANNEL_TITLE' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CHANNEL_DESCRIPTION' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('CHANNEL_PUBLISHED_AT' as string) as relation_column,
            cast('TIMESTAMP' as string) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'CHANNEL_TITLE'
            and
            relation_column_type not in ('STRING')

    )
    select *
    from test_data