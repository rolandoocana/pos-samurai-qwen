@echo off
cd /d "%~dp0..\backend"
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
netsh advfirewall firewall add rule name="SAMURAI-POS" dir=in action=allow protocol=TCP localport=8000
start "" uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
timeout /t 3
start http://localhost:8000/static/index.html
