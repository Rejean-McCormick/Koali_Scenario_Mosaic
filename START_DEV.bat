@echo off
cd /d "%~dp0"
where npm >nul 2>nul
if errorlevel 1 (echo Node.js/npm is required for development. You can still open START.html. & pause & exit /b 1)
if not exist node_modules (echo Installing dependencies... & call npm install & if errorlevel 1 pause & exit /b 1)
call npm run dev -- --open /uses/
