@echo off
title G*Power Clone Scientific Workbench (K4)
echo =========================================================
echo   G*Power Clone - Scientific Power Workbench (K4)
echo   Sunucu baslatiliyor: http://localhost:5000
echo =========================================================

start "" "http://localhost:5000"
"%~dp0.venv\Scripts\python.exe" web/app.py 5000
