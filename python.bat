@echo off
setlocal
set PYTHON_EXE=C:\Users\MUK\AppData\Local\Programs\Python\Python314\python.exe
if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" %*
) else (
  py %*
)
