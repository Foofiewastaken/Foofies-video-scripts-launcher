@echo off
setlocal enabledelayedexpansion

:: Get the folder where the batch file is located
set "SCRIPT_DIR=%~dp0"

:loop
:: Reset artist variable
set "ARTIST="

:: Ask for Spotify URL
set /p SPOTIFY_LINK=Paste Spotify URL (or type EXIT to quit) and press Enter: 
if /i "!SPOTIFY_LINK!"=="EXIT" goto exit

:: Ask for artist (optional)
echo Artist name is optional but can help improve search accuracy.
echo It'll also be used for the directory name.
set /p ARTIST=Optional: Enter main artist (or leave empty): 

:: Ask if user wants music video
:ask_choice
set /p CHOICE=Do you want the music video? (y/n): 
if /i "!CHOICE!"=="y" (
    echo.
    echo Searching YouTube and preparing video download...
    python "%SCRIPT_DIR%spotify_to_ytm_unified.py" "!SPOTIFY_LINK!" "!ARTIST!" -v
) else if /i "!CHOICE!"=="n" (
    echo.
    echo Searching YouTube and preparing audio download...
    python "%SCRIPT_DIR%spotify_to_ytm_unified.py" "!SPOTIFY_LINK!" "!ARTIST!"
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
