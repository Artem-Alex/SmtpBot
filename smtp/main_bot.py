from aiogram.utils import executor
from smtp_bot_class import SmtpBot

if __name__ == "__main__":
    smtp_bot: SmtpBot = SmtpBot()
    executor.start_polling(smtp_bot.get_dp(), skip_updates=True)
