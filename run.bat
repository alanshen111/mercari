@echo off
setlocal

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip not found. Installing pip...
    python -m ensurepip
    python -m pip install --upgrade pip
)

pip install -r requirements.txt

start cmd /k flask run

start http://127.0.0.1:5000

endlocal
