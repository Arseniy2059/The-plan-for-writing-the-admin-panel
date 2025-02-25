from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *


initiate_db()

api = ''

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()


button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb.add(button3)
kb.add(button4)

menu = ReplyKeyboardMarkup()
d = KeyboardButton(text="Купить")
v = KeyboardButton(text="Рассчитать")

menu.add(d)
menu.add(v)

fr = InlineKeyboardMarkup()

a = InlineKeyboardButton(text='Product1', callback_data="product_buying")
y = InlineKeyboardButton(text="Product2", callback_data="product_buying")
q = InlineKeyboardButton(text="Product3", callback_data="product_buying")
g = InlineKeyboardButton(text="Product4", callback_data="product_buying")

fr.add(a)
fr.add(y)
fr.add(q)
fr.add(g)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий товоему здоровью.', reply_markup=menu)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Введите опцию:', reply_markup=kb)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for index, product in enumerate(get_all_products()):
        await message.answer(f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}")
        with open(f'm{1+index}.jpg', 'rb') as po:
            await message.answer_photo(po)
    await message.answer("Выберите продукт для покупки:", reply_markup=fr)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x weight (kg) + 6.25 x height (cm) - 5 x Age (g) - 161')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)