from dotenv import *
import asyncpg
import os

load_dotenv()

password=os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn=await asyncpg.connect(
            user="postgres",
            port=5432,
            database="task_manager1",
            password=password,
            host="localhost"
        )
        return conn
    except Exception as error:
        print(f"Connection error: {error}")


async def create_table_db():
    try:
        conn=await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            username varchar(200),
            full_name varchar(300),
            telegram_id varchar(300),
            is_active boolean default true,
            created_at timestamp default now()
        );
        
        
        create table if not exists tasks(
            task_id serial primary key,
            title varchar(100),
            caption text,
            telegram_id varchar(200),
            due_date varchar(200),
            created_at timestamp default now(),
            status boolean default false,
            is_active boolean default true
        )  
        

                           """)
        print("Table created")
    except Exception as error:
        print(f"Create table Error: {error}")
    finally:
        await conn.close()
