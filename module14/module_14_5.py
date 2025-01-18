from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from module14.crud_functions import *

initiate_db()
TOKEN=" "
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
users = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация'),
            KeyboardButton(text='Купить'), KeyboardButton(text='Регистрация')
        ]
], resize_keyboard=True)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton('Формулы расчёта', callback_data='formulas')]
])

kb_pro = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Выберите продукт для покупки:', callback_data='product_buying')],
        [InlineKeyboardButton('Продукт 1', callback_data='product_buying')], [InlineKeyboardButton('Продукт 2', callback_data='product_buying')],
        [InlineKeyboardButton('Продукт 3', callback_data='product_buying')], [InlineKeyboardButton('Продукт 4', callback_data='product_buying')]
        ])

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.answer("Привет, я бот помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def inline_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=keyboard)

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    with open("1.png", "rb") as img:
        await message.answer(f"Название: {users[0][0]} | Описание: {users[0][1]} | Цена: {users[0][2]} руб.")
        await message.answer_photo(img)
    with open("2.png", "rb") as img:
        await message.answer(f"Название: {users[1][0]} | Описание: {users[1][1]} | Цена: {users[1][2]} руб.")
        await message.answer_photo(img)
    with open("3.jpg", "rb") as img:
        await message.answer(f"Название: {users[2][0]} | Описание: {users[2][1]} | Цена: {users[2][2]} руб.")
        await message.answer_photo(img)
    with open("4.png", "rb") as img:
        await message.answer(f"Название: {users[3][0]} | Описание: {users[3][1]} | Цена: {users[3][2]} руб.")
        await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_pro)

@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.answer('Введите ваше имя: (только латинские буквы)')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите ваш email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите ваш возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Вы успешно зарегистрировались!')
    await state.finish()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def formulas(call: types.CallbackQuery):
    await call.message.answer('Формулы расчёта:\n'
                              'Норма калорий: 10 * вес + 6.25 * рост - 5 * возраст - 161\n'
                              'Норма белков: 1.5 * вес\n'
                              'Норма жиров: 0.5 * вес\n'
                              'Норма углеводов: 0.5 * вес')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def calories(call: types.CallbackQuery):
    await call.message.answer('Введите ваш возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост: ')


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес: ')


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer('Бот создан для расчёта нормы калорий и белков, жиров и углеводов.')



if __name__ == '__main__':
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    executor.start_polling(dp, skip_updates=True)
    connection.commit()
    connection.close()
