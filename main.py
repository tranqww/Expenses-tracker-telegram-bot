import asyncio  # noqa: I001
import os
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "expenses.db")
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")

#database
conn = sqlite3.connect(FILE_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL
    )
""")
conn.commit()

class Form(StatesGroup):
    category = State()
    amount = State()

bot = Bot(token=TOKEN)
storage=MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
#start command
async def cmd_start(message: types.Message):
    await message.answer(f"Hi {message.from_user.first_name}! I am expenses tracker bot. If u need help, type /help") # pyright: ignore[reportOptionalMemberAccess]

@dp.message(Command("total"))
#total command, calculating total sum of expenses what user gave
async def cmd_total(message: types.Message):
    await message.answer("Calculating...")
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (message.from_user.id,)) # type: ignore
    total = cursor.fetchone()[0]
    if total is None:
        await message.answer("0")
    else:
        await message.answer(f"Total: {total}")

@dp.message(Command("list"))
#showing all categories, and how much lost on it
async def cmd_list(message: types.Message):
    await message.answer("Exploring...")
    cursor.execute("SELECT category, amount FROM expenses WHERE user_id = ?", (message.from_user.id,)) # type: ignore
    expenses = cursor.fetchall()
    if not expenses:
        await message.answer("List is empty!")
        return
    lines = []
    for category, amount in expenses:
        lines.append(f"{category}: {amount}")
    await message.answer("\n".join(lines))

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "/add — add expense\n"
        "/list — show all expenses\n"
        "/total — show total sum"
    )

@dp.message(Command("add"))
#add new element to expenses
async def cmd_add(message: types.Message, state: FSMContext) -> None:
    await message.answer("Input expense category:")
    await state.set_state(Form.category)
@dp.message(Form.category)
#save category state
async def state_category(message: types.Message, state: FSMContext) -> None:
    await state.update_data(category=message.text)
    await message.answer("Enter the amount of money spent on this expense:")
    await state.set_state(Form.amount)
@dp.message(Form.amount)
async def state_amount(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        await state.update_data(amount=float(message.text)) # type: ignore
        data = await state.get_data()
        data["user_id"] = message.from_user.id # pyright: ignore[reportOptionalMemberAccess]     
    except ValueError:
        await message.answer("Please, input an valid amount:")
        return
    cursor.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", (data["user_id"], data["category"], data["amount"]))
    conn.commit()
    await message.answer("Expense has been successfully added!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())