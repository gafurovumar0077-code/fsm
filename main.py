from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv
from connection import *
from service import *
import asyncio
import os


load_dotenv()

token_bot=os.getenv("BOT_TOKEN")

bot=Bot(token=token_bot)
dp=Dispatcher()

main_kb=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add Task"), KeyboardButton(text="Get My Tasks")],
        [KeyboardButton(text="Get Task")],
        [KeyboardButton(text="Update Task"), KeyboardButton(text="Delete Task")]
    ],
    resize_keyboard=True
)



class AddTask(StatesGroup):
    get_title = State()
    get_caption = State()

class GetTask(StatesGroup):
    get_id = State()
    
class DeleteTask(StatesGroup):
    get_id = State()
    
class UpdateTask(StatesGroup):
    get_id = State()
    get_title = State()
    get_caption = State()




@dp.message(CommandStart())
async def start_bot(message: Message):
    if await get_user_by_id(message.from_user.id):
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)




@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(f"This bot will be used by commands: /start, /help, /add_task, /get_task, /get_my_tasks, /update_task, /delete_task")





@dp.message(F.text=="Add Task")    
@dp.message(Command("add_task"))
async def add_task(message: Message, state : FSMContext):
    await message.answer("Enter task name: ")
    await state.set_state(AddTask.get_title)



@dp.message(AddTask.get_title)
async def add_task_title(message: Message, state : FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Enter description: ")
    await state.set_state(AddTask.get_caption)



@dp.message(AddTask.get_caption)
async def add_task_caption(message: Message, state : FSMContext):
    await state.update_data(caption = message.text)
    data = await state.get_data()
    await create_task(data["title"], data["caption"], message.from_user.id)
    await message.answer(f"""
    Your task created Succesfuly!
Title: {data["title"]}
Caption: {data["caption"]}
                         """)    
    await state.clear()




@dp.message(F.text=="Get My Tasks")
@dp.message(Command("get_my_tasks"))
async def get_my_tasks(message: Message, state: FSMContext):
    tasks = await get_task_by_id(message.from_user.id)
    if tasks:
        text = ""
        for task in tasks:
            text+= f"""
Id: {task['task_id']}
Title: {task['title']}
Caption: {task['caption']}
Dueration date: {task['due_date']}
Status: {task['status']}

Created at: {task['created_at']}

                             """
        await message.answer(text)
    else:
        await message.answer(f"Can't find any tasks!")
    await state.clear()




@dp.message(F.text=="Get Task")
@dp.message(Command("get_task"))
async def get_task_command(message: Message, state: FSMContext):
    task = await get_task_by_id(message.from_user.id)
    if task:
        await message.answer("Enter ID of the task: ")
        await state.set_state(GetTask.get_id)
    else:
        await message.answer("Can't find any tasks!")



@dp.message(GetTask.get_id)
async def get_task_id(message: Message, state: FSMContext):
    task = await get_task(int(message.text))
    if task:
        await message.answer(f"""
Id: {task['task_id']}
Title: {task['title']}
Caption: {task['caption']}
Dueration date: {task['due_date']}
Status: {task['status']}

Created at: {task['created_at']}


                             """)
    else:
        await message.answer("Can't find any tasks!")
    await state.clear()




@dp.message(F.text=="Delete Task")
@dp.message(Command("delete_task"))
async def delete_task_command(message: Message, state: FSMContext):
    await message.answer("Enter ID of the task for delete: ")
    await state.set_state(DeleteTask.get_id)


@dp.message(DeleteTask.get_id)
async def delete_task_id(message: Message, state: FSMContext):
    task_id = int(message.text)
    task = await get_task(task_id)
    if task:
        await delete_task(task_id)
        await message.answer(f"Task with ID {task_id} succesfuly deleted!")
    else:
        await message.answer("Can't find any tasks!")
    await state.clear()




@dp.message(F.text=="Update Task")
@dp.message(Command("update_task"))
async def update_task_command(message: Message, state: FSMContext):
    await message.answer("Enter ID task for updating: ")
    await state.set_state(UpdateTask.get_id)



@dp.message(UpdateTask.get_id)
async def update_task_id(message: Message, state: FSMContext):
    task_id = int(message.text)
    task = await get_task(task_id)
    if task:
        await state.update_data(task_id=task_id)
        await message.answer("Enter new name for the task: ")
        await state.set_state(UpdateTask.get_title)
    else:
        await message.answer("Can't find any tasks!")
        await state.clear()



@dp.message(UpdateTask.get_title)
async def update_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Enter new description for the task: ")
    await state.set_state(UpdateTask.get_caption)



@dp.message(UpdateTask.get_caption)
async def update_task_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    data = await state.get_data()
    await update_task(data["task_id"], data["title"], data["caption"])
    await message.answer(f"""
    Task succesfuly updated:
    Id: {data["task_id"]}
    Title: {data["title"]}
    Caption: {data["caption"]}
                         """)
    await state.clear()




async def  main():
    print("Bot started!")
    await create_table_db()
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())
