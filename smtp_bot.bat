@echo off
@echo "start smtp bot"

call %~dp0venv\Scripts\activate

cd %~dp0smtp

set TOKEN=6062536275:AAHEZTAprsJKyDB5e_tgHTm_hLwGt2J0R5U

python %~dp0smtp\main_bot.py

pause