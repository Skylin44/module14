from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


TOKEN=" "
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = ReplyKeyboardMarkup()
    kb.add(KeyboardButton('Рассчитать')), KeyboardButton('Информация')
    kb.add(KeyboardButton('Купить'))
    await message.answer("Привет, я бот помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def inline_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'))
    keyboard.add(InlineKeyboardButton('Формулы расчёта', callback_data='formulas'))
    await message.answer('Выберите опцию:', reply_markup=keyboard)

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    await message.answer('Название: Product1 | Описание: "Представьте себе, что ваше пищеварение - это автомобиль,' 
         'который нуждается в регулярном техническом обслуживании. И вот,' 
         'наш чай в фильтр-пакетиках - это как ваш личный механик, который '
         'всегда готов помочь вам в нужный момент." | Цена: 100')
    with open('1.png', 'rb') as f:
        photo = types.InputFile(f.name)
        await message.answer_photo(photo)
    await message.answer('Название: Product2 | Описание: "Наш травяной чай "Энергия Здоровья" - это ваш источник энергии и здоровья.'
          'Сделан из натуральных трав, он поможет вашему организму работать на полную мощность.' 
          'Попробуйте сегодня и почувствуйте разницу!" | Цена: 200')
    with open('2.png', 'rb') as f:
        photo = types.InputFile(f.name)
        await message.answer_photo(photo)
    await message.answer('Название: Product3 | Описание: "Наш чай "Фитолит" - это ваш источник энергии и здоровья." | Цена: 300')
    with open('3.jpg', 'rb') as f:
        photo = types.InputFile(f.name)
        await message.answer_photo(photo)
        await message.answer('Название: Product4 | Описание: "Наш чай "Таёжный знахарь" - это ваш источник энергии и здоровья." | Цена: 400')
    with open('4.png', 'rb') as f:
        photo = types.InputFile(f.name)
        await message.answer_photo(photo)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Выберите продукт для покупки:', callback_data='product_buying'))
    keyboard.add(InlineKeyboardButton('Продукт 1', callback_data='product_buying')), keyboard.add(InlineKeyboardButton('Продукт 2', callback_data='product_buying'))
    keyboard.add(InlineKeyboardButton('Продукт 3', callback_data='product_buying')),keyboard.add(InlineKeyboardButton('Продукт 4', callback_data='product_buying'))
    await message.answer('Выберите продукт для покупки:', reply_markup=keyboard)


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
