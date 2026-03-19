@echo off
cd /d C:\Users\anhmi\Downloads\games\ultittled_tank_game\tank-game
python -c "from src.server.server_gui import ServerGUI; s = ServerGUI('0.0.0.0', 12345); s.run()"
pause