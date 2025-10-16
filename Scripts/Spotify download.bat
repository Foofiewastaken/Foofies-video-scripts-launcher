@echo off
setlocal enabledelayedexpansion

:: Get the folder where the batch file is located
set "SCRIPT_DIR=%~dp0"

:loop
:: Ask for Spotify URL
set /p SPOTIFY_LINK=Paste Spotify URL (or type EXIT to quit) and press Enter: 
if /i "!SPOTIFY_LINK!"=="EXIT" goto exit

:: Ask if user wants music video
:ask_choice
set /p CHOICE=Do you want the music video? (y/n): 
if /i "!CHOICE!"=="y" (
    python "%SCRIPT_DIR%spotify_to_ytm_video.py" "!SPOTIFY_LINK!"
) else if /i "!CHOICE!"=="n" (
    python "%SCRIPT_DIR%spotify_to_ytm_mp3.py" "!SPOTIFY_LINK!"
) else (
    echo Invalid choice, please enter y or n.
    goto ask_choice
)

echo.
echo Download finished (or an error occurred). Press any key to continue.
pause >nul
echo.
goto loop

:exit
echo Exiting...
pause
