from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class MainKeyboard:
    __button_send = KeyboardButton("Отправить письмо")
    __button_receive = KeyboardButton("Получить список писем")
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        __button_send, __button_receive
    )
