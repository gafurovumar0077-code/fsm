from connection import *

async def create_user(username, full_name, telegram_id):
    try:
        conn=await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) values
        ($1, $2, $3)
                        """, username, full_name, str(telegram_id))
    except Exception as error:
        print(f"Create user error: {error}")
    finally:
        await conn.close()
    

async def get_user_by_id(telegram_id):
    try:
        conn=await connection_db()
        user=await conn.fetchrow("""
        select * from users 
        where telegram_id = $1
                                 """, str(telegram_id))
        return user
    except Exception as error:
        print(f"Get user by id error: {error}")
    finally:
        await conn.close()
    



async def get_task_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetch("""
        select * from tasks 
        where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get task by id Error: {Error}")
    finally:
        await conn.close()





async def create_task(title, caption, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into tasks(title, caption, telegram_id) values
        ($1, $2, $3)
                           """, title, caption, str(telegram_id))
        return True
    except Exception as Error:
        print(f"Create task Error: {Error}")
        return False
    finally:
        await conn.close()




async def get_task(task_id):
    try:
        conn = await connection_db()
        task = await conn.fetchrow("""
        select * from tasks 
        where task_id = $1
                     """, int(task_id))
        return task
    except Exception as Error:
        print(f"Get task Error: {Error}")
    finally:
        await conn.close()




async def update_task(task_id, title, caption):
    try:
        conn = await connection_db()
        await conn.execute("""
        update tasks 
        set title = $1, caption = $2 
        where task_id = $3
                           """, title, caption, int(task_id))
        return True
    except Exception as Error:
        print(f"Update task Error: {Error}")
        return False
    finally:
        await conn.close()




async def delete_task(task_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        delete from tasks 
        where task_id = $1
                           """, int(task_id))
        return True
    except Exception as Error:
        print(f"Delete task Error: {Error}")
        return False
    finally:
        await conn.close()
        await conn.close()