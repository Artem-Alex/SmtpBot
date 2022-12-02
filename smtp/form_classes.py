from aiogram.dispatcher.filters.state import StatesGroup, State


class StartDialogForm(StatesGroup):
    mail: State = State()
    password: State = State()


class SendMessageDialogForm(StatesGroup):
    address: State = State()
    message_subject: State = State()
    message_body: State = State()


class MainDialogForm(StatesGroup):
    main: State = State()
