#!/bin/bash

echo "start smtp bot"

exec > /dev/null 2>&1

venv/Scripts/activate

cd smtp

export TOKEN=$1

python main_bot.py

read