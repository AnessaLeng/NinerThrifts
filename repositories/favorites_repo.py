from repositories.db import get_pool


def get_all_favorites():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    user_id,
                    post_id
                FROM
                    favorites
            ''')
            return cursor.fetchall()

def add_favorite(user_id: int, post_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO 
                        favorites (user_id, post_id)
                VALUES 
                        (%s, %s)
            ''', (user_id, post_id))

def remove_favorite(user_id: int, post_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                DELETE FROM 
                        favorites
                WHERE
                        user_id = %s AND post_id = %s
            ''', (user_id, post_id))