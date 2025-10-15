@echo off
setlocal enabledelayedexpansion

:: Get the folder where the batch file is located
set "SCRIPT_DIR=%~dp0"

:loop
set /p SPOTIFY_LINK=Paste Spotify URL (or type EXIT to quit) and press Enter: 
if /i "!SPOTIFY_LINK!"=="EXIT" goto exit

:: Call the Python download script
python "%SCRIPT_DIR%spotify_to_ytm_download.py" "!SPOTIFY_LINK!"

echo.
echo Download finished (or an error occurred). Press any key to continue.
pause >nul
echo.
goto loop

:exit
echo Exiting...
pause
