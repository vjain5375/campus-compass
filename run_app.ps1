Write-Host "Starting Campus Compass..." -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your browser automatically." -ForegroundColor Green
Write-Host "If it doesn't, go to: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the app." -ForegroundColor Gray
Write-Host ""
python -m streamlit run app.py --server.headless false

