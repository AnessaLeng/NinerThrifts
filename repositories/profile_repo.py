from repositories.db import get_pool
from psycopg.rows import dict_row


def get_profile_info():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''      
                           SELECT
                                username,
                                biography,
                                profile_picture,
                                followers,
                                following
                           FROM
                                profiles
                            ''')
            return cursor.fetchall()
        
# def save_post_to_profile(username, post_image):
#     pool = get_pool()
#     with pool.connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute('''
#                 INSERT INTO posts (username, post_image)
#                 VALUES (%s, %s)
#             ''', (username, post_image))
