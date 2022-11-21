from aiogram.dispatcher.filters.state import StatesGroup, State


class StartDialogForm(StatesGroup):
    mail: State = State()
    password: State = State()
