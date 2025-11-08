@echo off
echo Starting Campus Compass...
echo.
echo The app will open in your browser automatically.
echo If it doesn't, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app.
echo.
python -m streamlit run app.py --server.headless false

