@echo off

where pyw > nul
if %ERRORLEVEL% NEQ 0 (
    cls
    echo You need to download Python.
    start ms-windows-store://pdp/?productid=9ncvdn91xzqp
    echo Press any key to exit...
    pause > nul
    exit
)

where pip > nul
if %ERRORLEVEL% NEQ 0 (
    cls
    echo PIP is not working. Make sure Python is installed correctly or install PIP manually.
    echo Press any key to exit...
    pause > nul
    exit
)

if exist requirements.txt (
    echo Installing required packages...
    pip install -r requirements.txt
    echo Done
    del requirements.txt
)

:launch
start "" pyw "main.py"
exit
