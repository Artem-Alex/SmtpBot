from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class MainKeyboard:
    __button_send = KeyboardButton("Отправить письмо")
    __button_receive = KeyboardButton("Получить список писем")
    __button_get_mail = KeyboardButton("Просмотреть письма")
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        __button_send,
        __button_receive,
        __button_get_mail
    )
