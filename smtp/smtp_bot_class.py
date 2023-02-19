import os
import logging

import dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand

from form_classes import StartDialogForm, SendMessageDialogForm, MainDialogForm
from singleton_wrapper import singleton
from send_message_class import MessageSender
from database_class import Database
from keyboards import MainKeyboard
from email_validator_class import EmailValidator

logging.basicConfig(level=logging.INFO, filename=f"{__name__}.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
dotenv.load_dotenv(dotenv.find_dotenv())


@singleton
class SmtpBot:
    __bot: Bot = Bot(token=os.getenv('TOKEN'))
    __storage: MemoryStorage = MemoryStorage()
    __dp: Dispatcher = Dispatcher(__bot, storage=__storage)

    @classmethod
    def get_dp(cls) -> Dispatcher:
        return cls.__dp

    @staticmethod
    @__dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        try:
            if Database.select_mail(message.chat.id) is not None:
                Database.delete_mail(message.chat.id)
                logging.info("Select mail is not None")
        except:
            logging.error("db do not create", exc_info=True)
            Database.create_mail_table()

        await StartDialogForm.mail.set()
        await message.reply("Приветствую, укажи адрес своей электронной почты")

    @staticmethod
    @__dp.message_handler(commands=['help'])
    async def commands(message: types.Message, bot=__bot):
        # commands = {'/start': 'Нажмите для запуска бота', '/help': 'Нажмите для просмотра доступных команд'}
        bot_commands = [
            BotCommand(command="/help", description="Get info about me"),

            # any command
            # BotCommand(command="/qna", description="set bot for a QnA task"),
            # BotCommand(command="/chat", description="set bot for free chat")
        ]
        await bot.set_my_commands(bot_commands)

        # await message.answer(f'{command}\n{discription}' for command, discription in commands.items())

    @staticmethod
    @__dp.message_handler(commands=["msg"])
    async def get_mail():
        pass

    @staticmethod
    @__dp.message_handler(commands=["continue"])
    async def cmd_continue(message: types.Message):
        await MainDialogForm.main.set()
        await message.answer("Что хотите сделать?", reply_markup=MainKeyboard.main_kb)

    @staticmethod
    @__dp.message_handler(state="*", commands="cancel")
    @__dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await message.answer("ОК")

        await MainDialogForm.main.set()
        await message.answer("Что хотите сделать?", reply_markup=MainKeyboard.main_kb)

    @staticmethod
    @__dp.message_handler(Text, state=StartDialogForm.mail)
    async def process_mail(message: types.Message, state: FSMContext):
        if EmailValidator.validate_email(message.text):
            await state.update_data(mail=message.text)
            await StartDialogForm.next()
            await message.answer("Укажи пароль от этой почты")
        else:
            await message.answer("Недействительный адрес почты, повтори ввод")

    @staticmethod
    @__dp.message_handler(Text, state=StartDialogForm.password)
    async def process_password(message: types.Message, state: FSMContext):
        await state.update_data(password=message.text)

        data = await state.get_data()
        mail = data.get("mail", None)
        password = data.get("password", None)
        user_id = message.chat.id
        Database.insert_mail(user_id, mail)
        print(f"mail= {mail}\n" f"password= {password}")
        await state.finish()
        await message.answer("Данные сохранены")
        await MainDialogForm.main.set()
        await message.answer("Что хотите сделать?", reply_markup=MainKeyboard.main_kb)

    @staticmethod
    @__dp.message_handler(
        Text(equals="Отправить письмо", ignore_case=True), state=MainDialogForm.main
    )
    async def cmd_send(message: types.Message):
        await SendMessageDialogForm.address.set()
        await message.answer(
            "Укажи адрес электронной почты на которую нужно отправить письмо"
        )

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.address)
    async def process_address(message: types.Message, state: FSMContext):
        if EmailValidator.validate_email(message.text):
            await state.update_data(address=message.text)
            await SendMessageDialogForm.next()
            await message.answer("Укажи заголовок письма")
        else:
            await message.answer("Недействительный адрес почты, повтори ввод")

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.message_subject)
    async def process_message_subject(message: types.Message, state: FSMContext):
        await state.update_data(message_subject=message.text)

        await SendMessageDialogForm.next()
        await message.answer("Введи текст письма")

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.message_body)
    async def process_message_body(message: types.Message, state: FSMContext):
        await state.update_data(message_body=message.text)

        data = await state.get_data()
        address = data.get("address", None)
        title = data.get("message_subject", None)
        text = data.get("message_body", None)

        user_id = message.chat.id
        login = Database.select_mail(user_id)

        print(f"mail= {address}\n" f"Title= {title}\nText= {text}")

        ms = MessageSender(login, address, title, text)
        # ms.send_message()

        await state.finish()
        await message.answer("Письмо отправленно")

        await MainDialogForm.main.set()
        await message.answer("Что хотите сделать?", reply_markup=MainKeyboard.main_kb)

    @staticmethod
    @__dp.message_handler(lambda message: message.get_command() not in (None, "/start", ...))
    async def answer_unknown_command(message: types.Message):
        await message.answer(f"Неизвестная команда\n\n{message.text}")
