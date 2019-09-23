@echo off
cd %~dp0
pipenv run python .\winmage.py
:: TODO Run without a window