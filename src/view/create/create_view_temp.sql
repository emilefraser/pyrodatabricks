-- Create a temporary view `subscribed_movies`.
CREATE TEMPORARY VIEW subscribed_movies
    AS SELECT mo.member_id, mb.full_name, mo.movie_title
         FROM movies AS mo
         INNER JOIN members AS mb
            ON mo.member_id = mb.id;