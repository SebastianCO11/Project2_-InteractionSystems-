@echo off
REM Script to create a virtual environment and install requirements
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
@echo.
echo Virtual environment setup complete. To activate later, run:
echo   call venv\Scripts\activate
