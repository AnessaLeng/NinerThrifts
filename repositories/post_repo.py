from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import redirect, url_for
from flask import Flask, session
import psycopg

def get_all_posts():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(''' 
                           SELECT
                                username,
                                post_id,
                                title,
                                body,
                                price,
                                condition,
                                image_url,
                                posted_date
                           FROM
                                posts
                            ''')
            return cursor.fetchall()


def get_searched_posts(title: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(''' 
                           SELECT
                                username,
                                post_id,
                                title,
                                body,
                                price,
                                condition,
                                image_url,
                                posted_date
                           FROM
                                posts
                           WHERE
                                title ILIKE %s
                            ''', ['%' + title + '%'])
            search_result = cursor.fetchall()
    return search_result


def get_post_by_id(post_id: dict[str, Any]):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(''' 
                           SELECT
                                username,
                                post_id,
                                title,
                                body,
                                condition,
                                price,
                                image_url,
                                posted_date
                           FROM
                                posts
                           WHERE
                                post_id = %s
                            ''', [post_id])
            return cursor.fetchone()
        

def get_posts_by_username(username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(''' 
                           SELECT
                                username,
                                post_id,
                                title,
                                body,
                                condition,
                                price,
                                image_url,
                                posted_date
                           FROM
                                posts
                           WHERE
                                username = %s
                            ''', [username])
            return cursor.fetchall()


def update_post(post_id, title, body, price=None, condition=None, image_url=None):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            if price is not None and condition is not None and image_url is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, price = %s, condition = %s, image_url = %s
                            WHERE post_id = %s;
                            ''', (title, body, price, condition, image_url, post_id))
            elif price is not None and condition is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, price = %s, condition = %s
                            WHERE post_id = %s;
                            ''', (title, body, price, condition, post_id))
            elif price is not None and image_url is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, price = %s, image_url = %s
                            WHERE post_id = %s;
                            ''', (title, body, price, image_url, post_id))
            elif condition is not None and image_url is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, condition = %s, image_url = %s
                            WHERE post_id = %s;
                            ''', (title, body, condition, image_url, post_id))
            elif price is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, price = %s
                            WHERE post_id = %s;
                            ''', (title, body, price, post_id))
            elif condition is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, condition = %s
                            WHERE post_id = %s;
                            ''', (title, body, condition, post_id))
            elif image_url is not None:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s, image_url = %s
                            WHERE post_id = %s;
                            ''', (title, body, image_url, post_id))
            else:
                cur.execute('''
                            UPDATE posts 
                            SET title = %s, body = %s
                            WHERE post_id = %s;
                            ''', (title, body, post_id))
            conn.commit()

def delete_post(post_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                DELETE FROM posts
                WHERE post_id = %s
            ''', (post_id,))
            conn.commit()
    return redirect(url_for('show_profile', username=session['username']))

def add_favorite(username, post_id):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO favorites (username, post_id) VALUES (%s, %s)"
                cursor.execute(insert_query, (username, post_id))
            conn.commit()
        print("Favorite added successfully!")
    except Exception as error:
        print("Error while adding favorite:", error)

def remove_favorite(username, post_id):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                delete_query = "DELETE FROM favorites WHERE username = %s AND post_id = %s"
                cursor.execute(delete_query, (username, post_id))
            conn.commit()
        print("Favorite removed successfully!")
        return redirect(url_for('favorites'))
    except Exception as error:
        print("Error while removing favorite:", error)

def get_favorite_posts_by_username(username):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                select_query = '''
                    SELECT
                        p.username AS post_owner,
                        p.post_id,
                        p.title,
                        p.body,
                        p.price,
                        p.condition,
                        p.image_url,
                        p.posted_date
                    FROM
                        posts p
                    INNER JOIN
                        favorites f ON p.post_id = f.post_id
                    WHERE
                        f.username = %s
                '''
                cursor.execute(select_query, (username,))
                favorite_posts = cursor.fetchall()
        return favorite_posts
    except Exception as error:
        print("Error while retrieving favorite posts:", error)
        return []