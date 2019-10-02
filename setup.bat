:: This script requires 'python' and 'virtualenv' to be in path!
:: TODO: Check already installed state and fix broken/uncomplete installation
:: TODO: Prompt to add a link to system startup folder
:: TODO: Check windows version if less than 10 then skip win10toast installation

@echo off
echo *********************************************
echo * Please wait until this window will close! *
echo *********************************************
cd %~dp0

pipenv install win10toast Pillow
