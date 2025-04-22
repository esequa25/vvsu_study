# -*- coding: utf-8 -*-

import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres_db",
    "user": "postgres",
    "password": "postgres",
    "client_encoding":"utf8"
}

fake = Faker('ru_RU')

def generate_users(cursor, count=50):
    for _ in range(count):
        username = fake.unique.user_name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (username, email) "
            "VALUES (%s, %s) RETURNING id",
            (username, email)
        )
        user_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO logs (user_id, action_type, status) "
            "VALUES (%s, 'register', 'success')",
            (user_id)
        )
    return count

def generate_topics(cursor, users, days=30):
    topic_ids = []
    for day in range(days):
        date = datetime.now() - timedelta(days=days-day-1)
        
        for _ in range(random.randint(3, 7)):  # 3-7 тем в день
            user_id = random.choice(users)
            
            # 2 ошибки на день (неавторизованные попытки)
            if random.random() < 0.1:  # ~10% ошибок
                cursor.execute(
                    "INSERT INTO logs (action_type, status, creation_date) "
                    "VALUES ('create_topic', 'error', %s)",
                    (date)
                )
                continue
                
            title = fake.sentence()
            cursor.execute(
                "INSERT INTO topics (user_id, title, content, creation_date) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, title, getContent(title), date)
            )
            topic_id = cursor.fetchone()[0]
            topic_ids.append(topic_id)
            
            cursor.execute(
                "INSERT INTO logs (user_id, action_type, action_id, status, creation_date) "
                "VALUES (%s, 'create_topic', %s, 'success', %s)",
                (user_id, topic_id, date)
            )
    return topic_ids

def generate_comments(cursor, topics, users, days=30):
    for day in range(days):
        date = datetime.now() - timedelta(days=days-day-1)
        
        for _ in range(random.randint(10, 20)):  # 10-20 комментариев в день
            topic_id = random.choice(topics)
            is_anonymous = random.choice([True, False])
            
            if is_anonymous:
                cursor.execute(
                    "INSERT INTO comments (topic_id, is_anon, content, creation_date) "
                    "VALUES (%s, %s, %s, %s) RETURNING id",
                    (topic_id, True, fake.text(), date)
                )
                comment_id = cursor.fetchone()[0]
                
                cursor.execute(
                    "INSERT INTO logs (action_type, action_id, status, creation_date) "
                    "VALUES ('create_comment',, %s, 'success', %s)",
                    (comment_id, date)
                )
            else:
                user_id = random.choice(users)
                cursor.execute(
                    "INSERT INTO comments (topic_id, user_id, is_anonymous, content, creation_date) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (topic_id, user_id, False, fake.text(), date)
                )
                comment_id = cursor.fetchone()[0]
                
                cursor.execute(
                    "INSERT INTO logs (user_id, action_type, action_id, status, creation_date) "
                    "VALUES (%s, 'create_comment', %s, 'success', %s)",
                    (user_id, comment_id, date)
                )

def getContent(text):
    return text.lower().replace(' ', '-').replace('.', '')[:210]

def main():
    conn = psycopg2.connect(**DB_CONFIG)

    cursor = conn.cursor()
    
    cursor.execute("TRUNCATE TABLE logs, comments, topics, users RESTART IDENTITY CASCADE")
    
    user_count = generate_users(cursor)
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    topic_ids = generate_topics(cursor, user_ids)
    generate_comments(cursor, topic_ids, user_ids)
    
    generate_other_logs(cursor, user_ids, topic_ids)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Генерация данных завершена!")

if __name__ == "__main__":
    main()