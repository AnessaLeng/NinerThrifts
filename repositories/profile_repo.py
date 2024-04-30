from repositories.db import get_pool
from psycopg.rows import dict_row


def get_profile_info():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''      
                           SELECT
<<<<<<< HEAD
                                biography,
                                profile_picture,
                                image_url
                           FROM
                                users
                           INNER JOIN
                                posts
                           ON
                                users.username = posts.username
=======
                                username,
                                biography,
                                profile_picture
                           FROM
                                users
>>>>>>> 2ae617eba3f1a84381ba245945d63422155ebb1f
                            ''')
            return cursor.fetchall()
        
def get_profile_by_email(email):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''      
                           SELECT
                                username,
                                biography,
                                profile_picture
                           FROM
                                users
                           WHERE
                                email = %s
                            ''',[email])
            return cursor.fetchone()

