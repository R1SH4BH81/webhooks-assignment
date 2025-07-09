@echo off
echo Starting GitHub Webhook System
echo ==============================

echo Starting MongoDB (if not already running)...
echo Note: This assumes MongoDB is installed and in your PATH
start /B mongod

echo Starting Flask backend...
start /B cmd /c "python webhook_receiver.py"

echo Starting UI server...
start /B cmd /c "python serve_ui.py"

echo.
echo All services started!
echo.
echo Access the UI at: http://localhost:8000/ui.html
echo.
echo To test with sample data, run: python test_webhook.py
echo.
echo Press any key to stop all services...
pause > nul

echo Stopping services...
taskkill /F /IM python.exe > nul 2>&1
taskkill /F /IM mongod.exe > nul 2>&1

echo Done!