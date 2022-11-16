from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class DatingForm(StatesGroup):
    mail: State = State()
    password: State = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await DatingForm.mail.set()
    await message.reply("Приветствую, укажи адрес своей электронной почты")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


@dp.message_handler(Text, state=DatingForm.mail)
async def process_mail(message: types.Message, state: FSMContext):
    await state.update_data(mail=message.text)
    # async with state.proxy() as data:
    #     data['mail'] = message.text

    await DatingForm.next()
    await message.reply("Укажи пароль от этой почты")


@dp.message_handler(Text, state=DatingForm.password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    # async with state.proxy() as data:
    #     data['password'] = message.text

    data = await state.get_data()
    print(f"mail={data.get('mail', None)}\n"
          f"password={data.get('password', None)}")
    await state.finish()
    await message.reply("Данные сохранены")


if __name__ == '__main__':
    executor.start_polling(dp)
