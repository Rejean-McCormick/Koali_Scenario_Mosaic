@echo off
setlocal
cd /d "%~dp0"

echo [Koali] Checking Node.js and npm...

where node >nul 2>&1
if errorlevel 1 goto :no_node

where npm >nul 2>&1
if errorlevel 1 goto :no_npm

for /f "delims=" %%V in ('node -p "process.versions.node"') do set "NODE_VERSION=%%V"
echo [Koali] Node %NODE_VERSION%

echo.
echo [Koali] Installing or updating npm dependencies...
call npm install --no-audit --no-fund
if errorlevel 1 goto :npm_error

echo.
echo [Koali] Building responsive scenario images and offline preview...
call npm run preview:offline
if errorlevel 1 goto :build_error

echo.
echo [Koali] Ready.
start "" "%~dp0START.html"
exit /b 0

:no_node
echo.
echo ERROR: Node.js was not found in PATH.
echo Install the Node.js version required by package.json, then run START.bat again.
pause
exit /b 1

:no_npm
echo.
echo ERROR: npm was not found in PATH.
pause
exit /b 1

:npm_error
echo.
echo ERROR: npm install failed.
pause
exit /b 1

:build_error
echo.
echo ERROR: responsive image or offline preview generation failed.
pause
exit /b 1
