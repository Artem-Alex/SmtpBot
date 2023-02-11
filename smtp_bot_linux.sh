#!/bin/bash

echo "start smtp bot"

exec > /dev/null 2>&1

venv/Scripts/activate

cd smtp

export TOKEN=6062536275:AAHEZTAprsJKyDB5e_tgHTm_hLwGt2J0R5U

python main_bot.py

read