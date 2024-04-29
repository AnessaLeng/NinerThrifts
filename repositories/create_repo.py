
from repositories.db import get_pool

def create_post(username: str, title: str, body: str, price: float, condition: str, image_url: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO 
                        posts 
                            (username, 
                            title, 
                            body, 
                            price,
                            condition, 
                            image_url
                            )
                VALUES
                        (%s, %s, %s, %s, %s, %s)
            ''', (username, title, body, price, condition, image_url))
