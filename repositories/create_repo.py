
from repositories.db import get_pool

def create_post(user_id: int, username: str, title: str, body: str, price: float, condition: str, post_image: bytes):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO 
                        posts 
                            (user_id, 
                            username, 
                            title, 
                            body, 
                            price,
                            condition, 
                            post_image)
                VALUES
                        (%s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, username, title, body, price, condition, post_image))
