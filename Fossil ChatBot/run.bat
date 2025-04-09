@echo off
echo Controleren van Ollama setup...
python check_ollama.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Druk op een toets om af te sluiten...
    pause > nul
    exit /b %ERRORLEVEL%
)

echo.
echo Start Brandweer Strategie Advies...
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Er is een fout opgetreden. Druk op een toets om af te sluiten...
    pause > nul
    exit /b %ERRORLEVEL%
) 