from repositories.db import get_pool
from psycopg.rows import dict_row


def get_profile_info():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''      
                           SELECT
                                user_id,
                                username,
                                biography,
                                profile_picture,
                                followers,
                                following
                           FROM
                                profiles
                            ''')
            return cursor.fetchall()

