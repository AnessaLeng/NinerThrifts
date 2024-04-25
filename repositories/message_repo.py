from typing import List, Any
from repositories.db import get_pool
from psycopg.rows import dict_row

def get_messages_for_user(user_id: int) -> List[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            m.message_id,
                            m.message_content,
                            m.sent_at,
                            u.username AS sender_username
                        FROM
                            messages m
                        INNER JOIN
                            app_user u
                        ON
                            m.sender_id = u.user_id
                        INNER JOIN
                            message_threads mt
                        ON
                            m.thread_id = mt.thread_id
                        WHERE
                            mt.sender_id = %s OR mt.recipient_id = %s
                        ORDER BY
                            m.sent_at DESC
                        ''', [user_id, user_id])
            messages = cur.fetchall()
            return messages
        
def get_thread_id(sender_id: int, recipient_id: int) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT
                            thread_id
                        FROM
                            message_threads
                        WHERE
                            (sender_id = %s AND recipient_id = %s)
                            OR
                            (sender_id = %s AND recipient_id = %s)
                        ''', [sender_id, recipient_id, recipient_id, sender_id])
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None
def get_or_create_thread(sender_id: int, recipient_id: int) -> int:
    thread_id = get_thread_id(sender_id, recipient_id)
    if thread_id is None:
        # If the thread doesn't exist, create a new one
        thread_id = create_thread(sender_id, recipient_id)
    return thread_id

def get_messages_for_thread(thread_id: int) -> List[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            m.message_id,
                            m.message_content,
                            m.sent_at,
                            u.username AS sender_username
                        FROM
                            messages m
                        INNER JOIN
                            app_user u
                        ON
                            m.sender_id = u.user_id
                        WHERE
                            m.thread_id = %s
                        ORDER BY
                            m.sent_at DESC
                        ''', [thread_id])
            messages = cur.fetchall()
            return messages

def create_thread(sender_id: int, recipient_id: int) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO message_threads (sender_id, recipient_id)
                        VALUES (%s, %s)
                        RETURNING thread_id
                        ''', [sender_id, recipient_id])
            thread_id = cur.fetchone()[0]
            return thread_id

def create_message(thread_id: int, sender_id: int, recipient_id: int, message_content: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO messages (thread_id, sender_id, recipient_id, message_content)
                        VALUES (%s, %s, %s, %s)
                        ''', (thread_id, sender_id, recipient_id, message_content))
            conn.commit()