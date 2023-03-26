@echo off
call ./ripfix/Scripts/activate.bat
python script.py %*
call ./ripfix/Scripts/deactivate.bat
pause