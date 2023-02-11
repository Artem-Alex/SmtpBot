@echo off
@echo "start smtp bot"

call %~dp0venv\Scripts\activate

cd %~dp0smtp

set TOKEN=%1

python %~dp0smtp\main_bot.py

pause