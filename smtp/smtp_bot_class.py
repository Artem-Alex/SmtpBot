from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import TOKEN
from form_classes import StartDialogForm, SendMessageDialogForm
from singleton_wrapper import singleton
from send_message_class import MessageSender


@singleton
class SmtpBot:
    __bot: Bot = Bot(token=TOKEN)
    __storage: MemoryStorage = MemoryStorage()
    __dp: Dispatcher = Dispatcher(__bot, storage=__storage)

    @classmethod
    def get_dp(cls) -> Dispatcher:
        return cls.__dp

    @staticmethod
    @__dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        await StartDialogForm.mail.set()
        await message.reply("Приветствую, укажи адрес своей электронной почты")

    @staticmethod
    @__dp.message_handler(state="*", commands="cancel")
    @__dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await message.reply("ОК")

    @staticmethod
    @__dp.message_handler(Text, state=StartDialogForm.mail)
    async def process_mail(message: types.Message, state: FSMContext):
        await state.update_data(mail=message.text)

        await StartDialogForm.next()
        await message.reply("Укажи пароль от этой почты")

    @staticmethod
    @__dp.message_handler(Text, state=StartDialogForm.password)
    async def process_password(message: types.Message, state: FSMContext):
        await state.update_data(password=message.text)

        data = await state.get_data()
        print(
            f"mail= {data.get('mail', None)}\n"
            f"password= {data.get('password', None)}"
        )
        await state.finish()
        await message.reply("Данные сохранены")

    @staticmethod
    @__dp.message_handler(commands=["send"])
    async def cmd_send(message: types.Message):
        await SendMessageDialogForm.address.set()
        await message.reply(
            "Приветствую, укажи адрес электронной почты на которую нужно отправить письмо"
        )

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.address)
    async def process_address(message: types.Message, state: FSMContext):
        await state.update_data(address=message.text)

        await SendMessageDialogForm.next()
        await message.reply("Укажи заголовок письма")

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.message_subject)
    async def process_message_subject(message: types.Message, state: FSMContext):
        await state.update_data(message_subject=message.text)

        await SendMessageDialogForm.next()
        await message.reply("Введи текст письма")

    @staticmethod
    @__dp.message_handler(Text, state=SendMessageDialogForm.message_body)
    async def process_message_body(message: types.Message, state: FSMContext):
        await state.update_data(message_body=message.text)

        data = await state.get_data()
        address = data.get("address", None)
        title = data.get("message_subject", None)
        text = data.get("message_body", None)

        print(f"mail= {address}\n" f"Title= {title}\nText= {text}")

        ms = MessageSender(address, title, text)
        # ms.send_message()

        await state.finish()
        await message.reply("Письмо отправленно")
