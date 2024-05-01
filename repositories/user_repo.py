from typing import List, Any
from flask import session
from repositories.db import get_pool
from psycopg.rows import dict_row

def does_email_exist(email: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT 
                            email
                        FROM 
                            users
                        WHERE 
                            email = %s;
                    ''', [email])
            user = cur.fetchone()
            return user is not None
        
def create_user(username: str, email: str, password: str, biography: str, first_name: str, last_name: str, dob: str, profile_picture: bytes) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('''
                            INSERT INTO users (username, email, pass, biography, first_name, last_name, dob, profile_picture)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING *
                        ''', [username, email, password, biography, first_name, last_name, dob, profile_picture])
                user = cur.fetchone()
                if user is None:
                    return None

                return {
                    "email": email,
                    "biography": biography,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "profile_picture": profile_picture
                }
        
def get_user_by_email(email:str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            username,
                            email,
                            pass AS hashed_password,
                            biography,
                            first_name,
                            last_name,
                            dob,
                            profile_picture
                        FROM 
                            users
                        WHERE 
                            email = %s;
                    ''', [email])
            user = cur.fetchone()
            return user
        
def get_username_by_email(email: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            username
                        FROM 
                            users
                        WHERE 
                            email = %s;
                    ''', [email])
            username = cur.fetchone()
            if username:
                return username
            else:
                None

def get_logged_in_user():
    email = session.get('email')
    print(email)
    if email is None:
        return None
    user = get_user_by_email(email)
    return user

# Needed for DMs

def get_all_users() -> List[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            username,
                            email,
                            pass AS hashed_password,
                            biography,
                            first_name,
                            last_name,
                            dob,
                            profile_picture
                        FROM 
                            users;
                    ''')
            users = cur.fetchall()
            return users

def get_user_by_username(username: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            username,
                            email,
                            pass AS hashed_password,
                            biography,
                            first_name,
                            last_name,
                            dob,
                            profile_picture
                        FROM 
                            users
                        WHERE 
                            username = %s;
                    ''', [str(username)])
            user = cur.fetchone()
            return user


def get_user_by_username(username: str) -> dict:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (str(username),))
            user = cur.fetchone()
            return user

def update_user_status(username: str, status: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET status = %s WHERE username = %s", (status, str(username)))
            conn.commit()


def get_current_user():
    username = session.get('username')
    if username is None:
        return None
    user = get_user_by_username(username)
    return user

def search_users(query: str) -> List[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            username,
                            email,
                            profile_picture
                        FROM 
                            users
                        WHERE 
                            username ILIKE %s;
                    ''', [f'%{query}%'])
            users = cur.fetchall()
            return users