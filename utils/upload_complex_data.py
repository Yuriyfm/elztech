import psycopg2
import os
from dotenv import load_dotenv
import random
import uuid

load_dotenv()


conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                        port=os.getenv('DB_PORT'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        database=os.getenv('DB_NAME')) # To remove slash

cursor = conn.cursor()
for i in range(20):
    cursor.execute("INSERT INTO complexes (name, uuid) VALUES(%s, %s)", (f'Комплекс № {random.randint(0, 100)}', str(uuid.uuid4())))
    conn.commit()
cursor.close()
conn.close()
