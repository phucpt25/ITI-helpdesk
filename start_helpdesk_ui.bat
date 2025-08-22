@echo off
cd /d "%~dp0"
echo ================================================
echo    IT Helpdesk Chatbot UI Launcher
echo ================================================
echo.
echo Starting the helpdesk chatbot interface...
echo.
echo Features:
echo  - AI-powered IT support chatbot
echo  - Knowledge base with 14+ solutions
echo  - Vector-based semantic search
echo  - Real-time chat interface
echo  - System status dashboard
echo  - Quick Actions (Reset Password, Admin Request, etc.)
echo.
echo The app will open automatically in your browser
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

"..\.venv\Scripts\python.exe" -m streamlit run "helpdesk_chatbot_ui.py" --server.port 8501

echo.
echo ================================================
echo Server stopped. Press any key to exit...
pause > nul
