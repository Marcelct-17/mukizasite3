@echo off
cd /d "%~dp0"
set PYTHON_EXE=C:\Users\MUK\AppData\Local\Programs\Python\Python314\python.exe

if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" app.py
) else (
    py -3.14 app.py
)
