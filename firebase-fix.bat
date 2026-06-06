@echo off
setlocal
cd /d "%~dp0"

echo.
echo  Firebase fix / login / deploy — HotelRestaurantMini-Mart
echo  Use Google account: roi.reuven@gmail.com
echo.

if /I "%~1"=="deploy" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\firebase-windows.ps1" -Deploy
    goto :done
)

if /I "%~1"=="login" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\firebase-windows.ps1" -LoginOnly
    goto :done
)

if /I "%~1"=="token" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\firebase-windows.ps1" -CiToken
    goto :done
)

if /I "%~1"=="help" (
    echo Usage:
    echo   firebase-fix.bat           Login + verify project
    echo   firebase-fix.bat login     Login only
    echo   firebase-fix.bat deploy    Login + build + deploy
    echo   firebase-fix.bat token     CI token for GitHub Actions
    goto :done
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\firebase-windows.ps1"

:done
echo.
pause
