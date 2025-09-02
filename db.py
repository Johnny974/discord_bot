import os
import psycopg2
from psycopg2.extras import DictCursor


DATABASE_URL = os.environ.get('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS fruit_highscores (
                    guild_id BIGINT PRIMARY KEY,
                    score INT NOT NULL DEFAULT 0
                )
            """)
            conn.commit()


def get_highscore(guild_id: int) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT score FROM fruit_highscores WHERE guild_id = %s", (guild_id,))
            row = cur.fetchone()
            return row["score"] if row else 0


def update_highscore(guild_id: int, new_score: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO fruit_highscores (guild_id, score)
                VALUES (%s, %s)
                ON CONFLICT (guild_id)
                DO UPDATE SET score = EXCLUDED.score
                WHERE fruit_highscores.score < EXCLUDED.score
            """, (guild_id, new_score))
            conn.commit()
