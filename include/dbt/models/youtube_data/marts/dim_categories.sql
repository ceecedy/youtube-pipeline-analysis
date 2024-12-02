WITH category_data AS (
    SELECT * 
    FROM {{ ref('staging_category') }}
),

category_lookup AS (
    SELECT 
        category_struct.category_id,
        category_struct.category_name,
        category_struct.category_description
    FROM UNNEST([
        STRUCT(1 AS category_id, 'Film & Animation' AS category_name, 'Videos related to film and animation.' AS category_description),
        STRUCT(2 AS category_id, 'Autos & Vehicles' AS category_name, 'Videos related to cars, trucks, motorcycles, and vehicles.' AS category_description),
        STRUCT(10 AS category_id, 'Music' AS category_name, 'Videos related to music, music videos, and performances.' AS category_description),
        STRUCT(15 AS category_id, 'Pets & Animals' AS category_name, 'Videos related to pets, animals, and wildlife.' AS category_description),
        STRUCT(17 AS category_id, 'Sports' AS category_name, 'Videos related to sports events, commentary, and athletics.' AS category_description),
        STRUCT(18 AS category_id, 'Short Movies' AS category_name, 'Short films and independent films.' AS category_description),
        STRUCT(19 AS category_id, 'Travel & Events' AS category_name, 'Videos related to travel and live events.' AS category_description),
        STRUCT(20 AS category_id, 'Gaming' AS category_name, 'Videos related to video games, game commentary, and more.' AS category_description),
        STRUCT(22 AS category_id, 'People & Blogs' AS category_name, 'Personal vlogs and commentary.' AS category_description),
        STRUCT(23 AS category_id, 'Comedy' AS category_name, 'Videos related to comedic content.' AS category_description),
        STRUCT(24 AS category_id, 'Entertainment' AS category_name, 'Content related to entertainment and celebrity culture.' AS category_description),
        STRUCT(25 AS category_id, 'News & Politics' AS category_name, 'News and political commentary or events.' AS category_description),
        STRUCT(26 AS category_id, 'Howto & Style' AS category_name, 'How-to videos and style-related content.' AS category_description),
        STRUCT(27 AS category_id, 'Education' AS category_name, 'Educational content for various fields and topics.' AS category_description),
        STRUCT(28 AS category_id, 'Science & Technology' AS category_name, 'Videos related to science, tech, and innovations.' AS category_description),
        STRUCT(29 AS category_id, 'Nonprofits & Activism' AS category_name, 'Content related to nonprofits, activism, and charitable causes.' AS category_description),
        STRUCT(30 AS category_id, 'Movies' AS category_name, 'Full-length movies, movie trailers, and related content.' AS category_description),
        STRUCT(31 AS category_id, 'Anime & Animation' AS category_name, 'Anime series, animation, and related content.' AS category_description),
        STRUCT(32 AS category_id, 'Action & Adventure' AS category_name, 'Videos related to action and adventure content.' AS category_description),
        STRUCT(33 AS category_id, 'Classics' AS category_name, 'Classic movies, TV shows, and content.' AS category_description),
        STRUCT(34 AS category_id, 'Documentaries' AS category_name, 'Documentaries and docuseries content.' AS category_description),
        STRUCT(35 AS category_id, 'Drama' AS category_name, 'Dramas, TV shows, and related content.' AS category_description),
        STRUCT(36 AS category_id, 'Family & Parenting' AS category_name, 'Videos related to family life and parenting.' AS category_description),
        STRUCT(37 AS category_id, 'Home & Garden' AS category_name, 'Content about home improvement, gardens, and DIY projects.' AS category_description),
        STRUCT(38 AS category_id, 'Lifestyle' AS category_name, 'Videos about lifestyle, health, wellness, and more.' AS category_description),
        STRUCT(39 AS category_id, 'Music Videos' AS category_name, 'Music video content, including live and pre-recorded.' AS category_description),
        STRUCT(40 AS category_id, 'Reality TV' AS category_name, 'Reality TV shows and unscripted content.' AS category_description)
    ]) AS category_struct
)

, deduplicated_categories AS (
    SELECT 
        c.category_id,
        COALESCE(l.category_name, c.category_name, 'Unknown Category') AS category_name,
        COALESCE(l.category_description, c.category_description, 'Description not found') AS category_description,
        ROW_NUMBER() OVER (PARTITION BY c.category_id ORDER BY c.category_id) AS row_num
    FROM category_data c
    LEFT JOIN category_lookup l
        ON c.category_id = l.category_id
)

SELECT
    category_id,
    category_name,
    category_description
FROM
    deduplicated_categories
WHERE
    row_num = 1  -- Only keep the first row for each category_id
ORDER BY
    category_id
