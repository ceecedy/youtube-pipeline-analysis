with relation_columns as (

        
        select
            cast('FACT_VIDEO_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('VIDEO_ID' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('REGION_CODE' as string) as relation_column,
            cast('STRING' as string) as relation_column_type
        union all
        
        select
            cast('VIEW_COUNT' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('LIKE_COUNT' as string) as relation_column,
            cast('INT64' as string) as relation_column_type
        union all
        
        select
            cast('COMMENT_COUNT' as string) as relation_column,
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
            relation_column = 'VIEW_COUNT'
            and
            relation_column_type not in ('INT64')

    )
    select *
    from test_data