import asyncio  # noqa: I001
import os
import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "expenses.json")
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def expenses_calculate():
    #calculating total amount of expenses
    total = 0
    for item in expenses:
        total += item["amount"]
    return total

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")

try:
    
    with open(FILE_PATH, "r", encoding = "utf-8") as file:
        expenses = json.load(file)
        print("File has been loaded.")
except FileNotFoundError as e:
    print(f"File is not created! Creating...\n{e}")
    expenses = []
    with open(FILE_PATH, "w", encoding = "utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)
        print("File has been created.")
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    expenses = []

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
    await message.answer(f"Total: {expenses_calculate()}")

@dp.message(Command("list"))
#showing all categories, and how much lost on it
async def cmd_list(message: types.Message):
    await message.answer("Exploring...")
    if not expenses:
        await message.answer("List is empty!")
        return
    lines = [f"{item['category']}: {item['amount']}" for item in expenses]
    await message.answer("\n".join(lines))

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
        print(data)
    except ValueError:
        await message.answer("Please, input an valid amount:")
        return
    global expenses  # noqa: PLW0602
    expenses.append(data)
    with open(FILE_PATH, "w", encoding = "utf-8") as file:  # noqa: ASYNC230
        json.dump(expenses, file, ensure_ascii=False, indent=2)
        print("File has been changed.")
        await message.answer("Expense has been successfully added!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())